import importlib
from pathlib import Path
from typing import Dict, List, Type

from src.core.base import Element
from src.core.entity import BattleEntity
from src.core.event import EventBus, AppendBuffEvent
from src.model.player import Player

event_bus = EventBus()


class Treasure(BattleEntity):
    def __init__(self, name: str, attack: int, health: int, mana_cost: Dict[Element, int],
                 buff_names: List[str] = None):
        super().__init__(name, attack, health, [])  # 初始buffs为空列表
        self.mana_cost = mana_cost
        self.owner: Player | None = None
        self.count = 1
        self.buff_names = buff_names or []  # 存储buff名称

    def contains_buff(self, buff_name):
        return any(b.name == buff_name for b in self.buffs)

    def add_buff(self, buff_name):
        from src.model.buff import BuffFactory
        buff = BuffFactory.create_buff(buff_name, self)
        self.buffs.append(buff)
        event_bus.publish(AppendBuffEvent(self, self, buff))

    def bind_owner(self, owner: Player):
        self.owner = owner
        ## 为新创建的卡牌正确添加buff ##
        for buff_name in self.buff_names:
            self.add_buff(buff_name)

    def __deepcopy__(self):
        return Treasure(self.name,
                        self.attack,
                        self.health,
                        self.mana_cost.copy(),
                        self.buff_names.copy())

    def to_dict(self):
        return {
            "name": self.name,
            "attack": self.attack,
            "mana_cost": {element.name: value for element, value in self.mana_cost.items()},
            "buffs": [b.to_dict() for b in self.buffs],
            "health": self.health,
            "id": self.id,
            "type": "treasure"
        }

    def has_buff(self, buff_name):
        return any(b.name == buff_name for b in self.buffs)

    def __str__(self):
        return f"{self.name}({self.attack}/{self.health}/{self.max_health})"


class TreasureMeta(type):
    def __new__(cls, name, bases, attrs):
        # 自动收集属性
        cost = {}
        for k in list(attrs.keys()):  # 遍历所有属性
            if k.startswith('cost_'):
                element = getattr(Element, k.split('_')[1].upper())
                cost[element] = attrs.pop(k)

        # 动态生成构造函数
        def init(self):
            Treasure.__init__(
                self,
                name=name,
                attack=attrs.get('atk', attrs.get('attack', 0)),
                health=attrs.get('hp', attrs.get('health', 0)),
                mana_cost=cost,
                buff_names=attrs.get('buffs', []),
            )
            self.count = attrs.get('count', 1)

        attrs['__init__'] = init
        bases = (Treasure,) + bases

        return super().__new__(cls, name, bases, attrs)


class CardRegistry:
    _cards = {}

    @classmethod
    def register(cls, card_class: Type):
        """ 注册方法保持不变 """
        cls._cards[card_class.__name__] = card_class
        return card_class

    @classmethod
    def auto_discover(cls, package_path: str):
        """ 自动发现卡牌类 """
        package_dir = Path(package_path)
        for py_file in package_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            module_name = py_file.stem
            full_module_path = f"{package_path.replace('/', '.')}.{module_name}"

            try:
                importlib.import_module(full_module_path)
            except Exception as e:
                print(f"加载卡牌模块失败 {full_module_path}: {str(e)}")

    @classmethod
    def create_card(cls, name: str):
        """ 增加延迟加载机制 """
        if not cls._cards:
            cls.auto_discover("model/cards")  # 指定卡牌存放目录

        if name not in cls._cards:
            raise ValueError(f"未知卡牌: {name}")
        return cls._cards[name]().__deepcopy__()


def treasure(cls):
    decorated_cls = TreasureMeta(cls.__name__, (), dict(cls.__dict__))
    CardRegistry.register(decorated_cls)
    return decorated_cls
