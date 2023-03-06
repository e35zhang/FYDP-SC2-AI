from sc2.unit import Unit
from sharpy.plans.acts import ActBase
from sharpy.managers.core.roles import UnitTask
from sharpy.knowledges import Knowledge
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
import random


class OracleHarass(ActBase):
    def __init__(self):
        super().__init__()
        self.oracle_tags = []
        self.harass_started = False
        self.already_begin_attack = []
        self.reached_position = []
        self.grouped = True
        self.group_check = 0

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)

    async def execute(self) -> bool:
        oracles = self.knowledge.unit_cache.own(UnitTypeId.ORACLE).ready
        position = self.get_enemy_base(0)
        if oracles.amount >= 1:
            for oracles_index in range(len(oracles)):
                if not oracles[oracles_index].tag in self.oracle_tags:
                    self.knowledge.roles.set_task(UnitTask.Reserved, oracles[oracles_index])
                    self.oracle_tags.append(oracles[oracles_index].tag)
                    self.reached_position.append(False)
                    self.already_begin_attack.append(False)
                    if oracles.amount > 1:
                        self.grouped = False
            self.harass_started = True
        else:
            self.harass_started = False
        self.roles.refresh_tasks(oracles)
        if self.harass_started:
            if len(oracles) >= 2:
                self.group_check = 0
                for oracle_index in range(len(self.oracle_tags)):
                    harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
                    self.oracle_evasive_move_to(oracle_index, position)
                    if harass_oracle is not None:
                        if harass_oracle.distance_to(position) <= 5:
                            self.group_check += 1
                if self.group_check == len(self.oracle_tags):
                    self.grouped = True
                    print("grouped")
            for oracle_index in range(len(self.oracle_tags)):
                harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
                if harass_oracle is not None and self.grouped == True:
                    if not self.reached_position[oracle_index]:
                        if harass_oracle.distance_to(position) <= 5 and harass_oracle.energy >= 50:
                            self.reached_position[oracle_index] = True
                        elif harass_oracle.shield_percentage >= 0.95:
                            enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 13).of_type(
                                [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.MULE]
                            )
                            if enemy_workers.amount >= 3 and harass_oracle.energy >= 40:
                                self.reached_position[oracle_index] = True
                            else:
                                self.oracle_evasive_move_to(oracle_index, position)
                        elif harass_oracle.shield_percentage <= 0.3:
                            if self.knowledge.zone_manager.our_zones:
                                self.oracle_evasive_move_to(oracle_index, position)
                    else:
                        await self.harass_with_oracle()
        return True  # never block

    async def harass_with_oracle(self):
        group_point = self.get_group_oracle_flank_position()
        target = self.get_enemy_base(0)
        for oracle_index in range(len(self.oracle_tags)):
            harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
            if harass_oracle is not None:
                if not self.already_begin_attack[oracle_index]:
                    harass_oracle.move(target)
                    enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 8).of_type(
                        [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.MULE]
                    )
                    # worth activate weapon
                    if enemy_workers.amount >= 3 and harass_oracle.energy >= 40:
                        self.already_begin_attack[oracle_index] = True
                        harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMON)
                        return
                if self.already_begin_attack[oracle_index] and harass_oracle.energy <= 1:
                    self.already_begin_attack[oracle_index] = False
                    return

                if not self.oracle_in_danger() and self.already_begin_attack[oracle_index]:
                    enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 8).of_type(
                        [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.MULE]
                    )
                    if enemy_workers.exists:
                        # try attack the ones that can be one shot killed
                        attack_target = None
                        for worker in enemy_workers:
                            if worker.shield_health_percentage < 0.5:
                                attack_target = worker
                                break
                        if attack_target is None:
                            attack_target = enemy_workers.closest_to(harass_oracle)
                        harass_oracle.attack(attack_target)
                    else:
                        # gather intel
                        self.oracle_evasive_move_to(oracle_index, self.knowledge.zone_manager.enemy_expansion_zones[0].behind_mineral_position_center)
                elif self.oracle_in_danger() and self.already_begin_attack[oracle_index]:
                    if harass_oracle.shield_percentage <= 0.3:
                        self.oracle_evasive_move_to(oracle_index, group_point)
                else:
                    if harass_oracle.energy <= 2:
                        harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMOFF)
                        self.already_begin_attack[oracle_index] = False
                        self.reached_position[oracle_index] = False
                    self.oracle_evasive_move_to(oracle_index, group_point)

    def oracle_in_danger(self):
        for oracle_index in range(len(self.oracle_tags)):
            harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
            enemy_anti_air_units = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 11) \
                .filter(lambda unit: unit.can_attack_air).visible
            enemy_anti_air_structure = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 11) \
                .of_type(UnitTypeId.BUNKER)
            for AA in enemy_anti_air_units:
                if AA.position.distance_to(harass_oracle) < AA.air_range + 5:
                    return True

            for AA in enemy_anti_air_structure:
                if AA.position.distance_to(harass_oracle) < 12:
                    return True
            return False

    def oracle_evasive_move_to(self, oracle_index, position_to):
        harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
        if harass_oracle is not None:
            enemy_anti_air_structure = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 11) \
            .of_type(UnitTypeId.BUNKER)
            enemy_anti_air_units = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 11) \
            .filter(lambda unit: unit.can_attack_air).visible

            if enemy_anti_air_units.exists or enemy_anti_air_structure.exists:
                position = harass_oracle.position3d
                for aa in enemy_anti_air_units:
                    distance = harass_oracle.distance_to(aa.position3d)
                    if distance > 0:
                        amount_of_evade = 20 - distance
                        position = position.towards(aa, - amount_of_evade)
                for aa in enemy_anti_air_structure:
                    distance = harass_oracle.distance_to(aa.position3d)
                    if distance > 0:
                        amount_of_evade = 15 - distance
                        position = position.towards(aa, - amount_of_evade)
                # after the for loop, position is the best vector away from enemy
                distance_to_best_evade_point = harass_oracle.distance_to(position) * 0.7 + 0.1
                should_go = position.towards(position_to, distance_to_best_evade_point)
                harass_oracle.move(should_go)
            else:
                harass_oracle.move(position_to)

    def get_first_oracle_flank_position(self):
        distance = 1.3 * self.knowledge.zone_manager.enemy_expansion_zones[1].behind_mineral_position_center. \
            distance_to(self.knowledge.zone_manager.enemy_expansion_zones[0].center_location)
        return self.knowledge.zone_manager.enemy_expansion_zones[0].center_location. \
            towards(self.knowledge.zone_manager.enemy_expansion_zones[1].behind_mineral_position_center, distance)

    def get_group_oracle_flank_position(self):
        return self.knowledge.zone_manager.enemy_expansion_zones[5].center_location

    def get_enemy_base(self, base_index):
        return self.knowledge.zone_manager.enemy_expansion_zones[base_index].behind_mineral_position_center