from sharpy.interfaces import ILostUnitsManager
from sharpy.plans.acts import ActUnit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from sc2.ids.upgrade_id import UpgradeId
from .warp_unit import WarpUnit


class ProtossUnit(ActUnit):
    lost_units_manager: ILostUnitsManager

    def __init__(self, unit_type: UnitTypeId, to_count: int = 9999, priority: bool = False, only_once: bool = False):
        production_units: set = UNIT_TRAINED_FROM.get(unit_type, {UnitTypeId.GATEWAY})

        if UnitTypeId.GATEWAY in production_units:
            super().__init__(unit_type, UnitTypeId.GATEWAY, to_count, priority)
        else:
            super().__init__(unit_type, list(production_units)[0], to_count, priority)

        self.only_once = only_once

        if UnitTypeId.WARPGATE in production_units:
            self.warp = WarpUnit(unit_type, to_count)
        else:
            self.warp = None

    def get_unit_count(self) -> int:
        count = super().get_unit_count()

        if self.only_once:
            count += self.lost_units_manager.own_lost_type(self.unit_type)
        return count

    async def start(self, knowledge: "Knowledge"):
        if self.warp:
            await self.warp.start(knowledge)
        await super().start(knowledge)
        self.lost_units_manager = knowledge.get_required_manager(ILostUnitsManager)

    async def execute(self) -> bool:
        if self.ai.already_pending_upgrade(UpgradeId.WARPGATERESEARCH) >= 1:
            if self.is_done:
                return True
            # Ensure that unit types are the same, python please some proper setters and getters?!?
            if self.warp:
                self.warp.unit_type = self.unit_type
                self.warp.to_count = self.to_count
                return await self.warp.execute()

        return await super().execute()
