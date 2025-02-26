import inspect
import sys

from src.core.base_buff import Buff
from src.core.event import AppendBuffEvent, EventBus, CouldAttackEvent, EndTurnEvent, DamageEvent, NewTurnEvent
from src.core.logger import battle_logger
from src.model.basic import Treasure
from src.model.player import Player

event_bus = EventBus()

INF = 999999


class 召唤失调(Buff):
    def __init__(self, owner):
        super().__init__("召唤失调", owner, duration=1)  # 修正参数顺序
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())


class 突袭(Buff):
    def __init__(self, owner):
        super().__init__("突袭", owner, duration=INF)
        self.add_subscription(AppendBuffEvent, self.on_append_buff)

    def on_append_buff(self, event: AppendBuffEvent):
        if event.target == self.owner:
            if event.buff_name == "召唤失调":
                event.prevented = True
            if event.buff_name == "突袭":
                self.owner.remove_if_exist("召唤失调")


class 行动完毕(Buff):
    def __init__(self, owner):
        super().__init__("行动完毕", owner, duration=1)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())


class 被冻结(Buff):
    def __init__(self, owner):
        super().__init__("被冻结", owner, duration=INF)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())
        # 如果自己的回合结束+自己没有触发行动完毕 则解除冰冻
        self.add_subscription(EndTurnEvent, self._check_expire)

    def _check_expire(self, event: EndTurnEvent):
        """检查是否应该解除冰冻"""
        if self.owner.owner == event.turn_owner and not self.owner.contains_buff("行动完毕"):
            self.on_expire()
            battle_logger.log("解除冻结", f"{self.owner.name} 被解除了冰冻")


class 冰冻(Buff):
    """ 冻结对其造成伤害的目标"""

    def __init__(self, owner):
        super().__init__("冰冻", owner, duration=INF)

        self.add_subscription(DamageEvent, self.on_deal_damage)

    def on_deal_damage(self, event: DamageEvent):
        if event.source == self.owner:
            event.target.add_buff("被冻结")
            battle_logger.log("freeze",
                              f"{self.owner.name}冻结了{event.target.name}",
                              source_id=self.owner.id,
                              target_id=event.target.id)
        if event.target == self.owner:
            event.source.add_buff("被冻结")
            battle_logger.log("freeze",
                              f"{self.owner.name}冻结了{event.source.name}",
                              source_id=self.owner.id,
                              target_id=event.source.id)


class 嘲讽(Buff):
    def __init__(self, owner):
        super().__init__("嘲讽", owner, duration=INF)


class 回合开始所有法宝加buff(Buff):
    def __init__(self, owner):
        super().__init__("回合开始所有法宝加buff", owner, duration=INF)
        self.add_subscription(NewTurnEvent, self.on_turn_start)

    def on_turn_start(self, event: NewTurnEvent):
        player = None
        if isinstance(self.owner, Treasure):
            if self.owner in self.owner.owner.hand:
                return
            player = self.owner.owner
        if isinstance(self.owner, Player):
            player = self.owner
        if player != event.turn_owner:
            return
        for target in player.ally_board:
            target.attack += self.x
            target.health += self.y
            battle_logger.log("modify", f"{target.name}获得了+{self.x}/+{self.y}",
                              source_id=self.owner.id,
                              attack=target.attack,
                              health=target.health)

    # 自动收集buff类用于创建


class BuffFactory:
    _registry = {}

    @classmethod
    def _collect_buff_classes(cls):
        """自动收集当前模块中所有Buff子类"""
        current_module = sys.modules[__name__]
        for name, obj in inspect.getmembers(current_module):
            if (inspect.isclass(obj) and
                    issubclass(obj, Buff) and
                    obj != Buff and  # 排除基类本身
                    not getattr(obj, "_abstract", False)):  # 支持标记抽象类
                cls._registry[name] = obj

    @classmethod
    def create_buff(cls, name: str, owner: "BattleEntity") -> Buff:
        if not cls._registry:
            cls._collect_buff_classes()

        # 解析name中的数字
        parts = name.split('_')
        base_part = parts[0]

        # 提取base_part中的数字
        base_name = ''.join(filter(str.isalpha, base_part))
        x = int(''.join(filter(str.isdigit, base_part))) if any(c.isdigit() for c in base_part) else 0
        y = int(parts[1]) if len(parts) > 1 else 0

        if base_name not in cls._registry:
            raise ValueError(f"未知的BUFF类型: {base_name}")

        # 创建buff并设置x,y值
        buff = cls._registry[base_name](owner)
        buff.x = x
        buff.y = y
        return buff
