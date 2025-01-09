import pyxel
import random

TRANSPARENT_COLOR = 2


class BaseMonster:
    def __init__(
        self,
        u,
        v,
        w,
        h,
        name,
        type,
        hp,
        attack,
        defense,
        speed,
        compatibility,
        moves,
    ):
        pass


class Monster:
    def __init__(self, x, y, base_monster_instance, win_count=0):
        pass

    def draw_monster(self, is_facing_right=False):
        pass

    def get_result_of_move(self, move, target):
        pass


class Move:
    def __init__(self, name, type, power, accuracy):
        pass


class SelectTriangle:
    def __init__(self, base_x, base_y, delta_y, y1_max):
        pass

    def reset(self, y1_max):
        pass

    def draw(self):
        pass

    def select(self, is_up=False):
        pass
