from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def pvp_late_game_macro() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),

        ChronoAnyTech(save_to_energy=50),
        ChronoUnit(UnitTypeId.TEMPEST, UnitTypeId.STARGATE, 10),
        ChronoUnit(UnitTypeId.MOTHERSHIP, UnitTypeId.NEXUS, 3),
        ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 5),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6),

        Step(
            Minerals(700),
            ProtossUnit(UnitTypeId.ZEALOT, priority=True),
        ),

        Step(
            Gas(700),
            SequentialList(
                GridBuilding(unit_type=UnitTypeId.TEMPLARARCHIVE, to_count=1),
                ProtossUnit(UnitTypeId.HIGHTEMPLAR, priority=True),
                Archon([UnitTypeId.HIGHTEMPLAR]),
            )
        ),

        Step(
            UnitExists(UnitTypeId.NEXUS, 4),
            SequentialList(
                Tech(UpgradeId.PROTOSSSHIELDSLEVEL1),
                Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2),
                Tech(UpgradeId.PROTOSSGROUNDARMORSLEVEL2),
                Tech(UpgradeId.PROTOSSSHIELDSLEVEL2),
            )
        ),

        Step(
            UnitExists(UnitTypeId.NEXUS, 4),
            SequentialList(
                GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=1, priority=True),
                GridBuilding(unit_type=UnitTypeId.FLEETBEACON, to_count=1, priority=True),
                ProtossUnit(UnitTypeId.PHOENIX, priority=True, to_count=6),
                ProtossUnit(UnitTypeId.MOTHERSHIP, priority=True, to_count=1),
            )
        ),
        ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=2),

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
