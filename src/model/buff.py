from src.core.base_buff import Buff
from src.core.event import AppendBuffEvent, EventBus, CouldAttackEvent

event_bus = EventBus()

INF = 999999


class 召唤失调(Buff):
    def __init__(self, owner):
        super().__init__("召唤失调", duration=1, owner=owner)
        self.subscribe_events()

    def subscribe_events(self):
        # 使用统一的方法添加订阅
        self.add_subscription(CouldAttackEvent, self.check_could_attack)
        event_bus.subscribe(CouldAttackEvent, self.check_could_attack)

    def check_could_attack(self, event: CouldAttackEvent):
        # 添加有效性检查
        if self.duration <= 0:
            return
        if event.attacker == self.owner:
            event.prevented = True



class 突袭(Buff):
    def __init__(self, owner):
        super().__init__("突袭", duration=INF, owner=owner)
        event_bus.subscribe(AppendBuffEvent, self.on_append_buff)

    def on_append_buff(self, event: AppendBuffEvent):
        if event.buff.name == "召唤失调":
            event.prevented = True
        self.owner.remove_if_exist("召唤失调")


class 行动完毕(Buff):
    def __init__(self, owner):
        super().__init__("行动完毕", duration=1, owner=owner)
        event_bus.subscribe(CouldAttackEvent, self.check_could_attack)

    def check_could_attack(self, event: CouldAttackEvent):
        event.prevented = True
