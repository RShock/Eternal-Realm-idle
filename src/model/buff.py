import inspect
import sys

from src.core.base_buff import Buff
from src.core.entity import BattleEntity
from src.core.event import AppendBuffEvent, EventBus, CouldAttackEvent, EndTurnEvent, BeforeDamageEvent, NewTurnEvent, \
    DeathEvent, AfterDamageEvent, DamageEvent
from src.core.logger import battle_logger
from src.model.basic import Treasure
from src.model.player import Player

event_bus = EventBus()

INF = 999999


class 在场(Buff):
    def __init__(self, owner):
        super().__init__("在场", owner, duration=INF, priority=-1)
        self.add_subscription(AfterDamageEvent, self.after_damage_event)
        self.add_subscription(DamageEvent, self.damage_event)

    def after_damage_event(self, event: AfterDamageEvent):
        owner: BattleEntity = self.owner
        if event.target == owner:
            if (owner.health <= 0 or owner.max_health <= 0):
                owner.add_buff("死了")
                self.on_expire()
                if isinstance(owner, Treasure):
                    battle_logger.log("destroy", f"{owner.name}被摧毁！", d_type="treasure", id=owner.id)
                    owner.owner.ally_board.remove(owner)
                if isinstance(owner, Player):
                    battle_logger.log("destroy", f"{owner.name}死亡！", d_type="player", id=owner.id)

    def damage_event(self, event: DamageEvent):
        if event.source != self.owner:
            return
        attacker = event.source
        defender = event.target
        battle_logger.log("deal_damage",
                          f"{attacker.name}对{defender.name}造成了{event.attack_deal_damage}点伤害！",
                          damage=event.attack_deal_damage, attacker_id=attacker.id, defender_id=defender.id,
                          defender_hp=defender.health)



class 死了(Buff):
    def __init__(self, owner):
        super().__init__("死了", owner, duration=INF)


class 召唤失调(Buff):
    def __init__(self, owner):
        super().__init__("召唤失调", owner, duration=1)  # 修正参数顺序
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())


class 突袭(Buff):
    def __init__(self, owner):
        super().__init__("突袭", owner, duration=INF)
        self.add_subscription(AppendBuffEvent, self.on_append_buff)

    def on_append_buff(self, event: AppendBuffEvent):
        if event.target == self.owner:
            if event.buff_name == "召唤失调":
                event.prevented = True
            if event.buff_name == "突袭":
                self.owner.remove_if_exist("召唤失调")


class 行动完毕(Buff):
    def __init__(self, owner):
        super().__init__("行动完毕", owner, duration=1)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())


class 被冻结(Buff):
    def __init__(self, owner):
        super().__init__("被冻结", owner, duration=INF)
        self.add_subscription(CouldAttackEvent, lambda e: e.attacker == self.owner and e.prevent())
        # 如果自己的回合结束+自己没有触发行动完毕 则解除冰冻
        self.add_subscription(EndTurnEvent, self._check_expire)

    def _check_expire(self, event: EndTurnEvent):
        """检查是否应该解除冰冻"""
        owner = get_player_owner(self)
        if owner == event.turn_owner and not self.owner.has_buff("行动完毕") and self.owner.has_buff("在场"):
            self.on_expire()
            battle_logger.log("remove_buff", f"{self.owner.name} 解除了冰冻", id=self.owner.id, buff_type="freeze")


class 冰冻(Buff):
    """ 冻结对其造成伤害的目标"""
    def __init__(self, owner):
        super().__init__("冰冻", owner, duration=INF)

        self.add_subscription(AfterDamageEvent, self.on_deal_damage)

    def on_deal_damage(self, event: AfterDamageEvent):
        if event.source != self.owner:
            return
        t = event.target
        if t.has_buff("被冻结"):
            return
        t.add_buff("被冻结")
        battle_logger.log("add_buff",
                          f"{self.owner.name}冻结了{t.name}",
                          source_id=self.owner.id,
                          target_id=t.id,
                          buff_type="冰冻")


class 嘲讽(Buff):
    def __init__(self, owner):
        super().__init__("嘲讽", owner, duration=INF)


class 回合开始所有法宝加buff(Buff):
    def __init__(self, owner):
        super().__init__("回合开始所有法宝加buff", owner, duration=INF)
        self.add_subscription(NewTurnEvent, self.on_turn_start)

    def on_turn_start(self, event: NewTurnEvent):
        player = None
        if isinstance(self.owner, Treasure):
            if self.owner in self.owner.owner.hand:
                return
            player = self.owner.owner
        if isinstance(self.owner, Player):
            player = self.owner
        if player != event.turn_owner:
            return
        for target in player.ally_board:
            target.attack += self.x
            target.health += self.y
            battle_logger.log("modify", f"{target.name}获得了+{self.x}/+{self.y}",
                              source_id=self.owner.id,
                              attack=target.attack,
                              health=target.health)


def get_player_owner(t: Buff):
    t = t.owner
    if isinstance(t, Treasure):
        return t.owner
    if isinstance(t, Player):
        return t


def get_opponent_board(t: Treasure | Player):
    if isinstance(t, Treasure):
        return t.owner.opponent_board
    if isinstance(t, Player):
        return t.opponent_board


class 回合结束所有法宝加buff(Buff):
    def __init__(self, owner):
        super().__init__("回合结束所有法宝加buff", owner, duration=INF)
        self.add_subscription(EndTurnEvent, self.on_turn_end)

    def on_turn_end(self, event: EndTurnEvent):
        player = None
        if isinstance(self.owner, Treasure):
            if self.owner in self.owner.owner.hand:
                return
            player = self.owner.owner
        if isinstance(self.owner, Player):
            player = self.owner
        if player != event.turn_owner:
            return
        for target in player.ally_board:
            target.attack += self.x
            target.health += self.y
            battle_logger.log("modify", f"{target.name}获得了+{self.x}/+{self.y}",
                              source_id=self.owner.id,
                              attack=target.attack,
                              health=target.health)


class 亡语随机打(Buff):
    def __init__(self, owner):
        super().__init__("亡语随机打", owner, duration=INF)
        self.add_subscription(DeathEvent, self.on_death)

    def on_death(self, event: DeathEvent):
        """当实体死亡时触发，随机选择一个目标进行攻击"""
        if event.source == self.owner:
            # 获取所有存活的目标
            alive_targets = [entity for entity in self.owner.owner.opponent.entities
                             if entity.health > 0]

            if alive_targets:
                import random
                target = random.choice(alive_targets)
                # 创建攻击事件
                attack_event = AttackEvent(self.owner, target)
                event_bus.publish(attack_event)
                battle_logger.log("亡语触发",
                                  f"{self.owner.name}死亡后随机攻击了{target.name}",
                                  source_id=self.owner.id,
                                  target_id=target.id)


# 自动收集buff类用于创建
class BuffFactory:
    _registry = {}

    @classmethod
    def _collect_buff_classes(cls):
        """自动收集当前模块中所有Buff子类"""
        current_module = sys.modules[__name__]
        for name, obj in inspect.getmembers(current_module):
            if (inspect.isclass(obj) and
                    issubclass(obj, Buff) and
                    obj != Buff and  # 排除基类本身
                    not getattr(obj, "_abstract", False)):  # 支持标记抽象类
                cls._registry[name] = obj

    @classmethod
    def create_buff(cls, name: str, owner: "BattleEntity") -> Buff:
        if not cls._registry:
            cls._collect_buff_classes()

        # 解析name中的数字
        parts = name.split('_')
        base_part = parts[0]

        # 提取base_part中的数字
        base_name = ''.join(filter(str.isalpha, base_part))
        x = int(''.join(filter(str.isdigit, base_part))) if any(c.isdigit() for c in base_part) else 0
        y = int(parts[1]) if len(parts) > 1 else 0

        if base_name not in cls._registry:
            raise ValueError(f"未知的BUFF类型: {base_name}")

        # 创建buff并设置x,y值
        buff = cls._registry[base_name](owner)
        buff.x = x
        buff.y = y
        return buff
