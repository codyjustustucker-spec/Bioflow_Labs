from bioflow.sim.state import State, Params
from bioflow.sim.engine import step


def test_total_volume_conserved():
    p = Params(dt=0.01, total_volume_ml=5000.0)
    s = State(V_art_ml=1200.0, V_ven_ml=3800.0)
    total0 = s.V_art_ml + s.V_ven_ml

    for _ in range(10_000):
        s = step(s, p)

    total1 = s.V_art_ml + s.V_ven_ml
    assert abs(total1 - total0) < 1e-6
    assert abs(total1 - p.total_volume_ml) < 1e-6
