from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Params:
    dt: float = 0.01
    total_volume_ml: float = 5000.0

    arterial_compliance: float = 2.0
    venous_compliance: float = 80.0
    peripheral_resistance: float = 1.0

    # Heart (pump)
    hr_bpm: float = 70.0
    stroke_volume_ml: float = 70.0
    systole_fraction: float = 0.35


@dataclass
class State:
    t: float = 0.0
    V_art_ml: float = 1000.0
    V_ven_ml: float = 4000.0

    P_art_mmHg: float = 0.0
    P_ven_mmHg: float = 0.0
    Q_periph_ml_s: float = 0.0
    Q_pump_ml_s: float = 0.0
