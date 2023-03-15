from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.managers.extensions.build_detector import EnemyRushBuild
from sharpy.plans.protoss import *

from .build_orders.pvp.start_up import pvp_start_up
from .build_orders.pvp.counterCannonRush import counterCannonRush
from .build_orders.pvp.counterNexusFirst import counterNexusFirst
from .build_orders.pvp.counterProxyZealots import counterProxyZealots
from .build_orders.pvp.counterProxyRobo import counterProxyRobo
from .build_orders.pvp.counterProxyFourGates import counterProxyFourGates
from .build_orders.pvp.counterSingleGate import counterSingleGate
from .build_orders.pvp.MidGameMacro import pvp_mid_game_macro
from .build_orders.pvp.LateGameMacro import pvp_late_game_macro

from .build_orders.pvz.start_up import pvz_start_up
from .build_orders.pvz.counter_12d import counter12Pool
from .build_orders.pvz.counter_ling_rush import counterLingRush
from .build_orders.pvz.counterRoachRush import counterRoachRush
from .build_orders.pvz.LateGameMacro import pvz_late_game_macro


from .build_orders.pvt.start_up import pvt_start_up
from .build_orders.pvt.LateGameMacro import pvt_late_game_macro
from .build_orders.pvt.fourgates import pvt_fourgates
from .build_orders.pvt.MidGameMacro import pvt_mid_game_micro


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
        return await super().on_step(iteration)

    def pvp_build(self) -> BuildOrder:
        return BuildOrder(
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Start, pvp_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.WorkerRush, counterProxyZealots()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.CannonRush, counterCannonRush()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.NexusFirst, counterNexusFirst()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.SingleGate, counterSingleGate()),

            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyZealots, counterProxyZealots()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyRobo, counterProxyRobo()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyVoid, counterNexusFirst()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyFourGate, counterProxyFourGates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PotentialProxy, counterProxyFourGates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.RoboExpand, pvp_mid_game_macro()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.StargateExpand, pvp_mid_game_macro()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.TwilightExpand, pvp_mid_game_macro()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVPMidGameMacro, pvp_mid_game_macro()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVPLateGameMacro, pvp_late_game_macro()),

        )


    def pvt_build(self) -> BuildOrder:
        return BuildOrder(
            #Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Start, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Start, pvt_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyTwoRaxMarine, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.WorkerRush, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyThreeRaxMarine, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyReaper, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ProxyMarauders, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.OneBaseTech, pvt_fourgates()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.ThreeRaxStim, pvt_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.RaxFactPort, pvt_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVTMidGameMacro, pvt_mid_game_micro()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVTLateGameMacro, pvt_late_game_macro()),
        )

    def pvz_build(self) -> BuildOrder:
        return BuildOrder(
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Start, pvz_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.WorkerRush, counter12Pool()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Pool12, counter12Pool()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.Pool17, counterLingRush()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.RoachRush, counterRoachRush()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.LingBaneRush, counterLingRush()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVZMidGameMacro, pvz_start_up()),
            Step(lambda k: k.build_detector.rush_build == EnemyRushBuild.PVZLateGameMacro, pvz_late_game_macro()),
        )

    def pvr_build(self) -> BuildOrder:
        return self.pvp_build()
