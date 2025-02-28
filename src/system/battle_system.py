import random
from typing import Dict

from src.core.base import compare_dicts, Element
from src.core.entity import BattleEntity
from src.core.event import EventBus, PlayCardEvent, CouldAttackEvent, AttackEvent, BeforeDamageEvent, AppendBuffEvent, \
    EndTurnEvent, NewTurnEvent, AfterDamageEvent, DamageEvent
from src.core.logger import JSONLogHandler, ConsoleLogHandler
from src.model.buff import 召唤失调
from src.model.player import Player
from src.model.basic import Treasure
from src.core.logger import battle_logger 

event_bus = EventBus()


class Battle:
    def __init__(self):
        self.players: list[Player] = []
        self.field: list[list[Treasure]] = [[], []]
        self.turn = 0
        self.battle_log = []
        battle_logger.add_handler(JSONLogHandler(self.battle_log))
        battle_logger.add_handler(ConsoleLogHandler())
        event_bus.subscribe(AttackEvent, self.register_event_attack)

    def add_player(self, player: Player):
        self.players.append(player)
        battle_logger.log("add_player", f"玩家{player.name}加入战斗", player=player.to_dict())

    def start_battle(self):
        self.players.sort(key=lambda p: (-p.speed, random.random()))
        current_player_index = 0
        while True:
            current_player = self.players[current_player_index]
            if current_player.health <= 0:
                current_player_index = (current_player_index + 1) % len(self.players)
                continue
            self.new_turn()
            if self.turn >= 10:
                battle_logger.log("end", "战斗结束，回合数已达上限")
                break
            battle_logger.log("new_turn", f"第{self.turn}回合开始了，当前玩家是{current_player.name}", turn=self.turn,
                      current_player_id=current_player.id)
            event_bus.publish(NewTurnEvent(self.turn, current_player))

            while self.play_card(current_player):
                pass
            self.auto_attack(current_player)
            if self._check_end():
                break
            current_player_index = (current_player_index + 1) % len(self.players)
            event_bus.publish(EndTurnEvent(current_player, self.turn))

    def _check_end(self) -> bool:
        return any(p.health <= 0 for p in self.players)

    def new_turn(self):
        self.turn += 1

        # buff消退
        for p in (self.players + self.field[0] + self.field[1]):
            # expired_indices = []
            for i, buff in enumerate(p.buffs):
                if buff.duration > 0:
                    buff.duration -= 1

    def play_card(self, player: Player) -> bool:
        card: Treasure = next((c for c in player.hand if compare_dicts(c.mana_cost, player.mana)), None)
        if not card:
            return False
        battle_logger.log("play_card", f"{player.name}打出了{card.name}", player_id=player.id, card=card.to_dict(),
                  part="ally" if player.part == 0 else "enemy")

        player.hand.remove(card)
        self.field[player.part].append(card)
        card.add_buff("在场")
        card.owner = player
        if not event_bus.publish(AppendBuffEvent(card, card, "召唤失调")).prevented:
            card.buffs.append(召唤失调(card))

        for e, v in card.mana_cost.items():
            player.mana[e] += v
        event_bus.publish(PlayCardEvent(player, card))
        return False

    def _format_mana(self, mana: Dict[Element, int]) -> str:
        """格式化显示灵力"""
        return " ".join(f"{v}{e.value}" for e, v in mana.items())

    def auto_attack(self, attacker: Player):
        def check_attackable(t1: Treasure):
            if t1.has_buff("死亡"):
                return False
            event = CouldAttackEvent(t1)
            event_bus.publish(event)
            return not event.prevented

        def find_enemy(player):
            return next((p for p in self.players if p != player and p.part != player.part), None)

        our_field = self.field[attacker.part]
        enemy_field = self.field[attacker.part ^ 1]

        tmp_field = [e for e in enemy_field if e.has_buff("在场")]
        # 随机化
        random.shuffle(tmp_field)
        for t in our_field:
            if check_attackable(t):
                t.add_buff("行动完毕")
                if len(tmp_field) == 0:  # 直接攻击
                    event_bus.publish(AttackEvent(t, find_enemy(attacker)))
                    return
                for t2 in tmp_field:
                    if t2.contains_buff("嘲讽"):  # 嘲讽
                        event_bus.publish(AttackEvent(t, t2))
                        return
                event_bus.publish(AttackEvent(t, tmp_field[0]))  # 随机攻击某一个法宝
                return

    def register_event_attack(self, event: AttackEvent):
        attacker, defender = event.source, event.target
        dmg_event = BeforeDamageEvent(attacker, defender, attacker.attack, defender.attack)
        event_bus.publish(dmg_event)
        if not dmg_event.prevented:
            battle_logger.log("attack", f"{attacker.name}攻击了{defender.name}", attacker_id=attacker.id,
                              defender_id=defender.id)
            if dmg_event.attack_deal_damage > 0:
                defender.health -= dmg_event.attack_deal_damage
                event_bus.publish(DamageEvent(attacker, defender, dmg_event.attack_deal_damage))

            if dmg_event.defend_deal_damage > 0:
                attacker.health -= dmg_event.defend_deal_damage
                event_bus.publish(DamageEvent(attacker, defender, dmg_event.attack_deal_damage))

            if dmg_event.attack_deal_damage > 0:
                event_bus.publish(AfterDamageEvent(attacker, defender, dmg_event.attack_deal_damage))

            if dmg_event.defend_deal_damage > 0:
                event_bus.publish(AfterDamageEvent(defender, attacker, dmg_event.defend_deal_damage))
