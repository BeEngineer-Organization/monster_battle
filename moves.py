from models import RecoverMove, AttackMove

# ノーマル
NORMAL_MOVES = [
    AttackMove(name="とっしん", description="", type="ノーマル", power=90, accuracy=85),
    AttackMove(
        name="すてみタックル", description="", type="ノーマル", power=120, accuracy=100
    ),
]
# ほのお
FIRE_MOVES = [
    AttackMove(name="ひのこ", description="", type="ほのお", power=40, accuracy=100),
    AttackMove(
        name="ほのおのパンチ", description="", type="ほのお", power=75, accuracy=100
    ),
    AttackMove(
        name="だいもんじ", description="", type="ほのお", power=110, accuracy=85
    ),
]
# みず
WATER_MOVES = [
    AttackMove(name="だくりゅう", description="", type="みず", power=90, accuracy=85),
    AttackMove(
        name="ハイドロポンプ", description="", type="みず", power=110, accuracy=80
    ),
    AttackMove(
        name="ハイドロカノン", description="", type="みず", power=150, accuracy=90
    ),
]
# くさ
GRASS_MOVES = [
    AttackMove(
        name="はっぱカッター", description="", type="くさ", power=55, accuracy=95
    ),
    AttackMove(
        name="タネばくだん", description="", type="くさ", power=80, accuracy=100
    ),
    AttackMove(
        name="パワーウィップ", description="", type="くさ", power=120, accuracy=85
    ),
    RecoverMove(name="こうごうせい", description="HPを半分回復する", type="くさ"),
]
# ひこう
FLY_MOVES = [
    AttackMove(
        name="エアスラッシュ", description="", type="ひこう", power=75, accuracy=95
    ),
    RecoverMove(name="はねやすめ", description="HPを半分回復する", type="ひこう"),
]
# ドラゴン
DRAGON_MOVES = [
    AttackMove(
        name="りゅうのいぶき", description="", type="ドラゴン", power=60, accuracy=100
    ),
    AttackMove(
        name="りゅうのはどう", description="", type="ドラゴン", power=85, accuracy=85
    ),
    AttackMove(
        name="ドラゴンダイブ", description="", type="ドラゴン", power=100, accuracy=75
    ),
]
# どく
POIZON_MOVES = [
    AttackMove(
        name="ヘドロこうげき", description="", type="どく", power=65, accuracy=100
    ),
    AttackMove(
        name="ヘドロばくだん", description="", type="どく", power=90, accuracy=100
    ),
]
