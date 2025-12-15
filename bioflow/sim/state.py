from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Params:
    dt: float = 0.01
    total_volume_ml: float = 5000.0

    # Unstressed volumes (ml)
    V0_art_ml: float = 700.0
    V0_ven_ml: float = 3000.0
    V0_pool_ml: float = 0.0

    # Compliances (mL / mmHg)
    arterial_compliance: float = 2.0
    venous_compliance: float = 80.0
    pool_compliance: float = 200.0

    # Resistance
    peripheral_resistance: float = 1.0        # baseline R0
    resistance_nonlinearity: float = 0.015    # k (bigger => more nonlinear)

    # Heart (pump)
    hr_bpm: float = 70.0
    stroke_volume_ml: float = 70.0
    systole_fraction: float = 0.35

    # Pooling
    # fraction of TOTAL blood that wants to sit in pool (0..0.6)
    venous_pooling_target: float = 0.10
    # seconds (how fast pooling equilibrates)
    pooling_tau_s: float = 6.0


@dataclass
class State:
    t: float = 0.0

    V_art_ml: float = 1000.0
    V_ven_ml: float = 3800.0
    V_pool_ml: float = 200.0

    P_art_mmHg: float = 0.0
    P_ven_mmHg: float = 0.0
    P_pool_mmHg: float = 0.0

    Q_periph_ml_s: float = 0.0
    Q_pump_ml_s: float = 0.0
    Q_pool_ml_s: float = 0.0  # ven <-> pool exchange (+ means ven->pool)
