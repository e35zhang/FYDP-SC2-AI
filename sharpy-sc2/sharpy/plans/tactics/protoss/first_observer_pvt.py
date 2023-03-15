from sc2.unit import Unit
from sharpy.plans.acts import ActBase
from sharpy.managers.core.roles import UnitTask
from sharpy.knowledges import Knowledge
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
import random


class First_Observer_PVT(ActBase):
    def __init__(self):
        super().__init__()
        self.first_ob_tag = None
        self.reached_position = False
        self.ended = False

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)

    async def execute(self) -> bool:
        if self.ended:
            return True

        observers = self.knowledge.unit_cache.own(UnitTypeId.OBSERVER).ready
        position = self.get_first_ob_position()
        if self.first_ob_tag is None:
            if observers.amount == 1:
                self.knowledge.roles.set_task(UnitTask.Reserved, observers.first)
                self.first_ob_tag = observers.first.tag
                self.roles.refresh_tasks(observers)
        else:
            observer: Unit = self.knowledge.unit_cache.by_tag(self.first_ob_tag)
            if observer is not None:
                self.knowledge.roles.set_task(UnitTask.Reserved, observer)
                first_observer = observers.filter(lambda unit: unit.tag == observer.tag)
                self.roles.refresh_tasks(first_observer)

        if not self.reached_position:
            observer: Unit = self.knowledge.unit_cache.by_tag(self.first_ob_tag)
            if observer is not None:
                if observer.distance_to(position) <= 1:
                    self.reached_position = True
                    observer(AbilityId.MORPH_SURVEILLANCEMODE)
                else:
                    observer.move(position)
            else:
                self.ended = True

        return True  # never block

    def get_first_ob_position(self):
        return self.knowledge.zone_manager.enemy_expansion_zones[1].center_location. \
            towards(self.knowledge.zone_manager.our_zones[1].center_location, 22)
