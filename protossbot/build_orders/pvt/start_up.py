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


def pvt_start_up() -> BuildOrder:
    return BuildOrder(
        SequentialList(
            Workers(13),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            WorkerScout(),
            Workers(15),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.PYLON), action=ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 1)),
            Workers(17),
            BuildGas(1),
            Workers(20),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Expand(2, priority=True),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=2, priority=True),
            Workers(21),
            BuildGas(2),
            ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=1, only_once=True),
            ChronoUnit(UnitTypeId.ADEPT, UnitTypeId.GATEWAY, 1),
            Tech(UpgradeId.WARPGATERESEARCH),
            BuildOrder(
                AutoWorker(),
                Step(UnitExists(UnitTypeId.NEXUS, count=2, include_not_ready=False), AutoPylon()),
                ChronoTech(AbilityId.RESEARCH_BLINK, UnitTypeId.TWILIGHTCOUNCIL),
                SequentialList(
                    GridBuilding(unit_type=UnitTypeId.TWILIGHTCOUNCIL, to_count=1, priority=True),
                    ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=1, only_once=True),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
                    Tech(UpgradeId.BLINKTECH),
                    GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
                    ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=2, only_once=True),
                    GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
                    ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=5, only_once=True),
                    BuildGas(3),
                    ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
                    ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=12, only_once=True),
                    BuildOrder(
                        Expand(3),
                        BuildGas(4),
                        GridBuilding(unit_type=UnitTypeId.ROBOTICSBAY, to_count=1, priority=True),
                        ProtossUnit(UnitTypeId.WARPPRISM, priority=True, to_count=1),
                        ProtossUnit(UnitTypeId.COLOSSUS, priority=True, to_count=3),
                        Tech(UpgradeId.EXTENDEDTHERMALLANCE),
                        ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=8),
                        Tech(UpgradeId.CHARGE),
                        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=10, priority=True),
                        ProtossUnit(UnitTypeId.ZEALOT, priority=True)
                    )
                )
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
            Step(Time(4*60+50), action=PlanZoneAttack()),
            PlanFinishEnemy(),
        )
    )
