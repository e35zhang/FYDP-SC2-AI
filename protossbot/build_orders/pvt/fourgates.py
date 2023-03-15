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
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINE), ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINEBURROWED),
             ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),
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
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
            Workers(23),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.ADEPT, 2, only_once=True, priority=True),
            ChronoUnit(UnitTypeId.ADEPT, UnitTypeId.GATEWAY, 2),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=2, only_once=True),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=3, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
            ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=4, only_once=True),
            BuildOrder(
                AutoPylon(),
                ProtossUnit(UnitTypeId.OBSERVER, to_count=1, priority=True),
                ProtossUnit(UnitTypeId.STALKER, priority=True),
            )
        ),
        common_strategy(),

    )
def common_strategy() -> BuildOrder:
    return BuildOrder(
        DoubleAdeptScout(2),
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
