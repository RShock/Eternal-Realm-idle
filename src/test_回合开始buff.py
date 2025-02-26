import unittest
from src.core.base import Element
from src.model.player import Player
from src.model.basic import CardRegistry
from src.system.battle_system import Battle

class TestMetalVsEarth(unittest.TestCase):
    def setUp(self):
        self.battle = Battle()

        # 创建玩家
        self.p1 = Player("修真者", {Element.GOLD: 2}, 2, [], 0, self.battle)  # 我方，2点金法术力
        self.p2 = Player("魔修", {Element.EARTH: 2, Element.WOOD: 2}, 1, [], 1, self.battle)    # 对方，2点土法术力

        # 创建卡牌
        def create_card(card_name: str, owner: Player):
            card = CardRegistry.create_card(card_name)
            card.bind_owner(owner)
            return card

        # 配置手牌
        self.p1.hand = [
            create_card("玄铁刃", self.p1),
            create_card("玄铁刃", self.p1)
        ]
        self.p2.hand = [
            create_card("百草囊", self.p2),
            create_card("百草囊", self.p2)
        ]

        # 创建战斗
        self.battle.add_player(self.p1)
        self.battle.add_player(self.p2)

    def test_turn(self):
        self.battle.start_battle()

if __name__ == "__main__":
    unittest.main()