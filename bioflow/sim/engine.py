from __future__ import annotations
from dataclasses import replace
from .state import State, Params
from .heart import pump_flow_ml_s
from .vessels import pressure_from_volume, peripheral_flow_nonlinear_ml_s


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def compute_derived(s: State, p: Params) -> State:
    P_art = pressure_from_volume(
        s.V_art_ml, p.V0_art_ml, p.arterial_compliance)
    P_ven = pressure_from_volume(s.V_ven_ml, p.V0_ven_ml, p.venous_compliance)
    P_pool = pressure_from_volume(s.V_pool_ml, p.V0_pool_ml, p.pool_compliance)

    dP = P_art - P_ven
    Q_periph = peripheral_flow_nonlinear_ml_s(
        dP, p.peripheral_resistance, p.resistance_nonlinearity)

    Q_pump = pump_flow_ml_s(
        t_s=s.t,
        hr_bpm=p.hr_bpm,
        stroke_volume_ml=p.stroke_volume_ml,
        systole_fraction=p.systole_fraction,
    )

    # Pooling wants some fraction of TOTAL blood volume in the pool
    target_pool = clamp(p.venous_pooling_target, 0.0, 0.6) * p.total_volume_ml
    tau = max(p.pooling_tau_s, 1e-6)
    Q_pool = (target_pool - s.V_pool_ml) / tau  # + means ven -> pool

    return replace(
        s,
        P_art_mmHg=P_art,
        P_ven_mmHg=P_ven,
        P_pool_mmHg=P_pool,
        Q_periph_ml_s=Q_periph,
        Q_pump_ml_s=Q_pump,
        Q_pool_ml_s=Q_pool,
    )


def step(state: State, params: Params) -> State:
    s = compute_derived(state, params)
    dt = params.dt

    Qp = s.Q_pump_ml_s        # ven -> art
    Qr = s.Q_periph_ml_s      # art -> ven
    Qpool = s.Q_pool_ml_s     # ven -> pool (if +)

    dV_art = (Qp - Qr) * dt
    dV_ven = (Qr - Qp - Qpool) * dt
    dV_pool = (Qpool) * dt

    V_art = s.V_art_ml + dV_art
    V_ven = s.V_ven_ml + dV_ven
    V_pool = s.V_pool_ml + dV_pool

    # Clamp physical
    V_art = clamp(V_art, 0.0, params.total_volume_ml)
    V_ven = clamp(V_ven, 0.0, params.total_volume_ml)
    V_pool = clamp(V_pool, 0.0, params.total_volume_ml)

    # Exact conservation correction (protects clamp edges)
    total = V_art + V_ven + V_pool
    if total != 0.0:
        scale = params.total_volume_ml / total
        V_art *= scale
        V_ven *= scale
        V_pool *= scale

    s2 = replace(s, t=s.t + dt, V_art_ml=V_art,
                 V_ven_ml=V_ven, V_pool_ml=V_pool)
    return compute_derived(s2, params)
