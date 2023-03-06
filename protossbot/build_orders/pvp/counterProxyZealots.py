from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Race
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *


def counterProxyZealots() -> BuildOrder:
    return BuildOrder(
        AutoWorker(),
        AutoPylon(),

        ChronoUnit(UnitTypeId.STALKER, UnitTypeId.GATEWAY, 10),

        Tech(UpgradeId.WARPGATERESEARCH),
        Step(UnitExists(UnitTypeId.STALKER, 5),
             GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=4, priority=True)),
        Step(UnitExists(UnitTypeId.CYBERNETICSCORE),
             GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=3, priority=True)),

        ProtossUnit(UnitTypeId.STALKER, to_count=3, priority=True),
        ProtossUnit(UnitTypeId.ADEPT, priority=True, to_count=6),
        DoubleAdeptScout(6),

        ProtossUnit(UnitTypeId.STALKER, priority=True),
        GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=1, priority=True),
        GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
        BuildGas(2),
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
