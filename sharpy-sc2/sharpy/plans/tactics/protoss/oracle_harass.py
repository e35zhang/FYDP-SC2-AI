from sc2.unit import Unit
from sharpy.plans.acts import ActBase
from sharpy.managers.core.roles import UnitTask
from sharpy.knowledges import Knowledge
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
import random


class OracleHarass(ActBase):
    def __init__(self):
        super().__init__()
        self.oracle_tags = []
        self.harass_started = False
        self.already_begin_attack = []
        self.reached_position = []
        self.ended = False

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)

    async def execute(self) -> bool:
        if self.ended:
            return True
        if self.ai.time > 6*60+40:
            self.ended = True
            return True
        oracles = self.knowledge.unit_cache.own(UnitTypeId.ORACLE).ready
        position = self.get_group_oracle_flank_position()
        retreat_point = self.get_retreat_point()
        if oracles.amount >= 1:
            for oracles_index in range(len(oracles)):
                if not oracles[oracles_index].tag in self.oracle_tags:
                    self.knowledge.roles.set_task(UnitTask.Reserved, oracles[oracles_index])
                    self.oracle_tags.append(oracles[oracles_index].tag)
                    self.reached_position.append(False)
                    self.already_begin_attack.append(False)
            self.harass_started = True
        else:
            self.harass_started = False
        self.roles.refresh_tasks(oracles)
        if self.harass_started:
            for oracle_index in range(len(self.oracle_tags)):
                harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
                if harass_oracle is not None:
                    if not self.reached_position[oracle_index]:
                        if harass_oracle.distance_to(position) <= 4 and harass_oracle.energy >= 50:
                            self.reached_position[oracle_index] = True
                        elif harass_oracle.shield_percentage >= 0.3:
                            enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position,
                                                                                     7).of_type(
                                [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.MULE]
                            )
                            if enemy_workers.amount >= 3 and harass_oracle.energy >= 40:
                                harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMON)
                                self.reached_position[oracle_index] = True
                            else:
                                self.oracle_evasive_move_to(oracle_index, position)
                        elif harass_oracle.shield_percentage <= 0.3:
                            harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMOFF)
                            if self.knowledge.zone_manager.our_zones:
                                self.oracle_evasive_move_to(oracle_index, retreat_point)
                    else:
                        await self.harass_with_oracle(oracle_index)

        return True  # never block

    async def harass_with_oracle(self, oracle_index):
        retreat_point = self.get_retreat_point()
        regroup_point = self.get_group_oracle_regroup_position()
        harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
        if harass_oracle is not None:
            distance = 9999999
            attack_point = self.knowledge.zone_manager.enemy_expansion_zones[0].behind_mineral_position_center
            for zone in self.knowledge.zone_manager.enemy_expansion_zones:
                if zone.behind_mineral_position_center.distance_to(harass_oracle) < distance and \
                        zone.enemy_workers.amount >= 3:
                    distance = zone.behind_mineral_position_center.distance_to(harass_oracle)
                    attack_point = zone.behind_mineral_position_center
            if not self.already_begin_attack[oracle_index]:

                harass_oracle.move(attack_point)
                enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position, 7).of_type(
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

            if (not self.oracle_in_danger(oracle_index)) and self.already_begin_attack[oracle_index]:
                enemy_workers = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position3d, 12).of_type(
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
                    self.oracle_evasive_move_to(oracle_index, attack_point)
            elif self.oracle_in_danger(oracle_index) and self.already_begin_attack[oracle_index]:
                if harass_oracle.shield_percentage <= 0.3:
                    harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMOFF)
                    self.oracle_evasive_move_to(oracle_index, retreat_point)
                    self.reached_position[oracle_index] = False
            else:
                if harass_oracle.energy <= 2:
                    harass_oracle(AbilityId.BEHAVIOR_PULSARBEAMOFF)
                    self.already_begin_attack[oracle_index] = False
                    self.reached_position[oracle_index] = False
                    self.oracle_evasive_move_to(oracle_index, regroup_point)

    def oracle_in_danger(self, oracle_index):
        harass_oracle: Unit = self.knowledge.unit_cache.by_tag(self.oracle_tags[oracle_index])
        if harass_oracle:
            enemy_anti_air_units = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position, 11) \
                .filter(lambda unit: unit.can_attack_air).visible
            enemy_anti_air_structure = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position, 11) \
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
            enemy_anti_air_structure = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position, 11) \
                .of_type(UnitTypeId.BUNKER)
            enemy_anti_air_units = self.knowledge.unit_cache.enemy_in_range(harass_oracle.position, 11) \
                .filter(lambda unit: unit.can_attack_air).visible

            if (enemy_anti_air_units.exists or enemy_anti_air_structure.exists) and \
                    harass_oracle.shield_percentage <= 0.3:
                position = harass_oracle.position3d
                for aa in enemy_anti_air_units:
                    distance = harass_oracle.distance_to(aa.position)
                    if distance > 0:
                        amount_of_evade = 20 - distance
                        position = position.towards(aa, - amount_of_evade)
                for aa in enemy_anti_air_structure:
                    distance = harass_oracle.distance_to(aa.position)
                    if distance > 0:
                        amount_of_evade = 15 - distance
                        position = position.towards(aa, - amount_of_evade)
                # after the for loop, position is the best vector away from enemy
                distance_to_best_evade_point = harass_oracle.distance_to(position) * 0.7 + 0.1
                should_go = position.towards(position_to, distance_to_best_evade_point)
                harass_oracle.move(should_go)
            else:
                harass_oracle.move(position_to)

    def get_retreat_point(self):
        return self.knowledge.zone_manager.our_zones[0].center_location

    def get_group_oracle_regroup_position(self):
        return self.get_retreat_point()
        enemy_natural_point = self.knowledge.zone_manager.enemy_expansion_zones[1].behind_mineral_position_center
        our_main_point = self.knowledge.zone_manager.our_zones[0].behind_mineral_position_center
        return enemy_natural_point.towards(our_main_point, 45)

    def get_group_oracle_flank_position(self):
        enemy_main = self.knowledge.zone_manager.enemy_expansion_zones[0].behind_mineral_position_center
        our_main = self.knowledge.zone_manager.our_zones[0].behind_mineral_position_center
        dx = enemy_main.x - our_main.x
        dy = enemy_main.y - our_main.y
        p1 = Point2((enemy_main.x - 0.3 * dx, enemy_main.y))
        p2 = Point2((enemy_main.x, enemy_main.y - 0.3 * dy))
        if p1.distance_to(enemy_main) >= p2.distance_to(enemy_main):
            return p2
        else:
            return p1

    def old_get_group_oracle_flank_position(self):
        distance = 1.3 * self.knowledge.zone_manager.enemy_expansion_zones[1].behind_mineral_position_center. \
            distance_to(self.knowledge.zone_manager.enemy_expansion_zones[0].center_location)
        return self.knowledge.zone_manager.enemy_expansion_zones[0].center_location. \
            towards(self.knowledge.zone_manager.enemy_expansion_zones[1].behind_mineral_position_center, distance)
