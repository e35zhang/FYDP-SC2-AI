from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def pvt_late_game_macro() -> BuildOrder:
    return BuildOrder(
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINE), ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),
        Step(EnemyUnitExists(UnitTypeId.WIDOWMINEBURROWED),
             ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2)),

        AutoWorker(),
        AutoPylon(),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1),
        StepBuildGas(requirement=UnitExists(UnitTypeId.NEXUS, 3), to_count=6),
        StepBuildGas(requirement=UnitExists(UnitTypeId.NEXUS, 4), to_count=8),
        StepBuildGas(requirement=UnitExists(UnitTypeId.NEXUS, 5), to_count=10),
        ChronoAnyTech(save_to_energy=50),
        ChronoUnit(UnitTypeId.CARRIER, UnitTypeId.STARGATE, 10),
        ChronoUnit(UnitTypeId.MOTHERSHIP, UnitTypeId.NEXUS, 3),
        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 5),
        ChronoUnit(UnitTypeId.DISRUPTOR, UnitTypeId.ROBOTICSFACILITY, 4),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6),
        GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=1),
        GridBuilding(unit_type=UnitTypeId.ROBOTICSBAY, to_count=1),
        GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=2),
        Expand(4),

        #Step(
        #    Minerals(500),
        #    DefensiveCannons(to_count_pre_base=2, additional_batteries=1),
        #),

        Step(
            Minerals(1000),
            ProtossUnit(UnitTypeId.ZEALOT, to_count=12, priority=True),
        ),
        Step(
            Supply(160),
            Expand(5)
        ),

        Step(
            Gas(1000),
            SequentialList(
                GridBuilding(unit_type=UnitTypeId.TEMPLARARCHIVE, to_count=1),
                Tech(UpgradeId.PSISTORMTECH),
                ProtossUnit(UnitTypeId.HIGHTEMPLAR, priority=True, to_count=2),
            )
        ),

        Step(
            UnitExists(UnitTypeId.NEXUS, 4),
            SequentialList(
                Tech(UpgradeId.PROTOSSSHIELDSLEVEL1),
                Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1),
                Tech(UpgradeId.PROTOSSGROUNDARMORSLEVEL1),
                Tech(UpgradeId.PROTOSSAIRWEAPONSLEVEL1),
                Tech(UpgradeId.PROTOSSSHIELDSLEVEL2),
                Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2),
                Tech(UpgradeId.PROTOSSGROUNDARMORSLEVEL2),
                Tech(UpgradeId.PROTOSSAIRWEAPONSLEVEL2),
                Tech(UpgradeId.PROTOSSAIRWEAPONSLEVEL3),
            )
        ),

        Step(
            UnitExists(UnitTypeId.NEXUS, 4),
            SequentialList(
                GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=1, priority=True),
                GridBuilding(unit_type=UnitTypeId.FLEETBEACON, to_count=1, priority=True),
                GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=3, priority=True),
            )
        ),
        ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=1),
        ProtossUnit(UnitTypeId.DISRUPTOR, priority=True, to_count=4),

        ProtossUnit(UnitTypeId.CARRIER, priority=True, to_count=9),
        ProtossUnit(UnitTypeId.MOTHERSHIP, priority=True, to_count=1),

        ProtossUnit(UnitTypeId.HIGHTEMPLAR, priority=True, to_count=4),
        ProtossUnit(UnitTypeId.COLOSSUS, priority=True, to_count=3),
        ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=10),

        common_strategy()
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
        Step(Supply(180), action=PlanZoneAttack()),
        PlanFinishEnemy(),
    )
