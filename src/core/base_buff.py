from src.core.event import EventBus, CouldAttackEvent
from src.core.logger import battle_logger
from typing import TYPE_CHECKING

event_bus = EventBus()
if TYPE_CHECKING:
    from src.core.entity import BattleEntity


class BuffMeta(type):
    """元类用于自动记录所有Buff子类"""

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        # 跳过基类Buff本身
        if name != "Buff" and issubclass(cls, Buff):
            # 确保每个Buff类都有唯一的名称
            if hasattr(cls, "_registry"):
                cls._registry[name] = cls


class Buff(metaclass=BuffMeta):

    def __init__(self, name: str, owner: "BattleEntity", duration: int = -1, x: int = 0, y: int = 0, priority=1):

        self.name = name
        self._duration = duration  # 改用私有变量配合属性访问器
        self.x = x
        self.y = y
        # 订阅记录需要独立存储
        self._event_subscriptions = []
        self.owner = owner
        self.priority = priority

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        # 当持续时间改变时自动检查失效
        old_value = self._duration
        self._duration = value
        if old_value > 0 and value <= 0:
            self.on_expire()

    def on_expire(self):
        """持续时间耗尽时触发"""
        self._duration = -1
        self.owner.buffs.remove(self)
        self.unsubscribe_all()

    def unsubscribe_all(self):
        """移除所有事件监听"""
        for event_type, handler in self._event_subscriptions:
            event_bus.unsubscribe(event_type, handler)
        self._event_subscriptions.clear()

    def add_subscription(self, event_type, handler):
        """记录事件订阅"""

        def wrapped_handler(*args, **kwargs):
            # 在调用原handler前进行条件判断
            if self.duration <= 0:
                return
            return handler(*args, **kwargs)

        self._event_subscriptions.append((event_type, wrapped_handler))

        event_bus.subscribe(event_type, wrapped_handler, self.priority)

    # 更改to str
    def __repr__(self):
        return f"【{self.name}】"

    def to_dict(self):
        return {
            "name": self.name,
            "x": self.x}

    def __deepcopy__(self, memo):
        new_buff = self.__class__(self.name, self.owner, self._duration, self.x)
        # 不复制_event_subscriptions，同一个buff共用一个subscriptions
        return new_buff
