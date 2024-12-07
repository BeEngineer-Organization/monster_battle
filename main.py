import pyxel
import PyxelUniversalFont as puf
import random
import time

from models import SelectTriangle
from monsters import ALL_MONSTERS

WIDTH, HEIGHT = 640, 400
WRITER = puf.Writer("misaki_gothic.ttf")

SELECT_ACTION_SCENE = 0
SELECT_MOVE_SCENE = 1
MOVE_MESSAGE_SCENE = 2
MOVE_SCENE = 3
MOVE_EFFECT_SCENE = 4
MOVE_COMPATIBILITY_SCENE = 5
SELECT_MONSTER_SCENE = 6

MESSAGE_X = 40
DELTA_MESSAGE_Y = 22
MESSAGE_Y = []
for i in range(5):
    MESSAGE_Y.append(HEIGHT * 0.66 + i * DELTA_MESSAGE_Y)
MESSAGE_FONT_SIZE = 16


def _draw_monster_name_and_hp(monster, x, y, is_visible=True):
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


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.scene = SELECT_ACTION_SCENE
        self.select_triangle = SelectTriangle(
            MESSAGE_X, MESSAGE_Y[0], DELTA_MESSAGE_Y, MESSAGE_Y[1]
        )
        self.game_settings()

    def game_settings(self):
        # 手持ちのモンスター
        self.my_monsters = [ALL_MONSTERS[0]]
        self.opponent_monsters = [ALL_MONSTERS[0]]
        # 場に出ているモンスター
        self.my_monster_battling = self.my_monsters[0]
        self.opponent_monster_battling = self.opponent_monsters[0]
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == SELECT_ACTION_SCENE:
            # 行動選択シーン
            self.update_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            # 技選択シーン
            self.update_select_move_scene()
        elif self.scene == MOVE_MESSAGE_SCENE:
            # 技メッセージシーン
            self.update_move_message_scene()
        elif self.scene == MOVE_SCENE:
            # 技使用シーン
            self.update_move_scene()
        elif self.scene == MOVE_EFFECT_SCENE:
            # 技効果シーン
            self.update_move_effect_scene()
        elif self.scene == MOVE_COMPATIBILITY_SCENE:
            # 技相性シーン
            self.update_move_compatibility_scene()

    def update_select_action_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            # 上ボタンが離されるとき
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            # 下ボタンが離されるとき
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            # スペースボタンが離されるとき
            if self.select_triangle.y1 == MESSAGE_Y[0]:
                # 技選択シーンに移動
                self.select_triangle.reset(MESSAGE_Y[4])
                self.scene = SELECT_MOVE_SCENE
            elif self.select_triangle.y1 == MESSAGE_Y[1]:
                # モンスター選択シーンに移動
                self.scene = SELECT_MONSTER_SCENE

    def update_select_move_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            # 上ボタンが離されるとき
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            # 下ボタンが離されるとき
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            # スペースボタンが離されるとき
            if self.select_triangle.y1 == MESSAGE_Y[4]:
                # 技選択シーンに戻る
                self.select_triangle.reset(MESSAGE_Y[1])
                self.scene = SELECT_ACTION_SCENE
            else:
                index = MESSAGE_Y.index(self.select_triangle.y1)
                try:
                    # プレイヤーの行動
                    my_action = {
                        "monster": self.my_monster_battling,
                        "move": self.my_monster_battling.moves[index],
                    }
                    # 相手の行動
                    opponent_action = {
                        "monster": self.opponent_monster_battling,
                        "move": self.opponent_monster_battling.moves[
                            random.randint(0, len(self.opponent_monster_battling.moves))
                        ],
                    }
                    # 素早さの差を取得
                    delta_speed = (
                        self.my_monster_battling.speed
                        - self.opponent_monster_battling.speed
                    )
                    # 素早さが速い方が先手、遅い方が後手
                    if delta_speed > 0:
                        self.actions = [my_action, opponent_action]
                    elif delta_speed < 0:
                        self.actions = [opponent_action, my_action]
                    else:
                        # 素早さが同じだと50%で決まる
                        if random.randint(0, 1) == 0:
                            self.actions = [my_action, opponent_action]
                        else:
                            self.actions = [opponent_action, my_action]
                    # 技メッセージシーンに移動
                    self.scene = MOVE_MESSAGE_SCENE

                except IndexError:
                    # 選択した技がないとき
                    return

    def update_move_message_scene(self):
        time.sleep(2)
        # 技使用シーンに移動
        self.scene = MOVE_SCENE

    def update_move_scene(self):
        pass

    def update_move_effect_scene(self):
        pass

    def update_move_compatibility_scene(self):
        pass

    def draw(self):
        pyxel.cls(7)
        if self.scene == SELECT_ACTION_SCENE:
            # 行動選択シーン
            self.draw_monsters()
            self.draw_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            # 技選択シーン
            self.draw_monsters()
            self.draw_select_move_scene()
        elif self.scene == MOVE_MESSAGE_SCENE:
            # 技メッセージシーン
            self.draw_monsters()
            try:
                # 順に行動する
                self.action = self.actions.pop(0)
                self.draw_move_message_scene(self.action)
            except IndexError:
                # 残っている行動がなくなれば次の行動選択シーンに移動
                self.scene = SELECT_ACTION_SCENE
        elif self.scene == MOVE_SCENE:
            # 技使用シーン
            self.draw_move_scene()
        elif self.scene == MOVE_EFFECT_SCENE:
            # 技効果シーン
            self.draw_move_effect_scene()
        elif self.scene == MOVE_COMPATIBILITY_SCENE:
            # 技相性シーン
            self.draw_move_compatibility_scene()

    def draw_monsters(self):
        # 場に出ているモンスターを描画
        self.my_monster_battling.draw_monster(WIDTH * 0.33, HEIGHT * 0.33, 4, True)
        self.opponent_monster_battling.draw_monster(WIDTH * 0.66, HEIGHT * 0.33, 4)
        # モンスターの名前とHPを描画
        _draw_monster_name_and_hp(
            self.my_monster_battling, WIDTH * 0.33 - 40, HEIGHT * 0.33 - 100
        )
        _draw_monster_name_and_hp(
            self.opponent_monster_battling,
            WIDTH * 0.66 - 40,
            HEIGHT * 0.33 - 100,
            is_visible=False,
        )
        # 「YOURS」を描画
        WRITER.draw(WIDTH * 0.33 - 30, HEIGHT * 0.33 + 60, "YOURS", 32, 8)
        # メッセージ表示枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)

    def draw_select_action_scene(self):
        # 行動の選択肢を描画
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[0], "たたかう", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[1], "モンスター", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    def draw_select_move_scene(self):
        # 技の選択肢を描画
        counter = 0
        for move in self.my_monster_battling.moves:
            WRITER.draw(
                MESSAGE_X + 20, MESSAGE_Y[counter], move.name, MESSAGE_FONT_SIZE, 0
            )
            counter += 1
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[4], "もどる", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    def draw_move_message_scene(self, info):
        # 技のメッセージを描画
        WRITER.draw(
            MESSAGE_X,
            MESSAGE_Y[0],
            f"{info["monster"].name}の{info["move"].name}！",
            MESSAGE_FONT_SIZE,
            0,
        )

    def draw_move_scene(self):
        pass

    def draw_move_effect_scene(self):
        pass

    def draw_move_compatibility_scene(self):
        pass


App()
