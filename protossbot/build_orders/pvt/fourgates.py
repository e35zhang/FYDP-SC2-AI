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


def pvt_fourgates() -> BuildOrder:
    return BuildOrder(
        SequentialList(
            Workers(13),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            WorkerScout(),
            Workers(15),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.PYLON), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 1)),
            Workers(17),
            BuildGas(2),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            Workers(20),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
            Workers(22),
            Tech(UpgradeId.WARPGATERESEARCH),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=2, only_once=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=3, priority=True),
            ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=3, only_once=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
            BuildOrder(
                AutoPylon(),
                ProtossUnit(UnitTypeId.STALKER, priority=True),
            )
        ),
        common_strategy(),

    )
def common_strategy() -> BuildOrder:
    return BuildOrder(
        Step(UnitExists(UnitTypeId.STALKER, 1, include_not_ready=False), DoubleAdeptScout(1)),
        SequentialList(
            DistributeWorkers(),
            PlanHallucination(),
            HallucinatedPhoenixScout(),
            PlanCancelBuilding(),
            WorkerRallyPoint(),
            PlanZoneGather(),
            PlanZoneDefense(),
            Step(UnitExists(UnitTypeId.WARPPRISM, include_not_ready=True), action=PlanZoneAttack(start_attack_power=0)),
            PlanFinishEnemy(),
        )
    )
