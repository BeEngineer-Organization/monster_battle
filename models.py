import pyxel

TRANSPARENT_COLOR = 2

TYPES = [None, "ノーマル", "ほのお", "みず", "くさ", "ひこう", "ドラゴン", "どく"]


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
    ):
        self.u, self.v, self.w, self.h = u, v, w, h
        self.name = name
        self.types = (TYPES.index(type1), TYPES.index(type2))
        (
            self.hp,
            self.attack,
            self.defense,
            self.sp_attack,
            self.sp_difense,
            self.speed,
        ) = (hp, attack, defense, sp_attack, sp_difense, speed)
        self.hp_now = hp

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
