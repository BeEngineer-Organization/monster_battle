from models import BaseMonster

ALL_MONSTERS = [
    BaseMonster(
        u=0,
        v=17,
        w=20,
        h=17,
        name="フシギダネ",
        type1="くさ",
        type2="どく",
        hp=120,
        attack=85,
        defense=85,
        speed=65,
        compatibility={
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
