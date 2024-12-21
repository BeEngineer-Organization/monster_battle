from models import RecoverMove, AttackMove

# ノーマル
NORMAL_MOVES = [
    AttackMove(name="とっしん", type="ノーマル", power=90, accuracy=85),
    AttackMove(name="すてみタックル", type="ノーマル", power=120, accuracy=100),
]
# ほのお
FIRE_MOVES = [
    AttackMove(name="ひのこ", type="ほのお", power=40, accuracy=100),
    AttackMove(name="ほのおのパンチ", type="ほのお", power=75, accuracy=100),
    AttackMove(name="だいもんじ", type="ほのお", power=110, accuracy=85),
]
# みず
WATER_MOVES = [
    AttackMove(name="だくりゅう", type="みず", power=90, accuracy=85),
    AttackMove(name="ハイドロポンプ", type="みず", power=110, accuracy=80),
    AttackMove(name="ハイドロカノン", type="みず", power=150, accuracy=90),
]
# くさ
GRASS_MOVES = [
    AttackMove(name="はっぱカッター", type="くさ", power=55, accuracy=95),
    AttackMove(name="タネばくだん", type="くさ", power=80, accuracy=100),
    AttackMove(name="パワーウィップ", type="くさ", power=120, accuracy=85),
    RecoverMove(name="こうごうせい", type="くさ", description="HPを半分回復する"),
]
# ひこう
FLY_MOVES = [
    AttackMove(name="エアスラッシュ", type="ひこう", power=75, accuracy=95),
    RecoverMove(name="はねやすめ", type="ひこう", description="HPを半分回復する"),
]
# ドラゴン
DRAGON_MOVES = [
    AttackMove(name="りゅうのいぶき", type="ドラゴン", power=60, accuracy=100),
    AttackMove(name="りゅうのはどう", type="ドラゴン", power=85, accuracy=85),
    AttackMove(name="ドラゴンダイブ", type="ドラゴン", power=100, accuracy=75),
]
# どく
POIZON_MOVES = [
    AttackMove(name="ヘドロこうげき", type="どく", power=65, accuracy=100),
    AttackMove(name="ヘドロばくだん", type="どく", power=90, accuracy=100),
]
