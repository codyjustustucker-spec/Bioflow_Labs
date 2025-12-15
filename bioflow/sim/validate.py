from __future__ import annotations
import math
from dataclasses import dataclass

from .state import State, Params


@dataclass(frozen=True)
class Health:
    ok: bool
    level: str          # "OK" | "WARN"
    message: str


def is_finite(x: float) -> bool:
    return math.isfinite(x)


def assess(state: State, params: Params) -> Health:
    # NaN/inf guard
    vals = [
        state.V_art_ml, state.V_ven_ml, state.V_pool_ml,
        state.P_art_mmHg, state.P_ven_mmHg, state.P_pool_mmHg,
        state.Q_periph_ml_s, state.Q_pump_ml_s, state.Q_pool_ml_s,
        params.dt, params.total_volume_ml,
    ]
    if any(not is_finite(v) for v in vals):
        return Health(False, "WARN", "Non-finite value detected (NaN/inf).")

    # Physical sanity
    if state.V_art_ml < 0 or state.V_ven_ml < 0 or state.V_pool_ml < 0:
        return Health(False, "WARN", "Negative volume detected.")

    total = state.V_art_ml + state.V_ven_ml + state.V_pool_ml
    if abs(total - params.total_volume_ml) > 1e-3:
        return Health(False, "WARN", "Volume conservation drift.")

    # Soft warnings (not fatal)
    if state.P_art_mmHg > 250:
        return Health(True, "WARN", "Arterial pressure very high (clamped?).")
    if state.P_art_mmHg < 1 and state.Q_pump_ml_s > 0:
        return Health(True, "WARN", "Pressure very low while pumping (unstable params).")

    # Very low perfusion (user can trigger by high R or high pooling)
    if abs(state.Q_periph_ml_s) < 0.5 and state.Q_pump_ml_s > 5:
        return Health(True, "WARN", "Very low peripheral flow (poor perfusion).")

    # Pooling too high (user can trigger by raising pooling target)
    if state.V_pool_ml / params.total_volume_ml > 0.45:
        return Health(True, "WARN", "Excessive venous pooling (low preload).")

    # Pumping into a 'stuck' system (high R + low compliance tends to do this)
    if state.P_art_mmHg > 180 and abs(state.Q_periph_ml_s) < 2:
        return Health(True, "WARN", "High pressure with low flow (afterload overload).")

    return Health(True, "OK", "Stable.")
