import pyxel
import random

TRANSPARENT_COLOR = 2


class Monster:
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
        sp_attack,
        sp_difense,
        speed,
        moves,
        compatibility,
    ):
        self.u, self.v, self.w, self.h = u, v, w, h
        self.name = name
        self.types = type1, type2
        (
            self.hp,
            self.attack,
            self.defense,
            self.sp_attack,
            self.sp_difense,
            self.speed,
        ) = (hp, attack, defense, sp_attack, sp_difense, speed)
        self.hp_now = hp
        self.moves = moves
        self.compatibility = compatibility

    def draw_monster(self, x, y, scale, is_facing_right=False):
        # モンスターを描画
        if is_facing_right:
            pyxel.blt(
                x,
                y,
                0,
                self.u,
                self.v,
                self.w * (-1),
                self.h,
                TRANSPARENT_COLOR,
                scale=scale,
            )
        else:
            pyxel.blt(
                x, y, 0, self.u, self.v, self.w, self.h, TRANSPARENT_COLOR, scale=scale
            )

    def move(self, index, target):
        info = self.moves[index].get_info()
        if info["kind"] == "recover":
            # 回復技のとき
            self.hp_now += round(self.hp * 0.5, 0)
            if self.hp_now > self.hp:
                self.hp_now = self.hp
        elif info["kind"] == "physical":
            if info["accuracy"] > random.randint(1, 100):
                # 命中したとき
                base_damage = round(
                    11
                    * self.attack
                    * info["power"]
                    * self.compatibility[info["type"]]
                    / (25 * target.defense),
                    0,
                )
                target.hp_now -= base_damage * random.randint(85, 100) / 100
        else:
            if info["accuracy"] > random.randint(1, 100):
                # 命中したとき
                base_damage = round(
                    11
                    * self.sp_attack
                    * info["power"]
                    * self.compatibility[info["type"]]
                    / (25 * target.sp_defense),
                    0,
                )
                target.hp_now -= base_damage * random.randint(85, 100) / 100


class Move:
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type


class PhysicalMove(Move):
    def __init__(self, name, description, type, power, accuracy):
        super().__init__(name, description, type)
        self.kind = "physical"
        self.power = power
        self.accuracy = accuracy

    def get_info(self):
        return {
            "kind": self.kind,
            "type": self.type,
            "power": self.power,
            "accuracy": self.accuracy,
        }


class SpecialMove(Move):
    def __init__(self, name, description, type, power, accuracy):
        super().__init__(name, description, type)
        self.kind = "special"
        self.power = power
        self.accuracy = accuracy

    def get_info(self):
        return {
            "kind": self.kind,
            "type": self.type,
            "power": self.power,
            "accuracy": self.accuracy,
        }


class RecoverMove(Move):
    def __init__(self, name, description, type):
        super().__init__(name, description, type)
        self.kind = "recover"

    def get_info(self):
        return {"kind": self.kind}


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
