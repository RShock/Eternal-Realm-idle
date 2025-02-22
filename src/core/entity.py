from typing import List

from src.core.decorator import IDComponent
from src.core.base_buff import Buff
from abc import ABC, abstractmethod


class Entity():
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

    def remove_if_exist(self, buff_name):
        for b in self.buffs:
            if b.name == buff_name:
                self.buffs.remove(b)
                b.on_expire()
                return
        self.buffs = [b for b in self.buffs if b.name != buff_name]

    def add_buff(self, param):
        raise NotImplementedError
