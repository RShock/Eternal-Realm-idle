import unittest
from src.models.core import Player, Battle, Treasure, DamageEvent
from src.models.buffs import 疾袭, 吸血, 嘲讽, 召唤失调, 突袭
from src.models.base import TriggerType


class TestBuffs(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("测试玩家1", {})
        self.p2 = Player("测试玩家2", {})
        self.battle = Battle(self.p1, self.p2)

    def test_swift_attack_priority(self):
        battle = Battle(Player("p1", {}), Player("p2", {}))

        # 配置带疾袭5的攻击方
        swift_attacker = Treasure("疾袭者", 3, 5, {}, [], [疾袭(5)])
        defender = Treasure("普通", 3, 3, {}, [], [])

        swift_attacker.bind_battle(battle)
        defender.bind_battle(battle)

        # 攻击方先攻
        battle.players[0].field = [swift_attacker]
        battle.players[1].field = [defender]

        battle.auto_attack()

        # 验证攻击顺序和结果
        assert defender.health == 0
        assert swift_attacker.health == 5
    def test_lifesteal(self):
        attacker = Treasure("吸血测试", 5, 5, {}, [], [吸血()])
        attacker.owner = self.p1
        damage_event = DamageEvent(attacker, self.p2, 5)
        self.battle.trigger_event(TriggerType.ON_DAMAGE_DEAL, damage_event)
        self.assertEqual(self.p1.hp, 35)

    def test_taunt_targeting(self):
        taunt = Treasure("嘲讽者", 1, 5, {}, [], [嘲讽()])
        normal = Treasure("普通", 1, 5, {}, [], [])
        self.p2.field = [taunt, normal]
        attacker = Treasure("攻击者", 3, 5, {}, [], [])
        defender = self.battle._select_defender(attacker)
        self.assertIs(defender, taunt)

    def test_summon_sickness(self):
        sick = Treasure("失调", 3, 5, {}, [], [召唤失调()])
        self.p1.field = [sick]
        self.assertFalse(sick.can_attack())

    def test_surprise_attack(self):
        surge = Treasure("突袭者", 3, 5, {}, [], [突袭()])
        self.p1.field = [surge]
        self.p2.field = []
        defender = self.battle._select_defender(surge)
        self.assertIsNone(defender)


if __name__ == "__main__":
    unittest.main()
