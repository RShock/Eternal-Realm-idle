from typing import Dict, List

from src.core.base import Element, Buff
from src.core.entity import BattleEntity
from src.model.player import Player


class Treasure(BattleEntity):
    def __init__(self, name: str, attack: int, health: int, mana_cost: Dict[Element, int],
                 buffs: List[Buff] = None):
        super().__init__(name, attack, health, buffs)
        self.mana_cost = mana_cost
        self.owner = None
        self.destroyed = False

    def contains_buff(self, buff_name):
        return any(b.name == buff_name for b in self.buffs)

    def bind_owner(self, owner: Player):
        self.owner = owner

    def __deepcopy__(self):
        return Treasure(self.name, self.attack, self.health, self.mana_cost.copy(), self.buffs.copy())

    def to_dict(self):
        return {
            "name": self.name,
            "attack": self.attack,
            "mana_cost": {element.name: value for element, value in self.mana_cost.items()},
            "destroyed": self.destroyed,
            "buffs": [b.to_dict() for b in self.buffs],
            "health": self.health,
            "id": self.id,
            "type": "treasure"
        }
