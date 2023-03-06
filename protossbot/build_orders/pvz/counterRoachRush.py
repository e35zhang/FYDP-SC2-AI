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

from .after_early_pool import pvz_after_early_pool


def counterRoachRush() -> BuildOrder:
    AutoPylon(),
    AutoWorker(),
    ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 2),
    ChronoUnit(UnitTypeId.WARPPRISM, UnitTypeId.ROBOTICSFACILITY, 2),
    DoubleAdeptScout(2),

    Step(EnemyUnitExists(UnitTypeId.ZERGLING, 4),
         ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=1)),
    Step(EnemyUnitExists(UnitTypeId.ZERGLING, 8),
         ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=6)),

    SequentialList(
        BuildGas(2),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
        ProtossUnit(UnitTypeId.ZEALOT, priority=True, to_count=1, only_once=True),
        Step(UnitExists(UnitTypeId.PYLON, 2, include_not_ready=False),
             GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True)),

        BuildOrder(
            ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=4, only_once=True),
        ),

        BuildOrder(
            ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=4),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.ADEPT, priority=True),
            ProtossUnit(UnitTypeId.IMMORTAL, priority=True),
        ),
    )


def common_strategy() -> SequentialList:
    return SequentialList(

        OracleHarass(),
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        Step(UnitExists(UnitTypeId.ZEALOT), action=DoubleAdeptScout()),
        Step(UnitExists(UnitTypeId.WARPPRISM), action=PlanZoneAttack()),
        PlanFinishEnemy(),
    )
