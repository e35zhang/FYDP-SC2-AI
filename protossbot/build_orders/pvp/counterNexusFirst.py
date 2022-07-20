from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterNexusFirst() -> BuildOrder:
    return BuildOrder(

        ChronoAnyTech(save_to_energy=50),
        Tech(UpgradeId.WARPGATERESEARCH),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
        ProtossUnit(UnitTypeId.STALKER, to_count=40, priority=True),
        AutoWorker(),
        AutoPylon(),
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
