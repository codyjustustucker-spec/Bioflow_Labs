from bioflow.sim.state import State, Params
from bioflow.sim.engine import compute_derived


def test_pressure_zero_below_unstressed_volume():
    p = Params(V0_art_ml=700.0, arterial_compliance=2.0)
    s = State(V_art_ml=600.0, V_ven_ml=3000.0, V_pool_ml=0.0)
    s = compute_derived(s, p)
    assert s.P_art_mmHg == 0.0


def test_pressure_linear_above_unstressed_volume():
    p = Params(V0_art_ml=700.0, arterial_compliance=2.0)
    s = State(V_art_ml=900.0, V_ven_ml=3000.0, V_pool_ml=0.0)
    s = compute_derived(s, p)
    # (900-700)/2 = 100 mmHg
    assert abs(s.P_art_mmHg - 100.0) < 1e-9


def test_flow_direction_matches_pressure_gradient():
    p = Params()
    s = State(V_art_ml=2000.0, V_ven_ml=2000.0, V_pool_ml=1000.0)
    s = compute_derived(s, p)
    # If arterial pressure > venous pressure, peripheral flow should be positive
    assert (s.P_art_mmHg - s.P_ven_mmHg) * s.Q_periph_ml_s >= 0.0
