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
        ChronoAnyTech(save_to_energy=0),

        SequentialList(
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 2, only_once=True, priority=True),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.STALKER, 4, only_once=True, priority=True),
            Step(UnitExists(UnitTypeId.CYBERNETICSCORE),
                 GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True)),
        ),

        Step(UnitExists(UnitTypeId.GATEWAY, count=4),
             ProtossUnit(UnitTypeId.STALKER, priority=True)),
        AutoWorker(),
        AutoPylon(),
        common_strategy(),
    )


def common_strategy() -> SequentialList:
    return SequentialList(
        SpeedMining(),
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        PlanZoneAttack(start_attack_power=2),
        PlanFinishEnemy(),
    )
