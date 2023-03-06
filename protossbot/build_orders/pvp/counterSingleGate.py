from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterSingleGate() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),
        DoubleAdeptScout(2),
        ChronoAnyTech(0),
        ChronoUnit(UnitTypeId.ADEPT, UnitTypeId.GATEWAY, count=2),

        SequentialList(
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Workers(22),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
            Workers(23),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=2),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
            ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=4),
            ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=6),
            BuildOrder(
                Step(Gas(400), ProtossUnit(UnitTypeId.SENTRY, priority=True)),
                ProtossUnit(UnitTypeId.STALKER, priority=True),
            ),
        common_strategy()
        )
    )


def common_strategy() -> BuildOrder:
    return BuildOrder(
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        PlanZoneAttack(),
        PlanFinishEnemy()
    )
