from src.core.base_buff import Buff
from src.core.event import AppendBuffEvent, EventBus, CouldAttackEvent, AddBuffEvent

event_bus = EventBus()

INF = 999999


class 召唤失调(Buff):
    def __init__(self, owner):
        super().__init__("召唤失调", duration=1, owner=owner)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())


class 突袭(Buff):
    def __init__(self, owner):
        super().__init__("突袭", duration=INF, owner=owner)
        self.add_subscription(AppendBuffEvent, self.on_append_buff)

    def on_append_buff(self, event: AppendBuffEvent):
        if event.target == self.owner:
            if event.buff_name == "召唤失调":
                event.prevented = True
            if event.buff_name == "突袭":
                self.owner.remove_if_exist("召唤失调")

class 行动完毕(Buff):
    def __init__(self, owner):
        super().__init__("行动完毕", duration=1, owner=owner)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())



class BuffFactory:
    _registry = {
        "召唤失调": 召唤失调,
        "突袭": 突袭,
        "行动完毕": 行动完毕
    }

    @classmethod
    def create_buff(cls, name: str, owner: "BattleEntity") -> Buff:
        if name not in cls._registry:
            raise ValueError(f"未知的BUFF类型: {name}")
        return cls._registry[name](owner)