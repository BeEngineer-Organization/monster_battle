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
        type,
        hp,
        attack,
        defense,
        speed,
        compatibility,
        moves,
    ):
        self.u, self.v, self.w, self.h = u, v, w, h
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.compatibility = compatibility
        self.moves = moves


class Monster:
    def __init__(self, x, y, base_monster_instance, win_count=0):
        self.x, self.y = x, y
        self.base_monster_instance = base_monster_instance
        self.hp_now = base_monster_instance.hp
        self.win_count = win_count

    def draw_monster(self, is_facing_right=False):
        # モンスターを描画
        if is_facing_right:
            pyxel.blt(
                x=self.x,
                y=self.y,
                img=0,
                u=self.base_monster_instance.u,
                v=self.base_monster_instance.v,
                w=self.base_monster_instance.w * (-1),
                h=self.base_monster_instance.h,
                colkey=TRANSPARENT_COLOR,
                scale=4,
            )
        else:
            pyxel.blt(
                x=self.x,
                y=self.y,
                img=0,
                u=self.base_monster_instance.u,
                v=self.base_monster_instance.v,
                w=self.base_monster_instance.w,
                h=self.base_monster_instance.h,
                colkey=TRANSPARENT_COLOR,
                scale=4,
            )

    def get_result_of_move(self, move, target):
        message = []
        if move.accuracy > random.randrange(100):
            # 命中したとき
            # 技の相性
            compatibility = target.base_monster_instance.compatibility[move.type]
            if compatibility > 1:
                message.append("効果は抜群だ！")
            elif compatibility < 1:
                message.append("効果はいまひとつだ...")
            # モンスターのタイプと技のタイプが一致していれば 1.5 倍の補正が乗る
            if move.type == self.base_monster_instance.type:
                type_match = 1.5
            else:
                type_match = 1
            # ダメージ
            base_damage = round(
                11
                * self.base_monster_instance.attack
                * move.power
                * type_match
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
    def __init__(self, name, type, power, accuracy):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy


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
