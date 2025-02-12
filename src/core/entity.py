from typing import List

from src.core.decorator import IDComponent
from src.core.base import Buff


class Entity:
    def __init__(self):
        self._id_component = IDComponent()

    @property
    def id(self):
        return str(self._id_component.id)
        # return self._id_component.id
class BattleEntity(Entity):
    def __init__(self, name: str, attack: int, health: int, buffs: List[Buff] = None):
        super().__init__()
        self.name = name
        self.attack = attack
        self.health = health
        self.max_health = health
        self.buffs = buffs or []
