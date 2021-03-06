from typing import Union, Optional

from sc2.ids.ability_id import AbilityId
from sc2.position import Point2, Pointlike
from sc2.unit import Unit
from sc2.unit_command import UnitCommand


class Action:
    target: Union[Point2, Unit]
    is_attack: bool

    def __init__(
        self,
        target: Optional[Union[Point2, Pointlike, Unit]],
        is_attack: bool,
        ability: Optional[AbilityId] = None,
        debug_comment: Optional[str] = None,
    ):

        self.target = target
        self.is_attack = is_attack
        self.ability = ability
        self.is_final = False
        self.debug_comment = debug_comment

    def to_commmand(self, unit: Unit) -> bool:
        if self.ability is not None:
            action = unit(self.ability, self.target)
        elif self.is_attack:
            action = unit.attack(self.target)
        else:
            action = unit.move(self.target)
        return action

    @property
    def position(self) -> Optional[Point2]:
        if self.target is None:
            return None
        if isinstance(self.target, Point2):
            return self.target

        return self.target.position


class NoAction(Action):
    def __init__(self):
        super().__init__(None, False)

    def to_commmand(self, unit: Unit) -> bool:
        return False
