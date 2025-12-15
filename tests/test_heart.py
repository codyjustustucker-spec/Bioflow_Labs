from bioflow.sim.heart import pump_flow_ml_s


def integrate_over_period(hr_bpm: float, sv_ml: float, dt: float = 1e-4) -> float:
    period = 60.0 / hr_bpm
    t = 0.0
    total = 0.0
    while t < period:
        total += pump_flow_ml_s(t, hr_bpm=hr_bpm, stroke_volume_ml=sv_ml) * dt
        t += dt
    return total


def test_pump_integral_equals_stroke_volume():
    hr = 60.0
    sv = 80.0
    pumped = integrate_over_period(hr, sv)
    assert abs(pumped - sv) < 1e-2  # numeric integration tolerance


def test_pump_scales_with_stroke_volume():
    hr = 75.0
    sv1 = 50.0
    sv2 = 100.0
    pumped1 = integrate_over_period(hr, sv1)
    pumped2 = integrate_over_period(hr, sv2)
    assert abs(pumped2 / pumped1 - 2.0) < 1e-2


def test_mean_flow_matches_cardiac_output():
    # Mean pump flow over time should be CO = HR*SV/60 (mL/s)
    hr = 120.0
    sv = 70.0
    period = 60.0 / hr

    dt = 1e-4
    t = 0.0
    total = 0.0
    while t < period:
        total += pump_flow_ml_s(t, hr_bpm=hr, stroke_volume_ml=sv) * dt
        t += dt

    mean_flow = total / period
    expected = hr * sv / 60.0
    assert abs(mean_flow - expected) < 1e-1
