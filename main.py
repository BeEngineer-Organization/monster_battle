import pyxel
import PyxelUniversalFont as puf

WIDTH, HEIGHT = 640, 400
SCENE_BATTLE = 0
TRANSPARENT_COLOR = 2
SCALE = 4.0

TYPES = [None, "ノーマル", "ほのお", "みず", "くさ", "ひこう", "ドラゴン", "どく"]
WRITER = puf.Writer("misaki_gothic.ttf")


class Monster:
    def __init__(
        self,
        x,
        y,
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
        self.x = x
        self.y = y
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

    def draw(self):
        # モンスターを描画
        pyxel.blt(
            self.x,
            self.y,
            0,
            self.u,
            self.v,
            self.w,
            self.h,
            TRANSPARENT_COLOR,
            scale=SCALE,
        )
        # 名前を描画
        WRITER.draw(self.x - 40, self.y - 100, self.name, 16, 0)
        # HPバーを描画
        pyxel.rect(self.x - 40, self.y - 80, 100, 10, 0)
        hp_color = 11
        hp_ratio = self.hp_now / self.hp
        if hp_ratio < 0.25:
            # HPが1/4未満のとき赤色
            hp_color = 8
        elif hp_ratio < 0.5:
            # HPが1/4以上1/2未満のとき黄色
            hp_color = 10
        pyxel.rect(self.x - 40, self.y - 80, 100 * hp_ratio, 10, hp_color)
        # HP情報を描画
        WRITER.draw(
            self.x - 40, self.y - 60, f"{str(self.hp_now)}/{str(self.hp)}", 16, 0
        )


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.scene = SCENE_BATTLE

        self.monster1 = Monster(
            WIDTH * 0.66,
            HEIGHT * 0.33,
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
        self.monster2 = Monster(
            WIDTH * 0.33,
            HEIGHT * 0.33,
            0,
            17,
            -20,
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

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(7)
        self.monster1.draw()
        self.monster2.draw()
        # 「YOURS」を描画
        WRITER.draw(WIDTH * 0.33 - 30, HEIGHT * 0.33 + 60, "YOURS", 32, 8)
        # メッセージ表示枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)
        # メッセージを描画
        WRITER.draw(40, HEIGHT * 0.66 + 10, "どうする？", 24, 0)
        WRITER.draw(80, HEIGHT * 0.66 + 60, "戦う", 24, 0)
        WRITER.draw(200, HEIGHT * 0.66 + 60, "モンスター", 24, 0)
        WRITER.draw(400, HEIGHT * 0.66 + 60, "降参する", 24, 0)


App()
