from models import BaseMonster, AttackMove

sample_monster = BaseMonster(
    u=32,
    v=64,
    w=32,
    h=32,
    name="サラマンドン",
    type1="ほのお",
    type2="ひこう",
    hp=153,
    attack=129,
    defense=105,
    speed=120,
    compatibility={
        "ノーマル": 1,
        "ほのお": 0.5,
        "みず": 2,
        "くさ": 0.25,
        "ひこう": 1,
        "ドラゴン": 1,
        "どく": 1,
    },
    moves=[
        AttackMove(name="だいもんじ", type="ほのお", power=110, accuracy=85),
        AttackMove(name="エアスラッシュ", type="ひこう", power=75, accuracy=95),
        AttackMove(name="りゅうのはどう", type="ドラゴン", power=85, accuracy=85),
    ],
)
