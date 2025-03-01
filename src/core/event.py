from collections import defaultdict
from typing import Type, Callable, TYPE_CHECKING

from src.core.decorator import singleton

if TYPE_CHECKING:
    from src.core.entity import BattleEntity


class Event:
    """基础事件类"""

    def __init__(self):
        self.prevented = False

    def prevent(self):
        self.prevented = True


@singleton
class EventBus:
    """事件总线"""

    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable, priority=0):
        self._handlers[event_type].append((priority, handler))
        self._handlers[event_type].sort(reverse=True, key=lambda x: x[0])

    def publish(self, event: Event):
        handlers = self._handlers.get(type(event), [])
        for _, handler in handlers:
            handler(event)
            if event.prevented:
                break
        return event

    def unsubscribe(self, event_type, handler):
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)


class AttackEvent(Event):
    def __init__(self, source: "BattleEntity", target: "BattleEntity"):
        super().__init__()
        self.source = source
        self.target = target


class BeforeDamageEvent(Event):
    def __init__(self, source: "BattleEntity", target: "BattleEntity",
                 attack_deal_damage: int, defend_del_damage: int):
        super().__init__()
        self.source = source
        self.target = target
        self.attack_deal_damage = attack_deal_damage
        self.defend_deal_damage = defend_del_damage


class PlayCardEvent(Event):
    def __init__(self, source: "BattleEntity", card):
        super().__init__()
        self.source = source
        self.card = card


class EndTurnEvent(Event):
    def __init__(self, turn_owner: "BattleEntity", turn: int):
        super().__init__()
        self.turn_owner = turn_owner
        self.turn = turn


class DeathEvent(Event):
    def __init__(self, death: "BattleEntity", causer: "BattleEntity"):
        super().__init__()
        self.death = death
        self.causer = causer


class EndBattleEvent(Event):
    def __init__(self, source: "BattleEntity"):
        super().__init__()
        self.source = source


class StartBattleEvent(Event):
    def __init__(self, source: "BattleEntity"):
        super().__init__()
        self.source = source


class NewTurnEvent(Event):
    def __init__(self, turn: int, owner):
        super().__init__()
        self.turn = turn
        self.turn_owner = owner


class AppendBuffEvent(Event):
    def __init__(self, source: "BattleEntity", target: "BattleEntity", buff_name):
        super().__init__()
        self.source = source
        self.target = target
        self.buff_name = buff_name


class CouldAttackEvent(Event):
    def __init__(self, attacker: "BattleEntity"):
        super().__init__()
        self.attacker = attacker


class DeathEvent(Event):
    def __init__(self, source: "BattleEntity"):
        super().__init__()
        self.source = source


class AfterDamageEvent(Event):
    def __init__(self, source: "BattleEntity", target: "BattleEntity",
                 attack_deal_damage: int):
        super().__init__()
        self.source = source
        self.target = target
        self.attack_deal_damage = attack_deal_damage


class DamageEvent(Event):
    def __init__(self, source: "BattleEntity", target: "BattleEntity",
                 attack_deal_damage: int):
        super().__init__()
        self.source = source
        self.target = target
        self.attack_deal_damage = attack_deal_damage
