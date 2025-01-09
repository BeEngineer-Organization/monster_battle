from models import Move

# ノーマル
NORMAL_MOVES = [
    Move(name="とっしん", type="ノーマル", power=90, accuracy=85),
    Move(name="すてみタックル", type="ノーマル", power=120, accuracy=100),
]
# ほのお
FIRE_MOVES = [
    Move(name="ほのおのパンチ", type="ほのお", power=75, accuracy=100),
    Move(name="だいもんじ", type="ほのお", power=110, accuracy=85),
]
# みず
WATER_MOVES = [
    Move(name="だくりゅう", type="みず", power=90, accuracy=85),
    Move(name="ハイドロカノン", type="みず", power=150, accuracy=90),
]
# くさ
GRASS_MOVES = [
    Move(name="タネばくだん", type="くさ", power=80, accuracy=100),
    Move(name="パワーウィップ", type="くさ", power=120, accuracy=85),
]
