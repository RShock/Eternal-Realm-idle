from src.models.base import Element
from src.models.cards import create_cards
from src.models.core import Player, Battle
from src.utils.visualization import create_frame

frames = []
def test_battle():
    p1 = Player("修真者", {Element.FIRE: 1})
    p2 = Player("魔修", {Element.WATER: 1})

    all_cards = create_cards()
    card_dict = {c.name: c for c in all_cards}

    # 配置测试卡组
    p1.hand = [
        card_dict["火灵根"],
        card_dict["离火剑"],
        card_dict["九幽冥火"]
    ]
    p2.hand = [
        card_dict["水灵根"],
        card_dict["玄武甲"],
        card_dict["血神子"]
    ]

    battle = Battle(p1, p2)

    # 模拟3回合
    for _ in range(15):
        print(f"\n=== 第{battle.turn + 1}回合 ===")
        battle.new_turn()
        current = battle.current_player()

        # 出牌阶段
        if current.hand:
            card = current.hand[0]
            if battle.play_card(card):
                current.hand.pop(0)
                print(f"pop card {card.name}")

        # 攻击阶段
        battle.auto_attack()

        print("\n===== 最终状态 =====")
        print(f"{p1.name} HP: {p1.hp}")
        print(f"{p2.name} HP: {p2.hp}")
        print("战场:")
        print(f"{p1.name}: {p1.field}")
        print(f"{p2.name}: {p2.field}")
        print("手牌:")
        print(f"{p1.name}: {p1.hand}")
        print(f"{p2.name}: {p2.hand}")

        frame = create_frame(p1, p2, battle, battle.turn)
        frames.append(frame)
    import os

    # 创建GIF并保存
    frames[0].save('battle_result.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)

    # 打开生成的GIF
    if os.name == 'posix':  # Linux/MacOS
        os.system('xdg-open battle_result.gif')
    else:  # Windows
        os.system('start battle_result.gif')


if __name__ == "__main__":
    test_battle()