from models import Monster
from moves import ALL_MOVES

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
        [ALL_MOVES[1], ALL_MOVES[0]],
        {
            "ノーマル": 1,
            "ほのお": 2,
            "みず": 0.5,
            "くさ": 0.25,
            "ひこう": 2,
            "ドラゴン": 1,
            "どく": 1,
        },
    )
]
