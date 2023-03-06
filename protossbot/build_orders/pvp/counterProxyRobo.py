from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterProxyRobo() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),
        Step(EnemyUnitExists(UnitTypeId.DARKTEMPLAR),
             ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=1)),

        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 10),
        ChronoUnit(UnitTypeId.STALKER, UnitTypeId.GATEWAY, 10),
        ChronoUnit(UnitTypeId.WARPPRISM, UnitTypeId.ROBOTICSFACILITY, 1),

        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        BuildGas(2),
        DefensiveCannons(0, 1, 0),
        Step(Supply(60),
             Expand(2, priority=True)),
        StepBuildGas(requirement=UnitExists(UnitTypeId.PROBE, 36), to_count=4),

        Step(EnemyUnitExists(UnitTypeId.VOIDRAY),
             ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=8)),

        GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=2),

        Step(UnitExists(UnitTypeId.IMMORTAL, 2),
             ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1)),
        Step(UnitExists(UnitTypeId.IMMORTAL, 2),
             ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=1)),
        Step(UnitExists(UnitTypeId.IMMORTAL, 2),
             ProtossUnit(UnitTypeId.STALKER, priority=True)),

        ProtossUnit(UnitTypeId.SENTRY, priority=True, to_count=1, only_once=True),
        ProtossUnit(UnitTypeId.IMMORTAL, priority=True),
        common_strategy()

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
