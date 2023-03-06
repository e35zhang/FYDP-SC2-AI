from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterCannonRush() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),

        ChronoUnit(UnitTypeId.STALKER, UnitTypeId.GATEWAY, 10),
        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.GATEWAY, 10),
        ProtossUnit(UnitTypeId.SENTRY, priority=True, to_count=1),
        ProtossUnit(UnitTypeId.IMMORTAL, priority=True),
        ProtossUnit(UnitTypeId.STALKER, priority=True),
        Tech(UpgradeId.WARPGATERESEARCH),

        Step(UnitExists(UnitTypeId.GATEWAY),
             BuildGas(2)),
        Step(UnitExists(UnitTypeId.CYBERNETICSCORE),
             GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True)),
        Step(UnitExists(UnitTypeId.CYBERNETICSCORE),
             GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True)),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        common_strategy(),
    )


def common_strategy() -> SequentialList:
    return SequentialList(
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        PlanZoneAttack(),
        PlanFinishEnemy(),
    )
