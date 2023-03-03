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


def pvz_start_up() -> BuildOrder:
    return BuildOrder(
        SequentialList(
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            Workers(15),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.GATEWAY), action=WorkerScout()),
            Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 1)),
            Workers(16),
            BuildGas(1),
            Workers(19),
            Expand(2),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Workers(21),
            BuildGas(2),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),

            ProtossUnit(UnitTypeId.ADEPT, 1, only_once=True, priority=True),
            Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 2)),
            BuildOrder(
                AutoWorker(),
                AutoPylon(),
                SequentialList(
                    GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=1, priority=True),
                    Tech(UpgradeId.WARPGATERESEARCH),
                    Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 3)),
                    ProtossUnit(UnitTypeId.ADEPT, 2, only_once=True, priority=True),
                    ProtossUnit(UnitTypeId.ORACLE, 1, only_once=True, priority=True),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
                    Expand(3),
                    Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 4)),
                    ProtossUnit(UnitTypeId.ORACLE, 2, only_once=True, priority=True),
                    ProtossUnit(UnitTypeId.ADEPT, 3, only_once=True, priority=True),
                    BuildGas(3),
                    GridBuilding(unit_type=UnitTypeId.TWILIGHTCOUNCIL, to_count=1, priority=True),
                    GridBuilding(unit_type=UnitTypeId.FORGE, to_count=1, priority=True),
                    Step(UnitExists(UnitTypeId.NEXUS), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 5)),
                    ProtossUnit(UnitTypeId.ORACLE, 3, only_once=True, priority=True),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
                    Tech(UpgradeId.BLINKTECH),
                    Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1),
                    ChronoAnyTech(save_to_energy=0),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6, priority=True),
                    BuildGas(3),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=8, priority=True),
                    BuildGas(4),
                    ProtossUnit(UnitTypeId.STALKER, 60, priority=True),
                )
            )
        ),
        common_strategy()
    )


def common_strategy() -> SequentialList:
    return SequentialList(
        DoubleAdeptScout(),
        DistributeWorkers(),
        PlanHallucination(),
        HallucinatedPhoenixScout(),
        PlanCancelBuilding(),
        WorkerRallyPoint(),
        PlanZoneGather(),
        PlanZoneDefense(),
        Step(TechReady(UpgradeId.BLINKTECH, 0.9), action=PlanZoneAttack()),
        PlanFinishEnemy(),
    )
