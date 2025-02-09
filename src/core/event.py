from collections import defaultdict
from typing import Type, Callable, Any

from src.core.base import Buff
from src.core.decorator import singleton
from src.core.entity import Entity, BattleEntity


class Event:
    """基础事件类"""

    def __init__(self):
        self.prevented = False


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

class AttackEvent(Event):
    def __init__(self, source: BattleEntity, target: BattleEntity):
        super().__init__()
        self.source = source
        self.target = target


class DamageEvent(Event):
    def __init__(self, source: BattleEntity, target: BattleEntity,
                 attack_deal_damage: int, defend_del_damage: int):
        super().__init__()
        self.source = source
        self.target = target
        self.attack_deal_damage = attack_deal_damage
        self.defend_deal_damage = defend_del_damage


class PlayCardEvent(Event):
    def __init__(self, source: BattleEntity, card):
        super().__init__()
        self.source = source
        self.card = card


class EndTurnEvent(Event):
    def __init__(self, source: BattleEntity):
        super().__init__()
        self.source = source


class EndBattleEvent(Event):
    def __init__(self, source: BattleEntity):
        super().__init__()
        self.source = source


class StartBattleEvent(Event):
    def __init__(self, source: BattleEntity):
        super().__init__()
        self.source = source


class NewTurnEvent(Event):
    def __init__(self, source: BattleEntity):
        super().__init__()
        self.source = source


class AppendBuffEvent(Event):
    def __init__(self, source: BattleEntity, target: BattleEntity, buff: Buff):
        super().__init__()
        self.source = source
        self.target = target
        self.buff = buff
        self.prevented = False


class CouldAttackEvent(Event):
    def __init__(self, source: BattleEntity):
        super().__init__()
        self.source = source
        self.prevented = False
