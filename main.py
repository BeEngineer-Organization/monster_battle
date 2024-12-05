import pyxel
import PyxelUniversalFont as puf

from monsters import ALL_MONSTERS

WIDTH, HEIGHT = 640, 400
WRITER = puf.Writer("misaki_gothic.ttf")

SELECT_ACTION_SCENE = 0
SELECT_MOVE_SCENE = 1
BATTLE_SCENE = 2
SELECT_MONSTER_SCENE = 3

MESSAGE_X = 40
DELTA_MESSAGE_Y = 22
MESSAGE_Y = []
for i in range(5):
    MESSAGE_Y.append(HEIGHT * 0.66 + i * DELTA_MESSAGE_Y)
MESSAGE_FONT_SIZE = 16


def draw_monster_name_and_hp(monster, x, y, is_visible=True):
    # 名前を描画
    WRITER.draw(x, y, monster.name, 16, 0)
    # HPバーを描画
    pyxel.rect(x, y + 20, 100, 10, 0)
    hp_ratio = monster.hp_now / monster.hp
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
        WRITER.draw(x, y + 35, f"{str(monster.hp_now)}/{str(monster.hp)}", 16, 0)


class SelectTriangle:
    def __init__(self, max_y1):
        self.x1 = MESSAGE_X
        self.y1 = MESSAGE_Y[0]
        self.x2 = MESSAGE_X
        self.y2 = MESSAGE_Y[0] + 12
        self.x3 = MESSAGE_X + 10
        self.y3 = MESSAGE_Y[0] + 6
        self.max_y1 = max_y1

    def reset(self, max_y1):
        self.x1 = MESSAGE_X
        self.y1 = MESSAGE_Y[0]
        self.x2 = MESSAGE_X
        self.y2 = MESSAGE_Y[0] + 12
        self.x3 = MESSAGE_X + 10
        self.y3 = MESSAGE_Y[0] + 6
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

        if MESSAGE_Y[0] <= self.y1 + delta_y and self.y1 + delta_y <= self.max_y1:
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
        self.select_triangle = SelectTriangle(MESSAGE_Y[1])
        self.game_settings()

    def game_settings(self):
        # 手持ちのモンスター
        self.my_monsters.append(ALL_MONSTERS[0])
        self.opponenent_monsters.append(ALL_MONSTERS[0])
        # 場に出ているモンスター
        self.my_monster_battling = self.my_monsters[0]
        self.opponenent_monster_battling = self.opponenent_monsters[0]
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
            if self.select_triangle.y1 == MESSAGE_Y[0]:
                # 技選択画面に移動
                self.select_triangle.reset(MESSAGE_Y[4])
                self.scene = SELECT_MOVE_SCENE
            elif self.select_triangle.y1 == MESSAGE_Y[1]:
                # モンスター選択画面に移動
                self.scene = SELECT_MONSTER_SCENE

    def update_select_move_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            if self.select_triangle.y1 == MESSAGE_Y[4]:
                # 技選択画面に移動
                self.select_triangle.reset(MESSAGE_Y[1])
                self.scene = SELECT_ACTION_SCENE
            else:
                index = MESSAGE_Y.index(self.select_triangle.y1)
                try:
                    self.my_move = self.my_monster_battling.moves[index]
                    self.scene = BATTLE_SCENE
                except IndexError:
                    return
                # 選択した技があるとき

    def draw(self):
        pyxel.cls(7)
        if self.scene == SELECT_ACTION_SCENE:
            self.draw_monsters()
            self.draw_select_action_scene()
        if self.scene == SELECT_MOVE_SCENE:
            self.draw_monsters()
            self.draw_select_move_scene()

    def draw_monsters(self):
        # 場に出ているモンスターを描画
        self.my_monster_battling.draw_monster(WIDTH * 0.33, HEIGHT * 0.33, 4, True)
        self.opponenent_monster_battling.draw_monster(WIDTH * 0.66, HEIGHT * 0.33, 4)
        # モンスターの名前とHPを描画
        draw_monster_name_and_hp(
            self.my_monster_battling, WIDTH * 0.33 - 40, HEIGHT * 0.33 - 100
        )
        draw_monster_name_and_hp(
            self.opponenent_monster_battling,
            WIDTH * 0.66 - 40,
            HEIGHT * 0.33 - 100,
            is_visible=False,
        )
        # 「YOURS」を描画
        WRITER.draw(WIDTH * 0.33 - 30, HEIGHT * 0.33 + 60, "YOURS", 32, 8)
        # メッセージ表示枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)

    def draw_select_action_scene(self):
        # メッセージを描画
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[0], "たたかう", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[1], "モンスター", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    def draw_select_move_scene(self):
        # メッセージを描画
        counter = 0
        for move in self.my_monster_battling.moves:
            WRITER.draw(
                MESSAGE_X + 20, MESSAGE_Y[counter], move.name, MESSAGE_FONT_SIZE, 0
            )
            counter += 1
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[4], "もどる", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()


App()
