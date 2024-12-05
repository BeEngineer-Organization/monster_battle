import pyxel
import PyxelUniversalFont as puf

TRANSPARENT_COLOR = 2

TYPES = [None, "ノーマル", "ほのお", "みず", "くさ", "ひこう", "ドラゴン", "どく"]
WRITER = puf.Writer("misaki_gothic.ttf")


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

    def draw_name_and_hp(self, x, y, is_visible=True):
        # 名前を描画
        WRITER.draw(x, y, self.name, 16, 0)
        # HPバーを描画
        pyxel.rect(x, y + 20, 100, 10, 0)
        hp_ratio = self.hp_now / self.hp
        if hp_ratio < 0.25:
            # HPが1/4未満のとき赤色
            hp_color = 8
        elif hp_ratio < 0.5:
            # HPが1/4以上1/2未満のとき黄色
            hp_color = 10
        else:
            hp_color = 11
        pyxel.rect(x, y + 20, 100 * hp_ratio, 10, hp_color)
        if is_visible:
            # HP情報を描画
            WRITER.draw(x, y + 35, f"{str(self.hp_now)}/{str(self.hp)}", 16, 0)


ALL_MONSTERS = [
    Monster(0, 17, 20, 17, "フシギダネ", "くさ", "どく", 120, 69, 69, 85, 85, 65)
]
