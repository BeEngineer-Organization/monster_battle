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

MY_MONSTER_X = WIDTH * 0.25
OPPONENT_MONSTER_X = WIDTH * 0.75
MONSTER_Y = HEIGHT * 0.33


# モンスター名とHPバーを描画する関数
def _draw_monster_name_and_hp(monster, x, y, is_visible=True):
    # 名前を描画
    WRITER.draw(x, y, monster.base_monster_instance.name, 16, 0)
    # HPバーを描画
    # 最大HP
    pyxel.rect(x, y + 20, 100, 10, 0)
    # 現在HP
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


# 選択肢を描画する関数
def _draw_choices(choices):
    counter = 0
    for choice in choices:
        WRITER.draw(
            SELECTED_MESSAGE_X,
            MESSAGE_Y[counter],
            choice,
            MESSAGE_FONT_SIZE,
            0,
        )
        counter += 1


# メッセージを描画する関数
def _draw_message(message, y=0):
    WRITER.draw(
        MESSAGE_X,
        MESSAGE_Y[y],
        message,
        MESSAGE_FONT_SIZE,
        0,
    )


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("./resource.pyxres")
        self.scene = SELECT_ACTION_SCENE
        self.select_triangle = SelectTriangle(
            base_x=MESSAGE_X,
            base_y=MESSAGE_Y[0],
            delta_y=DELTA_MESSAGE_Y,
            y1_max=MESSAGE_Y[1],
        )
        self.game_settings()

    def game_settings(self):
        try:
            # セーブデータの読み込み
            with open("data.json", "r") as f:
                data = json.load(f)
            my_monsters = []
            for d in data:
                my_monsters.append(
                    Monster(
                        x=MY_MONSTER_X,
                        y=MONSTER_Y,
                        base_monster_instance=ALL_MONSTERS[d["monster_index"]],
                        win_count=d["win_count"],
                    ),
                )
            self.my_monsters = my_monsters
        except FileNotFoundError:
            # セーブデータがないとき
            self.my_monsters = [
                Monster(
                    x=MY_MONSTER_X,
                    y=MONSTER_Y,
                    base_monster_instance=ALL_MONSTERS[0],
                ),
                Monster(
                    x=MY_MONSTER_X,
                    y=MONSTER_Y,
                    base_monster_instance=ALL_MONSTERS[3],
                ),
                Monster(
                    x=MY_MONSTER_X,
                    y=MONSTER_Y,
                    base_monster_instance=ALL_MONSTERS[6],
                ),
            ]
        # 相手のモンスター
        self.opponent_monsters = [
            Monster(
                x=OPPONENT_MONSTER_X,
                y=MONSTER_Y,
                base_monster_instance=ALL_MONSTERS[random.choice([0, 3, 6, 9])],
            ),
            Monster(
                x=OPPONENT_MONSTER_X,
                y=MONSTER_Y,
                base_monster_instance=ALL_MONSTERS[random.choice([1, 4, 7, 10])],
            ),
            Monster(
                x=OPPONENT_MONSTER_X,
                y=MONSTER_Y,
                base_monster_instance=ALL_MONSTERS[random.choice([2, 5, 8, 11, 12])],
            ),
        ]
        # 場に出ているモンスター
        self.my_monster_battling = self.my_monsters[0]
        self.opponent_monster_battling = self.opponent_monsters[0]
        pyxel.run(self.update, self.draw)

    def save(self):
        data = []
        for monster in self.my_monsters:
            data.append(
                {
                    "monster_index": ALL_MONSTERS.index(monster.base_monster_instance),
                    "win_count": monster.win_count,
                }
            )
        with open("data.json", "w") as f:
            json.dump(data, f)

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
        # メッセージ描画枠を描画
        pyxel.rectb(15, HEIGHT * 0.66 - 15, WIDTH - 30, HEIGHT * 0.33, 0)
        # 場に出ているプレイヤーのモンスターを描画
        self.my_monster_battling.draw_monster(True)
        # モンスターの名前とHPを描画
        _draw_monster_name_and_hp(
            self.my_monster_battling, MY_MONSTER_X - 32, MONSTER_Y - 80
        )
        # 場に出ている相手モンスターを描画
        self.opponent_monster_battling.draw_monster()
        # モンスターの名前とHPを描画
        _draw_monster_name_and_hp(
            self.opponent_monster_battling,
            OPPONENT_MONSTER_X - 32,
            MONSTER_Y - 80,
            is_visible=False,
        )
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
                self.select_triangle.reset(MESSAGE_Y[4])
                self.scene = SELECT_MONSTER_SCENE

    def draw_select_action_scene(self):
        # 行動の選択肢を描画
        _draw_choices(["たたかう", "モンスター"])
        # 矢印の描画
        self.select_triangle.draw()

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
                # 行動選択シーンに戻る
                self.select_triangle.reset(MESSAGE_Y[1])
                self.scene = SELECT_ACTION_SCENE
            else:
                index = MESSAGE_Y.index(self.select_triangle.y1)
                try:
                    # プレイヤーの行動
                    my_action = {
                        "is_player": True,
                        "monster": self.my_monster_battling,
                        "move": self.my_monster_battling.base_monster_instance.moves[
                            index
                        ],
                    }
                    # 相手の行動
                    opponent_action = {
                        "is_player": False,
                        "monster": self.opponent_monster_battling,
                        "move": self.opponent_monster_battling.base_monster_instance.moves[
                            random.randrange(
                                len(
                                    self.opponent_monster_battling.base_monster_instance.moves
                                )
                            )
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
                    # 技名シーンに移動
                    self.scene = MOVE_NAME_SCENE

                except IndexError:
                    # 選択した技がないとき
                    return

    def draw_select_move_scene(self):
        # 選択肢として描画する情報
        choices = []
        for move in self.my_monster_battling.base_monster_instance.moves:
            if move.kind == "recover":
                # 回復技のとき
                choices.append(
                    f"{move.name} 分類:回復 タイプ:{move.type} {move.description}"
                )
            else:
                # 攻撃技のとき
                choices.append(
                    f"{move.name} 分類:攻撃 タイプ:{move.type} 威力:{move.power} 命中:{move.accuracy}"
                )
        # 技の選択肢を描画
        _draw_choices(choices)
        # 「戻る」を描画
        WRITER.draw(SELECTED_MESSAGE_X, MESSAGE_Y[4], "もどる", MESSAGE_FONT_SIZE, 0)
        # 矢印の描画
        self.select_triangle.draw()

    # モンスター選択シーン
    def update_select_monster_scene(self):
        if pyxel.btnr(pyxel.KEY_UP):
            # 上ボタンが離されるとき
            self.select_triangle.select(is_up=True)

        elif pyxel.btnr(pyxel.KEY_DOWN):
            # 下ボタンが離されるとき
            self.select_triangle.select()

        elif pyxel.btnr(pyxel.KEY_SPACE):
            # スペースボタンが離されるとき
            if self.select_triangle.y1 == MESSAGE_Y[4]:
                # 「戻る」ボタンが押されたとき、技選択シーンに戻る
                self.select_triangle.reset(MESSAGE_Y[1])
                self.scene = SELECT_ACTION_SCENE
            else:
                # モンスターが選択されたとき
                index = MESSAGE_Y.index(self.select_triangle.y1)
                try:
                    # 選択したモンスターがすでに場に出ているとき、または選択したモンスターのHPが0のとき
                    if (
                        self.my_monsters[index] == self.my_monster_battling
                        or self.my_monsters[index].hp_now == 0
                    ):
                        return
                    else:
                        if self.my_monster_battling.hp_now == 0:
                            # 場にいるモンスターのHPが0のとき、相手は行動しない
                            self.actions = []
                        else:
                            # 場にいるモンスターのHPが0でないとき、相手は行動する
                            opponent_action = {
                                "is_player": False,
                                "monster": self.opponent_monster_battling,
                                "move": self.opponent_monster_battling.base_monster_instance.moves[
                                    random.randrange(
                                        len(
                                            self.opponent_monster_battling.base_monster_instance.moves
                                        )
                                    )
                                ],
                            }
                            self.actions = [opponent_action]
                        # 場にいるモンスターを選択したモンスターに変更
                        self.my_monster_battling = self.my_monsters[index]
                        # 自分が場に出すシーンに移動
                        self.scene = PLAYER_PUT_SCENE

                except IndexError:
                    # 選択したモンスターがいないとき
                    return

    def draw_select_monster_scene(self):
        # 選択肢として描画する情報
        choices = []
        for monster in self.my_monsters:
            choices.append(
                f"{monster.base_monster_instance.name} タイプ:{monster.base_monster_instance.type1} {monster.base_monster_instance.type2} HP:{monster.hp_now}/{monster.base_monster_instance.hp} 攻:{monster.base_monster_instance.attack} 防:{monster.base_monster_instance.defense} 速:{monster.base_monster_instance.speed}"
            )
        # 技の選択肢を描画
        _draw_choices(choices)
        if self.my_monster_battling.hp_now > 0:
            # 自分の場に出ているモンスターが戦えるとき、「戻る」を描画
            WRITER.draw(
                SELECTED_MESSAGE_X, MESSAGE_Y[4], "もどる", MESSAGE_FONT_SIZE, 0
            )
        # 矢印の描画
        self.select_triangle.draw()

    # 技名シーン
    def update_move_name_scene(self):
        time.sleep(1)
        # 技シーンに移動
        self.scene = MOVE_SCENE

    def draw_move_name_scene(self):
        try:
            # 順に行動する
            self.action = self.actions.pop(0)
        except IndexError:
            # 残っている行動がなくなれば次の行動選択シーンに移動
            self.select_triangle.reset(MESSAGE_Y[1])
            self.scene = SELECT_ACTION_SCENE
            return

        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            _draw_message(
                f"{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )
        else:
            # 相手の行動のとき
            _draw_message(
                f"相手の{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )

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
        # 技によるHP処理シーンに移動
        self.scene = MOVE_HP_SCENE

    def draw_move_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            _draw_message(
                f"{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )
        else:
            # 相手の行動のとき
            _draw_message(
                f"相手の{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )

    # 技によるHP処理シーン
    def update_move_hp_scene(self):
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
        self.scene = MOVE_MESSAGE_SCENE

    def draw_move_hp_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            _draw_message(
                f"{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )
        else:
            # 相手の行動のとき
            _draw_message(
                f"相手の{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )

    # 技メッセージシーン
    def update_move_message_scene(self):
        time.sleep(1.5)
        if self.my_monster_battling.hp_now == 0:
            # 自分のモンスターのHPがなくなったとき
            if (
                self.my_monsters[0].hp_now
                + self.my_monsters[1].hp_now
                + self.my_monsters[2].hp_now
                == 0
            ):
                # 全滅したとき、敗北シーンに移動
                self.scene = LOSE_SCENE
            else:
                # モンスター選択シーンに移動
                self.select_triangle.reset(MESSAGE_Y[2])
                self.scene = SELECT_MONSTER_SCENE
        elif self.opponent_monster_battling.hp_now == 0:
            # 相手のモンスターのHPが無くなったとき、場にいるモンスターの勝利回数が増加
            self.my_monster_battling.win_count += 1
            if (
                self.opponent_monsters[0].hp_now
                + self.opponent_monsters[1].hp_now
                + self.opponent_monsters[2].hp_now
                == 0
            ):
                # 相手が全滅したら、勝利シーンに移動
                self.scene = WIN_SCENE
            else:
                # 進化処理
                if self.my_monster_battling.win_count == 1:
                    # 勝利回数が1回なら進化
                    self.my_monster_battling.base_monster_instance = ALL_MONSTERS[
                        ALL_MONSTERS.index(
                            self.my_monster_battling.base_monster_instance
                        )
                        + 1
                    ]
                elif self.my_monster_battling.win_count == 3:
                    # 勝利回数が3回なら進化
                    self.my_monster_battling.base_monster_instance = ALL_MONSTERS[
                        ALL_MONSTERS.index(
                            self.my_monster_battling.base_monster_instance
                        )
                        + 1
                    ]
                # 相手の場にいるモンスターを次の相手モンスターに変更
                self.opponent_monster_battling = self.opponent_monsters[
                    self.opponent_monsters.index(self.opponent_monster_battling) + 1
                ]
                # 相手が場に出すシーンに移動
                self.scene = OPPONENT_PUT_SCENE
        else:
            # 誰のHPも0にならないとき、技名シーンに移動
            self.scene = MOVE_NAME_SCENE

    def draw_move_message_scene(self):
        # 技のメッセージを描画
        if self.action["is_player"]:
            # 自分の行動のとき
            _draw_message(
                f"{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )
            counter = 1
            for msg in self.message:
                _draw_message(msg, counter)
                counter += 1
        else:
            # 相手の行動のとき
            _draw_message(
                f"相手の{self.action['monster'].base_monster_instance.name}の{self.action['move'].name}！"
            )
            counter = 1
            for msg in self.message:
                _draw_message(msg, counter)
                counter += 1

    # 自分が場に出すシーン
    def update_player_put_scene(self):
        time.sleep(1)
        self.scene = MOVE_NAME_SCENE

    def draw_player_put_scene(self):
        _draw_message(
            f"ゆけっ！{self.my_monster_battling.base_monster_instance.name}！"
        )

    # 相手が場に出すシーン
    def update_opponent_put_scene(self):
        time.sleep(1)
        self.select_triangle.reset(MESSAGE_Y[1])
        self.scene = SELECT_ACTION_SCENE

    def draw_opponent_put_scene(self):
        _draw_message(
            f"相手は{self.opponent_monster_battling.base_monster_instance.name}を繰り出した！"
        )

    # 勝利シーン
    def update_win_scene(self):
        time.sleep(1)
        self.save()
        sys.exit()

    def draw_win_scene(self):
        _draw_message("相手に勝利した！")

    # 敗北シーン
    def update_lose_scene(self):
        time.sleep(1)
        self.save()
        sys.exit()

    def draw_lose_scene(self):
        _draw_message("負けてしまった...")


App()
