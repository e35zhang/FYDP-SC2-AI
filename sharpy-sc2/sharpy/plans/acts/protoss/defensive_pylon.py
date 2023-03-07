import warnings
from typing import Optional

from sharpy.general.zone import Zone
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
from sharpy.interfaces import IZoneManager

from sharpy.plans.acts.act_base import ActBase


class DefensivePylons(ActBase):
    zone_manager: IZoneManager
    """Act of starting to build new buildings up to specified count"""

    def __init__(self, c: int):
        self.to_base_index = to_base_index
        super().__init__()

    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)
        self.zone_manager = knowledge.get_required_manager(IZoneManager)

    async def execute(self) -> bool:
        map_center = self.ai.game_info.map_center

        # Go through zones so that furthest expansions are fortified first
        zones = self.zone_manager.expansion_zones
        for i in range(0, len(zones)):
            zone = zones[i]
            # Filter out zones that aren't ours and own zones that we are about to lose.
            if zone.our_townhall is None or zone.known_enemy_power.ground_power > zone.our_power.ground_presence:
                continue

            if self.to_base_index is not None and i != self.to_base_index:
                # Defenses are not ordered to that base
                continue

            closest_pylon = None
            pylons = zone.our_units(UnitTypeId.PYLON)
            if pylons.exists:
                closest_pylon = pylons.closest_to(zone.center_location)

            available_minerals = self.ai.minerals - self.knowledge.reserved_minerals
            can_afford = available_minerals >= 100

            if closest_pylon is None or closest_pylon.distance_to(zone.center_location) > 10:
                # We need a pylon, but only if one isn't already on the way
                if not self.pending_build(UnitTypeId.PYLON) and can_afford:
                    await self.build(UnitTypeId.PYLON, near=zone.center_location.towards(map_center, 4))
        return True
