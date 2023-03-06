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


def pvz_counter_12d() -> BuildOrder:
    return BuildOrder(
        SequentialList(
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            ProtossUnit(UnitTypeId.ZEALOT, 1, only_once=True, priority=True),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
            ProtossUnit(UnitTypeId.ADEPT, 1, priority=True, only_once=True),
            Step(UnitExists(UnitTypeId.GATEWAY, include_not_ready=False),
                 action=ChronoUnit(UnitTypeId.ADEPT, UnitTypeId.GATEWAY, 1)),
            ProtossUnit(UnitTypeId.ADEPT, 2, priority=True, only_once=True),
            Tech(UpgradeId.WARPGATERESEARCH),
            Expand(to_count=2),
            BuildOrder(
                AutoWorker(),
                AutoPylon(),
                pvz_after_early_pool()
            )
        ),
        common_strategy()
    )


def common_strategy() -> SequentialList:
    return SequentialList(
        DoubleAdeptScout(),
        OracleHarass(),
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        Step(UnitExists(UnitTypeId.WARPPRISM), action=PlanZoneAttack()),
        PlanFinishEnemy(),
    )
