import json

from src.core.base import Element
from src.model.player import Player
from src.model.basic import CardRegistry
from src.system.battle_system import Battle

def test_battle():
    battle = Battle()

    p1 = Player("修真者", {Element.FIRE: 1}, 2, [], 0, battle)
    p2 = Player("魔修", {Element.WATER: 1}, 1, [], 1, battle)

    def create_card(card_name: str, owner: Player):
        card = CardRegistry.create_card(card_name)
        card.bind_owner(owner)
        return card

    # 配置测试卡组
    p1.hand = [
        create_card("火球", p1),
        create_card("水球", p1),
    ]
    p2.hand = [
        create_card("火球", p2),
        create_card("水球", p2),
    ]

    battle.add_player(p1)
    battle.add_player(p2)
    battle.start_battle()

    # 输出battle.battle_log到system\html_gen\log.json
    with open("../ui/public/log.json", "w", encoding='utf-8') as f:
        json.dump(battle.battle_log, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    test_battle()
