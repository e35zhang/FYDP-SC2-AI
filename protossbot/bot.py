from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

# This imports all the usual components for protoss bots
from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *

class ProtossBot(KnowledgeBot):
    data_manager: DataManager

    def __init__(self, build_name: str = "default"):
        super().__init__("FYDP")
        self.conceded = False
        self.builds: Dict[str, Callable[[], BuildOrder]] = {
            "pvp": lambda: self.pvp_build(),
            "pvz": lambda: self.pvz_build(),
            "pvt": lambda: self.pvt_build(),
            "pvr": lambda: self.pvr_build()
        }
        self.build_name = build_name
        self.enemy_last_intel = None
        self.enemy_intel = None

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        return [BuildDetector()]

    async def create_plan(self) -> BuildOrder:
        if self.build_name == "default":
            if self.knowledge.enemy_race == Race.Protoss:
                self.build_name = "pvp"
            elif self.knowledge.enemy_race == Race.Zerg:
                self.build_name = "pvz"
            elif self.knowledge.enemy_race == Race.Terran:
                self.build_name = "pvt"
            else:
                self.build_name = self.build_name = "pvr"

        self.data_manager.set_build(self.build_name)
        return self.builds[self.build_name]()

    async def on_step(self, iteration):
        self.enemy_intel = self.build_detector.macro_build

        if self.enemy_last_intel is None:
            self.enemy_last_intel = self.enemy_intel

        if self.enemy_last_intel != self.enemy_intel:
            str = "Looks like you wanna "
            str += self.enemy_intel.name
            self.enemy_last_intel = self.enemy_intel
            await self.chat_send(str)
        return await super().on_step(iteration)

    def pvz_build(self) -> BuildOrder:
        return BuildOrder(
            AutoWorker(),
            AutoPylon(),

            WorkerScout(),
            ChronoUnit(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY, 10),

            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            BuildGas(2),
            GridBuilding(unit_type=UnitTypeId.ROBOTICSFACILITY, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.STALKER, to_count=3, priority=True),
            Tech(UpgradeId.WARPGATERESEARCH),
            Step(UnitExists(UnitTypeId.IMMORTAL), Expand(2, priority=True)),
            Step(UnitExists(UnitTypeId.PROBE, 36),
                 BuildGas(4)),
            Step(UnitExists(UnitTypeId.NEXUS, 2),
                 GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=6, priority=True)),

            Step(EnemyUnitExists(UnitTypeId.VOIDRAY),
                 ProtossUnit(UnitTypeId.STALKER, priority=True, to_count=16)),
            Step(EnemyUnitExists(UnitTypeId.IMMORTAL),
                 ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=5)),
            Step(EnemyUnitExists(UnitTypeId.STALKER, 6),
                 ProtossUnit(UnitTypeId.IMMORTAL, priority=True, to_count=5)),

            ProtossUnit(UnitTypeId.OBSERVER, priority=True, to_count=1),
            ProtossUnit(UnitTypeId.STALKER, priority=True),
            ProtossUnit(UnitTypeId.SENTRY, to_count=1, priority=True),
            ProtossUnit(UnitTypeId.IMMORTAL, to_count=2, priority=True),
            self.pvz_create_common_strategy()
        )

    def pvt_build(self) -> BuildOrder:
        return BuildOrder(
            self.pvz_build(),
            self.pvt_create_common_strategy()
        )

        # these are pvp

    def pvp_build(self) -> BuildOrder:
        return BuildOrder(
            self.pvz_build(),
            self.pvp_create_common_strategy()
        )

    def pvr_build(self) -> BuildOrder:
        return BuildOrder(
            self.pvz_build(),
            self.pvz_create_common_strategy()
        )

    def pvp_create_common_strategy(self) -> SequentialList:
        return SequentialList(
            DistributeWorkers(),
            PlanHallucination(),
            HallucinatedPhoenixScout(),
            PlanCancelBuilding(),
            WorkerRallyPoint(),
            PlanZoneGather(),
            DoubleAdeptScout(adepts_to_start=1),
            PlanZoneDefense(),
            PlanZoneAttack(),
            PlanFinishEnemy()
        )

    def pvz_create_common_strategy(self) -> SequentialList:
        return SequentialList(
            DistributeWorkers(),
            PlanHallucination(),
            HallucinatedPhoenixScout(),
            PlanCancelBuilding(),
            WorkerRallyPoint(),
            PlanZoneGather(),
            DoubleAdeptScout(adepts_to_start=1),
            PlanZoneDefense(),
            PlanZoneAttack(),
            PlanFinishEnemy()
        )

    def pvt_create_common_strategy(self) -> SequentialList:
        return SequentialList(
            DistributeWorkers(),
            PlanHallucination(),
            HallucinatedPhoenixScout(),
            PlanCancelBuilding(),
            WorkerRallyPoint(),
            PlanZoneGather(),
            DoubleAdeptScout(adepts_to_start=1),
            PlanZoneDefense(),
            PlanZoneAttack(),
            PlanFinishEnemy()
        )