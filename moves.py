from models import RecoverMove, AttackMove

ALL_MOVES = [
    AttackMove(name="つるのむち", description="", type="くさ", power=45, accuracy=100),
    RecoverMove(name="こうごうせい", description="HPを半分回復する", type="くさ"),
    AttackMove(name="強い技", description="", type="ひこう", power=300, accuracy=100),
]
