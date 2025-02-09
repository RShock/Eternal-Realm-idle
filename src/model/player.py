import json
from typing import Dict, List

from src.core.base import Element, Buff
from src.core.entity import BattleEntity


class Player(BattleEntity):
    def __init__(self, name: str, base_mana: Dict[Element, int], speed: int, buffs: List[Buff], part):
        super().__init__(name, 0, 2, buffs)
        self.speed = speed
        self.mana = base_mana
        self.hand: List["Treasure"] = []
        self.part = part
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

    # def can_play(self, card: Treasure) -> bool:
    #     return (
    #             not self.played_this_turn and
    #             all(self.mana[e] >= req for e, req in card.mana_cost.items())
    #     )

