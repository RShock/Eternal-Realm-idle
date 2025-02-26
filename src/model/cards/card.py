from src.model import basic
from src.model.basic import treasure
from src.model.buff import 突袭


@treasure
class 水球:
    atk = 1
    hp = 3
    cost_water = 1
    buffs = ["冰冻"]


@treasure
class 火球:
    atk = 1
    hp = 5
    cost_fire = 1
    buffs = ["突袭"]


@treasure
class 铁精镖:
    atk = 3
    hp = 2
    cost_gold = 1


@treasure
class 荆棘索:
    atk = 2
    hp = 3
    cost_wood = 1


@treasure
class 雾隐珠:
    atk = 1
    hp = 4
    cost_water = 1


@treasure
class 爆炎石:
    atk = 4
    hp = 1
    cost_fire = 1


@treasure
class 岩甲符:
    atk = 0
    hp = 5
    cost_earth = 1
    

@treasure
class 玄铁刃:
    atk = 3
    hp = 3
    cost_gold = 1
    buffs = ["回合开始所有法宝加buff1_1"]


@treasure
class 百草囊:
    atk = 2
    hp = 4
    cost_wood = 1
    buffs = ["回合结束所有法宝加buff0_1"]


@treasure
class 寒泉佩:
    atk = 3
    hp = 4
    cost_water = 1
    buffs = ["冻结"]


@treasure
class 赤硝火筒:
    atk = 5
    hp = 1
    cost_fire = 1
    buffs = ["亡语随机打3"]

@treasure
class 石肤符:
    atk = 0
    hp = 12
    cost_earth = 1
    buffs = ["嘲讽"]


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
