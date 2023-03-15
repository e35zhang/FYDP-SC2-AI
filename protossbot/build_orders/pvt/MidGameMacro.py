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


def pvt_mid_game_micro() -> BuildOrder:
    return BuildOrder(
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINE), ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINEBURROWED),
             ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),
        AutoWorker(),
        Step(UnitExists(UnitTypeId.NEXUS, count=2, include_not_ready=False), AutoPylon()),
        ChronoUnit(UnitTypeId.COLOSSUS, UnitTypeId.ROBOTICSFACILITY, 6),
        Step(
            Gas(500), ProtossUnit(UnitTypeId.HIGHTEMPLAR, priority=True, to_count=8),
        ),

        SequentialList(
            Expand(3),
            DefensivePylons(2),
            BuildGas(4),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSBAY, to_count=1, priority=True),
            BuildOrder(
                DefensiveCannons(0, 1, 2),
                ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=12, only_once=True),
                ProtossUnit(UnitTypeId.COLOSSUS, priority=True, to_count=3),
                Tech(UpgradeId.EXTENDEDTHERMALLANCE),
                ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
                ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=8),
                Tech(UpgradeId.CHARGE),
                GridBuilding(unit_type=UnitTypeId.TEMPLARARCHIVE, to_count=1),
                Tech(UpgradeId.PSISTORMTECH),
                GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=10, priority=True),
                ProtossUnit(UnitTypeId.HIGHTEMPLAR, priority=True, to_count=4),
                ProtossUnit(UnitTypeId.ZEALOT, priority=True),
            ),
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
            Step(Time(4*60+50), action=PlanZoneAttack()),
            PlanFinishEnemy(),
        )
    )
