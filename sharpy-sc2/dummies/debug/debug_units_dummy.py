from sc2.ids.unit_typeid import UnitTypeId
from sharpy.plans.require import Time
from sharpy.plans.tactics import DistributeWorkers, PlanZoneAttack

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step


class DebugUnitsDummy(KnowledgeBot):
    """Dummy bot for creating debug units to test against."""

    def __init__(self):
        super().__init__(type(self).__name__)

    async def create_plan(self) -> BuildOrder:
        attack = PlanZoneAttack(1)
        attack.retreat_multiplier = 0.1
        attack.attack_on_advantage = False

        return BuildOrder([DistributeWorkers(), Step(Time(60), attack)])

    async def on_step(self, iteration):
        # Hack so that BuildingSolver is finally ready to give positions for the debug buildings.
        if iteration == 1:
            await self.create_debug_buildings()

        await super().on_step(iteration)

    async def create_debug_buildings(self):
        pid = self.player_id
        unit_type = UnitTypeId.VIPER
        amount = 1

        for i in range(0, 5):
            await self._client.debug_create_unit(
                [
                    [
                        UnitTypeId.COLOSSUS,
                        amount,
                        self.knowledge.enemy_expansion_zones[1].center_location.random_on_distance(4),
                        2,
                    ]
                ]
            )

        # Enemy 3rd
        pos = self.zone_manager.expansion_zones[-3].center_location

        await self._client.debug_create_unit([[unit_type, amount, pos, pid]])

        # Enemy 4th
        pos = self.zone_manager.expansion_zones[-4].center_location

        await self._client.debug_create_unit([[unit_type, amount, pos, pid]])

        await self._client.debug_create_unit([[UnitTypeId.OVERSEER, amount, pos, pid]])

        # Own natural
        pos = self.zone_manager.expansion_zones[1].center_location

        await self._client.debug_create_unit([[unit_type, amount, pos, pid]])

        # Own main
        pos = self.zone_manager.expansion_zones[0].center_location

        await self._client.debug_create_unit([[unit_type, amount, pos, pid]])
        await self._client.debug_create_unit([[UnitTypeId.WIDOWMINEBURROWED, amount, pos, pid]])

        await self._client.debug_tech_tree()
