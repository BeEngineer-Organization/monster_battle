import pyxel
import random

TRANSPARENT_COLOR = 2


class BaseMonster:
    def __init__(
        self,
        u,
        v,
        w,
        h,
        name,
        type1,
        type2,
        hp,
        attack,
        defense,
        speed,
        compatibility,
    ):
        self.u, self.v, self.w, self.h = u, v, w, h
        self.name = name
        self.types = type1, type2
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.compatibility = compatibility


class Monster:
    def __init__(self, x, y, base_monster_instance, moves):
        self.x, self.y = x, y
        self.base_monster_instance = base_monster_instance
        self.moves = moves
        self.hp_now = base_monster_instance.hp

    def draw_monster(self, is_facing_right=False):
        # モンスターを描画
        if is_facing_right:
            pyxel.blt(
                self.x,
                self.y,
                0,
                self.base_monster_instance.u,
                self.base_monster_instance.v,
                self.base_monster_instance.w * (-1),
                self.base_monster_instance.h,
                TRANSPARENT_COLOR,
                scale=4,
            )
        else:
            pyxel.blt(
                self.x,
                self.y,
                0,
                self.base_monster_instance.u,
                self.base_monster_instance.v,
                self.base_monster_instance.w,
                self.base_monster_instance.h,
                TRANSPARENT_COLOR,
                scale=4,
            )

    def get_result_of_move(self, move, target):
        message = []
        if move.kind == "recover":
            # 回復技のとき
            recovery_points = round(self.base_monster_instance.hp * 0.5)
            if self.hp_now == self.base_monster_instance.hp:
                result = self.hp_now
                message.append("しかし体力は満タンだ！")
            elif self.hp_now + recovery_points > self.base_monster_instance.hp:
                # 最大HPを超えるとき
                result = self.base_monster_instance.hp
            else:
                result = self.hp_now + recovery_points

        else:
            # 攻撃技
            if move.accuracy > random.randrange(99):
                # 命中したとき
                # 技の相性
                compatibility = target.base_monster_instance.compatibility[move.type]
                if compatibility > 1:
                    message.append("効果は抜群だ！")
                elif compatibility < 1:
                    message.append("効果はいまひとつだ...")
                # ダメージ
                base_damage = round(
                    11
                    * self.base_monster_instance.attack
                    * move.power
                    * target.base_monster_instance.compatibility[move.type]
                    / (25 * target.base_monster_instance.defense)
                )
                damage = round(base_damage * random.randint(85, 100) / 100)
                if target.hp_now < damage:
                    # HPが負の値になるとき
                    result = 0
                    message.append(f"{target.base_monster_instance.name}はやられた")
                else:
                    result = target.hp_now - damage
            else:
                # 外れたとき
                result = target.hp_now
                message.append("しかし当たらなかった！")
        return result, message


class Move:
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type


class AttackMove(Move):
    def __init__(self, name, description, type, power, accuracy):
        super().__init__(name, description, type)
        self.kind = "attack"
        self.power = power
        self.accuracy = accuracy


class RecoverMove(Move):
    def __init__(self, name, description, type):
        super().__init__(name, description, type)
        self.kind = "recover"


class SelectTriangle:
    def __init__(self, base_x, base_y, delta_y, y1_max):
        self.base_x = base_x
        self.base_y = base_y
        self.delta_y = delta_y
        self.y1_max = y1_max
        self.x1 = base_x
        self.y1 = base_y
        self.x2 = base_x
        self.y2 = base_y + 12
        self.x3 = base_x + 10
        self.y3 = base_y + 6

    def reset(self, y1_max):
        self.x1 = self.base_x
        self.y1 = self.base_y
        self.x2 = self.base_x
        self.y2 = self.base_y + 12
        self.x3 = self.base_x + 10
        self.y3 = self.base_y + 6
        self.y1_max = y1_max

    def draw(self):
        pyxel.tri(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            self.x3,
            self.y3,
            0,
        )

    def select(self, is_up=False):
        if is_up:
            delta_y = self.delta_y * -1
        else:
            delta_y = self.delta_y

        if self.base_y <= self.y1 + delta_y and self.y1 + delta_y <= self.y1_max:
            self.y1 += delta_y
            self.y2 += delta_y
            self.y3 += delta_y
