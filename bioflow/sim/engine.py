from __future__ import annotations
from dataclasses import replace
from .state import State, Params
from .heart import pump_flow_ml_s


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def compute_derived(s: State, p: Params) -> State:
    P_art = s.V_art_ml / max(p.arterial_compliance, 1e-9)
    P_ven = s.V_ven_ml / max(p.venous_compliance, 1e-9)

    R = max(p.peripheral_resistance, 1e-9)
    Q_periph = (P_art - P_ven) / R  # arteries -> veins

    Q_pump = pump_flow_ml_s(
        t_s=s.t,
        hr_bpm=p.hr_bpm,
        stroke_volume_ml=p.stroke_volume_ml,
        systole_fraction=p.systole_fraction,
    )  # veins -> arteries

    return replace(
        s,
        P_art_mmHg=P_art,
        P_ven_mmHg=P_ven,
        Q_periph_ml_s=Q_periph,
        Q_pump_ml_s=Q_pump,
    )


def step(state: State, params: Params) -> State:
    s = compute_derived(state, params)
    dt = params.dt

    Qp = s.Q_pump_ml_s
    Qr = s.Q_periph_ml_s

    # Closed-loop transfers
    # periphery: arteries -> veins (Qr)
    # pump: veins -> arteries (Qp)
    dV_art = (Qp - Qr) * dt
    dV_ven = (Qr - Qp) * dt

    V_art = s.V_art_ml + dV_art
    V_ven = s.V_ven_ml + dV_ven

    # Stability clamps
    V_art = clamp(V_art, 0.0, params.total_volume_ml)
    V_ven = clamp(V_ven, 0.0, params.total_volume_ml)

    # Conservation correction (mostly protects clamp edge cases)
    total = V_art + V_ven
    if total != 0:
        scale = params.total_volume_ml / total
        V_art *= scale
        V_ven *= scale

    s2 = replace(s, t=s.t + dt, V_art_ml=V_art, V_ven_ml=V_ven)
    return compute_derived(s2, params)
