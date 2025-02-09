from src.core.base import Element
from src.model.treasure import Treasure


def create_cards():
    return [
        Treasure("火球", 1, 2, {Element.FIRE: 1}, []),
        Treasure("水球", 1, 3, {Element.WATER: 1}, []),
        # Treasure("离火剑", 3, 2, {Element.FIRE: 2}, [
        #     Effect(TriggerType.ON_ATTACK, lambda s, _: print(f"{s.name}烈焰翻腾，伤害+1"))
        # ], [突袭()]),
        # Treasure("玄武甲", 1, 5, {Element.WATER: 2}, [
        #     Effect(TriggerType.ON_DAMAGE_TAKE, lambda s, damage: setattr(s, 'health', s.health + 1))
        # ], [嘲讽()]),
        # Treasure("血神子", 4, 4, {Element.WATER: 2}, [
        #     Effect(TriggerType.ON_DAMAGE_DEAL, lambda s, damage: setattr(s.owner, 'hp', s.owner.hp + damage // 2))
        # ], [吸血()]),
        # Treasure("九幽冥火", 4, 1, {Element.FIRE: 2}, [
        #     Effect(TriggerType.ON_DEATH, lambda s: print(f"{s.name}爆发冥火，造成2点AOE伤害"))
        # ], [突袭()]),
        # Treasure("疾风剑", 4, 3, {Element.FIRE: 2}, [
        #     Effect(TriggerType.ON_ATTACK, lambda s, _: print(f"{s.name}释放疾风剑攻击"))
        # ], [疾袭(5)]),
        # # 特殊元素卡牌
        # Treasure("暗蚀珠", 2, 3, {Element.DARK: 2}, [
        #     Effect(TriggerType.ON_ATTACK,
        #            lambda s, _: print(f"{s.name}释放暗影侵蚀"))
        # ], [吸血()]),
        #
        # Treasure("雷云锁", 3, 1, {Element.THUNDER: 3}, [
        #     Effect(TriggerType.ON_DEATH,
        #            lambda s: [t.take_damage(2) for t in s.owner.opponent().field])
        # ], [疾袭(2)])
    ]

