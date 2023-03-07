from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def pvp_mid_game_macro() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),
        SequentialList(
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
            BuildGas(1),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Tech(UpgradeId.WARPGATERESEARCH),
            ProtossUnit(UnitTypeId.STALKER, 1, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.SENTRY, 1, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 3, only_once=True, priority=True),
            # my 2nd base ~ 2:45
            Expand(2),
            # 3 stalker+1sentry at ~ 3:20 for early adept
            # ~ 3:30 HallucinatedPhoenixScout reach enemy base
            # the HallucinatedPhoenixScout() is modified to scout more enemy tech line
            DefensivePylons(to_base_index=1),
            GridBuilding(unit_type=UnitTypeId.TWILIGHTCOUNCIL, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 5, only_once=True, priority=True),
            DefensiveCannons(0, 1, 1),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True),
            Tech(UpgradeId.BLINKTECH),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 8, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.SENTRY, 2, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.OBSERVER, 1, only_once=True, priority=True),
            BuildGas(4),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSBAY, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6, priority=True),
            ProtossUnit(UnitTypeId.STALKER, 11, only_once=True, priority=True),
            ProtossUnit(UnitTypeId.DISRUPTOR, 1, only_once=True, priority=True),
        ),
        BuildOrder(
            # TODO
            # keep optimize
            AutoWorker(),
            AutoPylon(),

            Step(EnemyUnitExists(UnitTypeId.DARKTEMPLAR),
                 ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=1)),

            ChronoAnyTech(save_to_energy=50),
            ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 5),
            ChronoUnit(UnitTypeId.CARRIER, UnitTypeId.STARGATE, 5),
            ChronoUnit(UnitTypeId.MOTHERSHIP, UnitTypeId.NEXUS, 2),

            ProtossUnit(UnitTypeId.ADEPT, 4, only_once=True, priority=True),

            Step(Supply(90),
                 Expand(3, priority=True)),
            Step(EnemyUnitExists(UnitTypeId.NEXUS, 3), Expand(3, priority=True)),
            Step(EnemyUnitExists(UnitTypeId.PHOTONCANNON, 2), Expand(3, priority=True)),

            ProtossUnit(UnitTypeId.DISRUPTOR, 3, priority=True),

            Step(Time(time_in_seconds=4 * 60),
                 Scout(UnitTypeId.PROBE, 1,
                       ScoutLocation.scout_enemy3(),
                       ScoutLocation.scout_enemy4(),
                       ScoutLocation.scout_enemy5(),
                       )
                 ),

            Step(EnemyUnitExists(UnitTypeId.ZEALOT),
                 ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=4)),
            Step(EnemyUnitExists(UnitTypeId.VOIDRAY),
                 ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=12)),
            Step(EnemyUnitExists(UnitTypeId.STALKER, 8),
                 ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=4)),

            DefensiveCannons(0, 1, 2),
            DefensiveCannons(0, 1, 3),

            SequentialList(
                Tech(UpgradeId.PROTOSSGROUNDARMORSLEVEL1),
                Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1),
                Tech(UpgradeId.PROTOSSSHIELDSLEVEL1),
                Tech(UpgradeId.PROTOSSGROUNDARMORSLEVEL2),
            ),

            # eco plan
            StepBuildGas(to_count=6, requirement=UnitExists(UnitTypeId.NEXUS, 3)),

            Step(Supply(80), GridBuilding(unit_type=UnitTypeId.STARGATE, to_count=1)),

            # this is the final golden armada
            Step(Supply(120), self.pvt_macro_build()),

            # units

            ProtossUnit(UnitTypeId.OBSERVER, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.IMMORTAL, 2), ProtossUnit(UnitTypeId.WARPPRISM, to_count=1, priority=True)),
            ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=4),
            ProtossUnit(UnitTypeId.VOIDRAY, priority=True, to_count=4),
            ProtossUnit(UnitTypeId.STALKER, priority=True),

        ),
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
