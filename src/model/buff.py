from src.core.base import Buff
from src.core.event import AppendBuffEvent, EventBus, CouldAttackEvent

event_bus = EventBus()

INF = 999999


class 召唤失调(Buff):
    def __init__(self, owner):
        super().__init__("召唤失调", duration=1, owner=owner)
        event_bus.subscribe(CouldAttackEvent, self.check_could_attack)

    def check_could_attack(self, event: CouldAttackEvent):
        event.prevented = True


class 突袭(Buff):
    def __init__(self, owner):
        super().__init__("突袭", duration=INF, owner=owner)
        event_bus.subscribe(AppendBuffEvent, self.on_append_buff)

    def on_append_buff(self, event: AppendBuffEvent):
        if event.buff.name == "召唤失调":
            event.prevented = True


class 行动完毕(Buff):
    def __init__(self, owner):
        super().__init__("行动完毕", duration=1, owner=owner)
        event_bus.subscribe(CouldAttackEvent, self.check_could_attack)

    def check_could_attack(self, event: CouldAttackEvent):
        event.prevented = True
