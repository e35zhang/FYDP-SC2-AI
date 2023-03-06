from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterProxyFourGates() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),

        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 10),

        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        BuildGas(2),
        ProtossUnit(UnitTypeId.STALKER, to_count=2, priority=True, only_once=True),

        Tech(UpgradeId.WARPGATERESEARCH),
        Expand(2, priority=True),
        DefensiveCannons(0, 1, 1),

        Step(EnemyUnitExists(UnitTypeId.STALKER, 6),
             ProtossUnit(UnitTypeId.SENTRY, priority=True, to_count=1)),

        Step(EnemyUnitExists(UnitTypeId.VOIDRAY),
             ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=8)),
        Step(EnemyUnitExists(UnitTypeId.ADEPT, 4),
             ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=6)),
        Step(EnemyUnitExists(UnitTypeId.STALKER, 4),
             ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=4)),
        Step(EnemyUnitExists(UnitTypeId.STALKER, 8),
             ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=8)),

        Step(Supply(60),
             BuildGas(3)),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
        Step(UnitExists(UnitTypeId.GATEWAY, 6),
             GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True)),
        Step(Supply(64),
             GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6, priority=True)),
        ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
        ProtossUnit(UnitTypeId.STALKER, priority=True),
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
