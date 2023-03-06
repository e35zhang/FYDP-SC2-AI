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


def counterLingRush() -> BuildOrder:
    return BuildOrder(
        ChronoAnyTech(save_to_energy=100),
        ChronoUnit(UnitTypeId.ZEALOT, UnitTypeId.GATEWAY, 1),
        ChronoUnit(UnitTypeId.ADEPT, UnitTypeId.GATEWAY, 4),

        AutoPylon(),
        AutoWorker(),

        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
        BuildGas(1),
        ProtossUnit(UnitTypeId.ZEALOT, to_count=1, priority=True, only_once=True),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
        ProtossUnit(UnitTypeId.ADEPT, to_count=2, priority=True, only_once=True),
        ProtossUnit(UnitTypeId.ZEALOT, to_count=2, priority=True),

        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
        ProtossUnit(UnitTypeId.ADEPT, to_count=6, priority=True),
        DoubleAdeptScout(5),

        Step(Supply(32),
             Tech(UpgradeId.WARPGATERESEARCH)),
        Step(Supply(32),
             BuildGas(2)),
        Step(Supply(44),
             Expand(2, priority=True)),
        Step(UnitExists(UnitTypeId.NEXUS, 2),
             GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=8, priority=True)),
        StepBuildGas(4, UnitExists(UnitTypeId.GATEWAY, 6)),

        Step(EnemyUnitExists(UnitTypeId.ZERGLING, 8),
             ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=14)),

        ProtossUnit(UnitTypeId.STALKER, priority=True),
        common_strategy()
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
