import pyxel
import PyxelUniversalFont as puf
import random
import time

from models import Monster, SelectTriangle
from monsters import ALL_MONSTERS
from moves import ALL_MOVES

WIDTH, HEIGHT = 640, 400
WRITER = puf.Writer("misaki_gothic.ttf")

SELECT_ACTION_SCENE = 0
SELECT_MOVE_SCENE = 1
BEFORE_MOVE_SCENE = 2
MOVE_SCENE = 3
MOVE_EFFECT_SCENE = 4
AFTER_MOVE_SCENE = 5
SELECT_MONSTER_SCENE = 6

MESSAGE_X = 40
DELTA_MESSAGE_Y = 22
MESSAGE_Y = []
for i in range(5):
    MESSAGE_Y.append(HEIGHT * 0.66 + i * DELTA_MESSAGE_Y)
MESSAGE_FONT_SIZE = 16

MY_MONSTER_X = WIDTH * 0.25
OPPONENT_MONSTER_X = WIDTH * 0.75
MONSTER_Y = HEIGHT * 0.33


def _draw_monster_name_and_hp(monster, x, y, is_visible=True):
    # 名前を描画
    WRITER.draw(x, y, monster.base_monster_instance.name, 16, 0)
    # HPバーを描画
    pyxel.rect(x, y + 20, 100, 10, 0)
    hp_ratio = monster.hp_now / monster.base_monster_instance.hp
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
        WRITER.draw(
            x,
            y + 35,
            f"{str(monster.hp_now)}/{str(monster.base_monster_instance.hp)}",
            16,
            0,
        )


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
        self.my_monsters = [
            Monster(
                MY_MONSTER_X,
                MONSTER_Y,
                ALL_MONSTERS[12],
                [ALL_MOVES[0], ALL_MOVES[1]],
            )
        ]
        self.opponent_monsters = [
            Monster(
                OPPONENT_MONSTER_X,
                MONSTER_Y,
                ALL_MONSTERS[11],
                [ALL_MOVES[0], ALL_MOVES[1]],
            )
        ]
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
        elif self.scene == BEFORE_MOVE_SCENE:
            # 技前シーン
            self.update_before_move_scene()
        elif self.scene == MOVE_SCENE:
            # 技シーン
            self.update_move_scene()
        elif self.scene == MOVE_EFFECT_SCENE:
            # 技結果シーン
            self.update_move_effect_scene()
        elif self.scene == AFTER_MOVE_SCENE:
            # 技後シーン
            self.update_after_move_scene()

    # 行動選択シーン
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

    # 技選択シーン
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
                        "is_player": True,
                        "monster": self.my_monster_battling,
                        "move": self.my_monster_battling.moves[index],
                    }
                    # 相手の行動
                    opponent_action = {
                        "is_player": False,
                        "monster": self.opponent_monster_battling,
                        "move": self.opponent_monster_battling.moves[
                            random.randrange(len(self.opponent_monster_battling.moves))
                        ],
                    }
                    # 素早さの差を取得
                    delta_speed = (
                        self.my_monster_battling.base_monster_instance.speed
                        - self.opponent_monster_battling.base_monster_instance.speed
                    )
                    # 素早さが速い方が先手、遅い方が後手
                    if delta_speed > 0:
                        self.actions = [my_action, opponent_action]
                    elif delta_speed < 0:
                        self.actions = [opponent_action, my_action]
                    else:
                        # 素早さが同じだと50%で決まる
                        if random.randrange(1) == 0:
                            self.actions = [my_action, opponent_action]
                        else:
                            self.actions = [opponent_action, my_action]
                    # 技前シーンに移動
                    self.select_triangle.reset(MESSAGE_Y[1])
                    self.scene = BEFORE_MOVE_SCENE

                except IndexError:
                    # 選択した技がないとき
                    return

    # 技前シーン
    def update_before_move_scene(self):
        time.sleep(1)
        # 技シーンに移動
        self.scene = MOVE_SCENE

    # 技シーン
    def update_move_scene(self):
        if self.action["is_player"]:
            # 自分のモンスターの行動
            if self.action["move"].kind == "recover":
                # 回復
                time.sleep(0.5)
            else:
                # 攻撃
                if self.my_monster_battling.x < MY_MONSTER_X + 50:
                    self.my_monster_battling.x = MY_MONSTER_X + 50
                    return
                elif self.my_monster_battling.x == MY_MONSTER_X + 50:
                    self.my_monster_battling.x = MY_MONSTER_X
            # 技の結果
            result, message = self.my_monster_battling.get_result_of_move(
                self.action["move"], self.opponent_monster_battling
            )
            self.result = result
            self.message = message
        else:
            # 相手のモンスターの行動
            if self.action["move"].kind == "recover":
                # 回復
                time.sleep(0.5)
            else:
                # 攻撃
                if self.opponent_monster_battling.x > OPPONENT_MONSTER_X - 50:
                    self.opponent_monster_battling.x = OPPONENT_MONSTER_X - 50
                    return
                elif self.opponent_monster_battling.x == OPPONENT_MONSTER_X - 50:
                    self.opponent_monster_battling.x = OPPONENT_MONSTER_X
            # 技の結果
            result, message = self.opponent_monster_battling.get_result_of_move(
                self.action["move"], self.my_monster_battling
            )
            self.result = result
            self.message = message
        # 技シーンに移動
        self.scene = MOVE_EFFECT_SCENE

    # 技結果シーン
    def update_move_effect_scene(self):
        if self.action["move"].kind == "recover":
            # 回復技のとき
            if self.action["is_player"]:
                if self.my_monster_battling.hp_now < self.result:
                    self.my_monster_battling.hp_now += 1
                    return
            else:
                if self.opponent_monster_battling.hp_now < self.result:
                    self.opponent_monster_battling.hp_now += 1
                    return
        else:
            # 攻撃技のとき
            if self.action["is_player"]:
                if self.opponent_monster_battling.hp_now > self.result:
                    self.opponent_monster_battling.hp_now -= 1
                    return
            else:
                if self.my_monster_battling.hp_now > self.result:
                    self.my_monster_battling.hp_now -= 1
                    return
        self.scene = AFTER_MOVE_SCENE

    # 技後シーン
    def update_after_move_scene(self):
        time.sleep(2)
        # 技前シーンに移動
        self.scene = BEFORE_MOVE_SCENE

    def draw(self):
        pyxel.cls(7)
        # 場に出ているモンスターを描画
        self.my_monster_battling.draw_monster(True)
        self.opponent_monster_battling.draw_monster()
        # モンスターの名前とHPを描画
        _draw_monster_name_and_hp(
            self.my_monster_battling, MY_MONSTER_X - 32, MONSTER_Y - 80
        )
        _draw_monster_name_and_hp(
            self.opponent_monster_battling,
            OPPONENT_MONSTER_X - 32,
            MONSTER_Y - 80,
            is_visible=False,
        )
        # メッセージ表示枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)

        if self.scene == SELECT_ACTION_SCENE:
            # 行動選択シーン
            self.draw_select_action_scene()
        elif self.scene == SELECT_MOVE_SCENE:
            # 技選択シーン
            self.draw_select_move_scene()
        elif self.scene == BEFORE_MOVE_SCENE:
            # 技前シーン
            self.draw_before_move_scene()
        elif self.scene == MOVE_SCENE:
            # 技シーン
            self.draw_move_scene()
        elif self.scene == MOVE_EFFECT_SCENE:
            # 技結果シーン
            self.draw_move_effect_scene()
        elif self.scene == AFTER_MOVE_SCENE:
            # 技後シーン
            self.draw_after_move_scene()

    # 行動選択シーン
    def draw_select_action_scene(self):
        # 行動の選択肢を描画
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[0], "たたかう", MESSAGE_FONT_SIZE, 0)
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[1], "モンスター", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    # 技選択シーン
    def draw_select_move_scene(self):
        # 技の選択肢を描画
        counter = 0
        for move in self.my_monster_battling.moves:
            if move.kind == "recover":
                WRITER.draw(
                    MESSAGE_X + 20,
                    MESSAGE_Y[counter],
                    f"{move.name}  分類:回復 タイプ:{move.type} {move.description}",
                    MESSAGE_FONT_SIZE,
                    0,
                )
            else:
                WRITER.draw(
                    MESSAGE_X + 20,
                    MESSAGE_Y[counter],
                    f"{move.name}  分類:攻撃 タイプ:{move.type} 威力:{move.power} 命中:{move.accuracy} {move.description}",
                    MESSAGE_FONT_SIZE,
                    0,
                )
            counter += 1
        WRITER.draw(MESSAGE_X + 20, MESSAGE_Y[4], "もどる", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    # 技前シーン
    def draw_before_move_scene(self):
        try:
            # 順に行動する
            self.action = self.actions.pop(0)
        except IndexError:
            # 残っている行動がなくなれば次の行動選択シーンに移動
            self.scene = SELECT_ACTION_SCENE
            return

        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )
        else:
            # 相手の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"相手の{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )

    # 技シーン
    def draw_move_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )
        else:
            # 相手の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"相手の{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )

    # 技結果シーン
    def draw_move_effect_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )
        else:
            # 相手の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"相手の{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )

    # 技後シーン
    def draw_after_move_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )
            counter = 1
            for msg in self.message:
                WRITER.draw(
                    MESSAGE_X,
                    MESSAGE_Y[counter],
                    msg,
                    MESSAGE_FONT_SIZE,
                    0,
                )
                counter += 1
        else:
            # 相手の行動のとき
            WRITER.draw(
                MESSAGE_X,
                MESSAGE_Y[0],
                f"相手の{self.action["monster"].base_monster_instance.name}の{self.action["move"].name}！",
                MESSAGE_FONT_SIZE,
                0,
            )
            counter = 1
            for msg in self.message:
                WRITER.draw(
                    MESSAGE_X,
                    MESSAGE_Y[counter],
                    msg,
                    MESSAGE_FONT_SIZE,
                    0,
                )
                counter += 1


App()
