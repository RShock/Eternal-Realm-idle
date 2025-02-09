# src/views/battle_view.py
from src.core.architecture import EventBus


class BattleView:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._register_handlers()

    def _register_handlers(self):
        self.event_bus.subscribe(HealthChangeEvent, self.update_health_display)
        self.event_bus.subscribe(CardPlayedEvent, self.update_card_display)

    def update_health_display(self, event: HealthChangeEvent):
        # 更新生命值显示
        pass

    def update_card_display(self, event: CardPlayedEvent):
        # 更新卡牌显示
        pass
