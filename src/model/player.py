import json
from typing import Dict, List, TYPE_CHECKING

from src.core.base import Element
from src.core.base_buff import Buff
from src.core.entity import BattleEntity

if TYPE_CHECKING:
    from src.system.battle_system import Battle


class Player(BattleEntity):

    def __init__(self, name: str, base_mana: Dict[Element, int], speed: int, buffs: List[Buff], part,
                 battle_ground: "Battle"):
        super().__init__(name, 0, 2, buffs)
        self.speed = speed
        self.mana = base_mana
        from src.model.basic import Treasure
        self.hand: List["Treasure"] = []
        self.part = part
        self.battle_ground = battle_ground

    def to_dict(self):
        return {
            "name": self.name,
            "attack": self.attack,
            "mana": {element.name: value for element, value in self.mana.items()},
            "speed": self.speed,
            "buffs": [b.to_dict() for b in self.buffs],
            "health": self.health,
            "id": self.id,
            "type": "player",
            "part": "ally" if self.part == 0 else "enemy"
        }

    def add_buff(self, param):
        from src.model.buff import BuffFactory
        buff = BuffFactory.create_buff(param, self)
        self.buffs.append(buff)

    def __str__(self):
        return f"{self.name}{self.health}/{self.max_health})"

    @property
    def ally_board(self):
        return self.battle_ground.field[self.part]
