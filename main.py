import pyxel
import PyxelUniversalFont as puf

WIDTH, HEIGHT = 640, 400
SCENE_BATTLE = 0
TRANSPARENT_COLOR = 2
MESSAGE_POSITION_X = 40
FISRT_MESSAGE_POSITION_Y = HEIGHT * 0.66 + 10
FISRT_MESSAGE_POSITION_Y = HEIGHT * 0.66 + 10
SECOND_MESSAGE_POSITION_Y = HEIGHT * 0.66 + 60
MESSAGE_FONT_SIZE = 24

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
        difense,
        sp_attack,
        sp_difense,
        speed,
    ):
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.name = name
        self.types = (TYPES.index(type1), TYPES.index(type2))
        self.hp = hp
        self.hp_now = hp
        self.attack = attack
        self.difense = difense
        self.sp_attack = sp_attack
        self.sp_difense = sp_difense
        self.speed = speed

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
                x,
                y,
                0,
                self.u,
                self.v,
                self.w,
                self.h,
                TRANSPARENT_COLOR,
                scale=scale,
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
    Monster(
        0,
        17,
        20,
        17,
        "フシギダネ",
        "くさ",
        "どく",
        120,
        69,
        69,
        85,
        85,
        65,
    )
]


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.scene = SCENE_BATTLE
        self.my_monsters = []
        self.opponenent_monsters = []

        self.my_monsters.append(ALL_MONSTERS[0])
        self.opponenent_monsters.append(ALL_MONSTERS[0])

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(7)
        if self.scene == SCENE_BATTLE:
            # 「YOURS」を描画
            WRITER.draw(WIDTH * 0.33 - 30, HEIGHT * 0.33 + 60, "YOURS", 32, 8)
            # メッセージ表示枠を描画
            pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)
            # モンスターを描画
            self.my_monsters[0].draw_monster(WIDTH * 0.33, HEIGHT * 0.33, 4, True)
            self.opponenent_monsters[0].draw_monster(WIDTH * 0.66, HEIGHT * 0.33, 4)
            # モンスターの名前とHPを描画
            self.my_monsters[0].draw_name_and_hp(WIDTH * 0.33 - 40, HEIGHT * 0.33 - 100)
            self.opponenent_monsters[0].draw_name_and_hp(
                WIDTH * 0.66 - 40, HEIGHT * 0.33 - 100, False
            )
            # メッセージを描画
            WRITER.draw(
                MESSAGE_POSITION_X,
                FISRT_MESSAGE_POSITION_Y,
                "どうする？",
                MESSAGE_FONT_SIZE,
                0,
            )
            WRITER.draw(
                MESSAGE_POSITION_X + 40,
                SECOND_MESSAGE_POSITION_Y,
                "戦う",
                MESSAGE_FONT_SIZE,
                0,
            )
            WRITER.draw(
                MESSAGE_POSITION_X + 160,
                SECOND_MESSAGE_POSITION_Y,
                "モンスター",
                MESSAGE_FONT_SIZE,
                0,
            )
            WRITER.draw(
                MESSAGE_POSITION_X + 360,
                SECOND_MESSAGE_POSITION_Y,
                "降参する",
                MESSAGE_FONT_SIZE,
                0,
            )


App()
