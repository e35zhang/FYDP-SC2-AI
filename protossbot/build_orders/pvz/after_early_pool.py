from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def pvz_after_early_pool() -> BuildOrder:
    return BuildOrder(
        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 2),
        ChronoUnit(UnitTypeId.COLOSSUS, UnitTypeId.ROBOTICSFACILITY, 1),
        ChronoUnit(UnitTypeId.WARPPRISM, UnitTypeId.ROBOTICSFACILITY, 1),
        SequentialList(
            Tech(UpgradeId.WARPGATERESEARCH),
            Expand(2),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            ProtossUnit(UnitTypeId.ZEALOT, 1, priority=True),
            ProtossUnit(UnitTypeId.ADEPT, 2, priority=True),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            BuildGas(2),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSBAY, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=2, priority=True),
            BuildGas(4),
            ProtossUnit(UnitTypeId.IMMORTAL, to_count=2, priority=True),
            ProtossUnit(UnitTypeId.COLOSSUS, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.WARPPRISM, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=8, priority=True),
            ProtossUnit(UnitTypeId.OBSERVER, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, priority=True),
        ),
    )