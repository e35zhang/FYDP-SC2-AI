from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *
from sharpy.plans.acts import DefensePosition


def pvp_start_up() -> BuildOrder:
    return BuildOrder(
        SequentialList(
            Workers(14),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.PYLON), action=WorkerScout()),
            Workers(15),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 1)),
            Workers(17),
            BuildGas(1),
            Workers(18),
            BuildGas(2),
            Workers(19),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Workers(20),
            PositionBuilding(unit_type=UnitTypeId.PYLON, to_count=2,
                             position_type=DefensePosition.BehindMineralLineRight),
            Workers(23),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.STALKER, 1, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.SENTRY, 1, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 3, only_once=True, priority=True),
            Expand(2),
            ProtossUnit(UnitTypeId.STALKER, to_count=40, priority=True),
            AutoPylon(),
            AutoWorker(),
        ),
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
