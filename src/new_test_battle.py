import json

from src.core.base import Element
from src.model.card import create_cards
from src.model.player import Player
from src.system.battle_system import Battle

def test_battle():
    p1 = Player("修真者", {Element.FIRE: 1}, 2, [], 0)
    p2 = Player("魔修", {Element.WATER: 1}, 1, [], 1)

    all_cards = create_cards()
    card_dict = {c.name: c for c in all_cards}

    def create_card(card_name:str, owner:Player):
        card = card_dict[card_name]
        new_card = card.__deepcopy__()
        new_card.bind_owner(owner)
        return new_card

    # 配置测试卡组
    p1.hand = [
        create_card("火球", p1),
        create_card("水球", p1),
    ]
    p2.hand = [
        create_card("火球", p2),
        create_card("水球", p2),
    ]

    battle = Battle()
    battle.add_player(p1)
    battle.add_player(p2)
    battle.start_battle()

    #     print("\n===== 最终状态 =====")
    #     print(f"{p1.name} HP: {p1.hp}")
    #     print(f"{p2.name} HP: {p2.hp}")
    #     print("战场:")
    #     print(f"{p1.name}: {p1.field}")
    #     print(f"{p2.name}: {p2.field}")
    #     print("手牌:")
    #     print(f"{p1.name}: {p1.hand}")
    #     print(f"{p2.name}: {p2.hand}")
    #
    # 输出battle.battle_log到system\html_gen\log.json
    with open("../ui/public/log.json", "w", encoding='utf-8') as f:
        json.dump(battle.battle_log, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    test_battle()