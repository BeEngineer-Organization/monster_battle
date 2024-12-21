from models import BaseMonster, AttackMove

sample_monster = BaseMonster(
    u=128,
    v=32,
    w=32,
    h=32,
    name="ピッカー",
    type1="でんき",
    type2="",
    hp=110,
    attack=75,
    defense=70,
    speed=110,
    compatibility={
        "ノーマル": 1,
        "でんき": 0.5,
        "じめん": 2,
    },
    moves=[
        AttackMove(name="10まんボルト", type="でんき", power=90, accuracy=100),
        AttackMove(name="とっしん", type="ノーマル", power=90, accuracy=85),
        AttackMove(name="どろかけ", type="じめん", power=20, accuracy=100),
    ],
)
