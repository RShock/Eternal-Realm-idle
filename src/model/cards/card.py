from src.model import basic
from src.model.basic import treasure
from src.model.buff import 突袭


@treasure
class 水球:
    atk = 1
    hp = 3
    cost_water = 1

@treasure
class 火球:
    atk = 1
    hp = 2
    cost_fire = 1
    buffs = ["突袭"]

@treasure
class 青竹蜂云剑〇残:
    atk = 1
    hp = 1
    cost_wood = 12
    count = 12

@treasure
class 青竹蜂云剑〇残2:
    atk = 1
    hp = 1
    cost_wood = 24
    count = 24

@treasure
class 硫火雷筒:
    level = "炼气后期"
    atk = 12
    hp = 1
    cost_fire = 2
    cost_normal = 1
    rush = True