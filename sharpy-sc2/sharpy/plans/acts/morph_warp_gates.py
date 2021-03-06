import sc2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from .act_base import ActBase


class MorphWarpGates(ActBase):
    def __init__(self):
        super().__init__()

    async def execute(self) -> bool:
        target: Unit
        for target in self.cache.own(UnitTypeId.GATEWAY).ready:
            target(AbilityId.MORPH_WARPGATE)

        return True
