from bioflow.sim.state import Params
from bioflow.sim import presets


def test_high_resistance_increases_R():
    p = Params(peripheral_resistance=1.0)
    p2 = presets.high_resistance(p)
    assert p2.peripheral_resistance > p.peripheral_resistance


def test_low_compliance_decreases_Ca():
    p = Params(arterial_compliance=2.0)
    p2 = presets.low_compliance(p)
    assert p2.arterial_compliance < p.arterial_compliance


def test_weak_pump_reduces_sv():
    p = Params(stroke_volume_ml=70.0)
    p2 = presets.weak_pump(p)
    assert p2.stroke_volume_ml < p.stroke_volume_ml
