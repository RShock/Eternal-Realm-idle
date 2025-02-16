import json
from enum import Enum


class ElementEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Element):
            return obj.value  # 使用Enum的value属性
        return super().default(obj)
class Element(Enum):
    GOLD = "金"
    WOOD = "木"
    WATER = "水"
    FIRE = "火"
    EARTH = "土"
    DARK = "暗"
    MAGNET = "磁"
    ICE = "冰"
    THUNDER = "雷"
    NORMAL = "无"

    @classmethod
    def elemental_cycle(cls):
        """获取基础五行元素"""
        return [cls.GOLD, cls.WOOD, cls.WATER, cls.FIRE, cls.EARTH]

from typing import Dict

def compare_dicts(A: Dict, B: Dict) -> bool:
    for key, value in A.items():
        # 如果B中不包含A的元素或者A的元素值大于B的值，则返回False
        if key not in B or B[key] < value:
            return False
    return True


