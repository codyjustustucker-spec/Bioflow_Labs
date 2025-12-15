from bioflow.sim.vessels import peripheral_flow_nonlinear_ml_s


def test_linear_when_k_zero():
    dP = 50.0
    R0 = 2.0
    Q = peripheral_flow_nonlinear_ml_s(dP, R0, k=0.0)
    assert abs(Q - (dP / R0)) < 1e-12


def test_nonlinear_sublinear_scaling():
    # With k>0, doubling dP produces LESS than double Q (sublinear).
    R0 = 1.0
    k = 0.05

    Q1 = peripheral_flow_nonlinear_ml_s(20.0, R0, k)
    Q2 = peripheral_flow_nonlinear_ml_s(40.0, R0, k)

    assert Q2 < 2.0 * Q1
    assert Q2 > Q1  # still increases
