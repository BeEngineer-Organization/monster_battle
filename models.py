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
