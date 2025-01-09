import pyxel
import PyxelUniversalFont as puf
import random
import time
import sys
import json

from models import Monster, SelectTriangle
from monsters import ALL_MONSTERS

WIDTH, HEIGHT = 640, 400
WRITER = puf.Writer("misaki_gothic.ttf")

SELECT_ACTION_SCENE = 0
SELECT_MOVE_SCENE = 1
SELECT_MONSTER_SCENE = 2
MOVE_NAME_SCENE = 3
MOVE_SCENE = 4
MOVE_HP_SCENE = 5
MOVE_MESSAGE_SCENE = 6
PLAYER_PUT_SCENE = 7
OPPONENT_PUT_SCENE = 8
WIN_SCENE = 9
LOSE_SCENE = 10

MESSAGE_X = 40
SELECTED_MESSAGE_X = MESSAGE_X + 20
DELTA_MESSAGE_Y = 22
MESSAGE_Y = []
for i in range(5):
    MESSAGE_Y.append(HEIGHT * 0.66 + i * DELTA_MESSAGE_Y)
MESSAGE_FONT_SIZE = 16

MY_MONSTER_X = WIDTH * 0.2
OPPONENT_MONSTER_X = WIDTH * 0.7
MONSTER_Y = HEIGHT * 0.4


# モンスター名とHPバーを描画する関数
def _draw_monster_name_and_hp(monster, x, y, is_visible=True):
    pass


# 選択肢を描画する関数
def _draw_choices(choices):
    pass


# メッセージを描画する関数
def _draw_message(message, y=0):
    pass


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.game_settings()

    def game_settings(self):
        pyxel.run(self.update, self.draw)

    def save(self):
        pass

    def update(self):
        if self.scene == SELECT_ACTION_SCENE:
            # 行動選択シーン
            self.update_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            # 技選択シーン
            self.update_select_move_scene()
        elif self.scene == SELECT_MONSTER_SCENE:
            # モンスター選択シーン
            self.update_select_monster_scene()
        elif self.scene == PLAYER_PUT_SCENE:
            # 自分が場に出すシーン
            self.update_player_put_scene()
        elif self.scene == OPPONENT_PUT_SCENE:
            # 相手が場に出すシーン
            self.update_opponent_put_scene()
        elif self.scene == MOVE_NAME_SCENE:
            # 技名シーン
            self.update_move_name_scene()
        elif self.scene == MOVE_SCENE:
            # 技シーン
            self.update_move_scene()
        elif self.scene == MOVE_HP_SCENE:
            # 技によるHP処理シーン
            self.update_move_hp_scene()
        elif self.scene == MOVE_MESSAGE_SCENE:
            # 技メッセージシーン
            self.update_move_message_scene()
        elif self.scene == WIN_SCENE:
            # 勝利シーン
            self.update_win_scene()
        elif self.scene == LOSE_SCENE:
            # 敗北シーン
            self.update_lose_scene()

    def draw(self):
        pyxel.cls(7)
        if self.scene == SELECT_ACTION_SCENE:
            # 行動選択シーン
            self.draw_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            # 技選択シーン
            self.draw_select_move_scene()
        elif self.scene == SELECT_MONSTER_SCENE:
            # モンスター選択シーン
            self.draw_select_monster_scene()
        elif self.scene == OPPONENT_PUT_SCENE:
            # 相手が場に出すシーン
            self.draw_opponent_put_scene()
        elif self.scene == PLAYER_PUT_SCENE:
            # 自分が場に出すシーン
            self.draw_player_put_scene()
        elif self.scene == MOVE_NAME_SCENE:
            # 技名シーン
            self.draw_move_name_scene()
        elif self.scene == MOVE_SCENE:
            # 技シーン
            self.draw_move_scene()
        elif self.scene == MOVE_HP_SCENE:
            # 技によるHP処理シーン
            self.draw_move_hp_scene()
        elif self.scene == MOVE_MESSAGE_SCENE:
            # 技メッセージシーン
            self.draw_move_message_scene()
        elif self.scene == WIN_SCENE:
            # 勝利シーン
            self.draw_win_scene()
        elif self.scene == LOSE_SCENE:
            # 敗北シーン
            self.draw_lose_scene()

    # 行動選択シーン
    def update_select_action_scene(self):
        pass

    def draw_select_action_scene(self):
        pass

    # 技選択シーン
    def update_select_move_scene(self):
        pass

    def draw_select_move_scene(self):
        pass

    # モンスター選択シーン
    def update_select_monster_scene(self):
        pass

    def draw_select_monster_scene(self):
        pass

    # 技名シーン
    def update_move_name_scene(self):
        pass

    def draw_move_name_scene(self):
        pass

    # 技シーン
    def update_move_scene(self):
        pass

    def draw_move_scene(self):
        pass

    # 技によるHP処理シーン
    def update_move_hp_scene(self):
        pass

    def draw_move_hp_scene(self):
        pass

    # 技メッセージシーン
    def update_move_message_scene(self):
        pass

    def draw_move_message_scene(self):
        pass

    # 自分が場に出すシーン
    def update_player_put_scene(self):
        pass

    def draw_player_put_scene(self):
        pass

    # 相手が場に出すシーン
    def update_opponent_put_scene(self):
        pass

    def draw_opponent_put_scene(self):
        pass

    # 勝利シーン
    def update_win_scene(self):
        pass

    def draw_win_scene(self):
        pass

    # 敗北シーン
    def update_lose_scene(self):
        pass

    def draw_lose_scene(self):
        pass


App()
