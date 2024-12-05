import pyxel

from monster import WRITER, ALL_MONSTERS

WIDTH, HEIGHT = 640, 400

SELECT_ACTION_SCENE = 0
SELECT_MOVE_SCENE = 1
SELECT_MONSTER_SCENE = 2

MESSAGE_X = 40
DELTA_MESSAGE_Y = 22
MESSAGE_1_Y = HEIGHT * 0.66
MESSAGE_2_Y = MESSAGE_1_Y + DELTA_MESSAGE_Y
MESSAGE_3_Y_Y = MESSAGE_2_Y + DELTA_MESSAGE_Y
MESSAGE_4_Y = MESSAGE_3_Y_Y + DELTA_MESSAGE_Y
MESSAGE_5_Y = MESSAGE_4_Y + DELTA_MESSAGE_Y
MESSAGE_FONT_SIZE = 16


class SelectTriangle:
    def __init__(self, max_y1):
        self.x1 = MESSAGE_X
        self.y1 = MESSAGE_1_Y
        self.x2 = MESSAGE_X
        self.y2 = MESSAGE_1_Y + 12
        self.x3 = MESSAGE_X + 10
        self.y3 = MESSAGE_1_Y + 6
        self.max_y1 = max_y1

    def reset(self, max_y1):
        self.x1 = MESSAGE_X
        self.y1 = MESSAGE_1_Y
        self.x2 = MESSAGE_X
        self.y2 = MESSAGE_1_Y + 12
        self.x3 = MESSAGE_X + 10
        self.y3 = MESSAGE_1_Y + 6
        self.max_y1 = max_y1

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
            delta_y = DELTA_MESSAGE_Y * -1
        else:
            delta_y = DELTA_MESSAGE_Y

        if MESSAGE_1_Y <= self.y1 + delta_y and self.y1 + delta_y <= self.max_y1:
            self.y1 += delta_y
            self.y2 += delta_y
            self.y3 += delta_y


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.scene = SELECT_ACTION_SCENE
        self.my_monsters = []
        self.opponenent_monsters = []
        self.select_triangle = SelectTriangle(MESSAGE_2_Y)
        self.game_settings()

    def game_settings(self):
        self.my_monsters.append(ALL_MONSTERS[0])
        self.opponenent_monsters.append(ALL_MONSTERS[0])
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == SELECT_ACTION_SCENE:
            self.update_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            self.update_select_move_scene()

    def update_select_action_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            if self.select_triangle.y1 == MESSAGE_1_Y:
                # 技選択画面に移動
                self.select_triangle.reset(MESSAGE_5_Y)
                self.scene = SELECT_MOVE_SCENE
            elif self.select_triangle.y1 == MESSAGE_2_Y:
                # モンスター選択画面に移動
                self.scene = SELECT_MONSTER_SCENE

    def update_select_move_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            if self.select_triangle.y1 == MESSAGE_5_Y:
                # 技選択画面に移動
                self.select_triangle.reset(MESSAGE_2_Y)
                self.scene = SELECT_ACTION_SCENE

    def draw(self):
        pyxel.cls(7)
        if self.scene == SELECT_ACTION_SCENE:
            self.draw_monsters()
            self.draw_select_action_scene()
        if self.scene == SELECT_MOVE_SCENE:
            self.draw_monsters()
            self.draw_select_move_scene()

    def draw_monsters(self):
        # モンスターを描画
        self.my_monsters[0].draw_monster(WIDTH * 0.33, HEIGHT * 0.33, 4, True)
        self.opponenent_monsters[0].draw_monster(WIDTH * 0.66, HEIGHT * 0.33, 4)
        # モンスターの名前とHPを描画
        self.my_monsters[0].draw_name_and_hp(WIDTH * 0.33 - 40, HEIGHT * 0.33 - 100)
        self.opponenent_monsters[0].draw_name_and_hp(
            WIDTH * 0.66 - 40, HEIGHT * 0.33 - 100, False
        )
        # 「YOURS」を描画
        WRITER.draw(WIDTH * 0.33 - 30, HEIGHT * 0.33 + 60, "YOURS", 32, 8)
        # メッセージ表示枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)

    def draw_select_action_scene(self):
        # メッセージを描画
        WRITER.draw(MESSAGE_X + 20, MESSAGE_1_Y, "たたかう", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_2_Y, "モンスター", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    def draw_select_move_scene(self):
        # メッセージを描画
        WRITER.draw(MESSAGE_X + 20, MESSAGE_1_Y, "たいあたり", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_2_Y, "つるのむち", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_3_Y_Y, "はたく", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_4_Y, "のしかかる", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_5_Y, "もどる", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()


App()
