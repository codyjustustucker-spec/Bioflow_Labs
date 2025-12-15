from __future__ import annotations
import math


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def pressure_from_volume(V_ml: float, V0_ml: float, C_ml_per_mmHg: float) -> float:
    """
    Simple compliance model:
      P = (V - V0) / C, with floor at 0.
    """
    C = max(C_ml_per_mmHg, 1e-9)
    P = (V_ml - V0_ml) / C
    return max(P, 0.0)


def peripheral_flow_nonlinear_ml_s(dP_mmHg: float, R0: float, k: float) -> float:
    """
    Nonlinear resistance model:
      R_eff = R0 * (1 + k*|Q|)
      Q = dP / R_eff

    This is implicit (Q depends on R_eff depends on Q), but it has a closed-form solution.

    For dP >= 0: Q >= 0 solves:
      (R0*k) Q^2 + (R0) Q - dP = 0
    Mirror for dP < 0.
    """
    R0 = max(R0, 1e-9)
    k = max(k, 0.0)

    if k == 0.0:
        return dP_mmHg / R0

    sign = 1.0 if dP_mmHg >= 0.0 else -1.0
    dP = abs(dP_mmHg)

    a = R0 * k
    b = R0
    c = -dP

    disc = b * b - 4.0 * a * c
    disc = max(disc, 0.0)

    Q = (-b + math.sqrt(disc)) / (2.0 * a)  # positive root
    return sign * Q
