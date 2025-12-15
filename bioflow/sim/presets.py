from __future__ import annotations
from dataclasses import replace
from .state import Params


def baseline(p: Params) -> Params:
    # Keep whatever baseline you started with
    return p


def high_resistance(p: Params) -> Params:
    # Stenosis proxy: harder to push through periphery
    return replace(
        p,
        peripheral_resistance=3.0,
        resistance_nonlinearity=max(p.resistance_nonlinearity, 0.03),
    )


def low_compliance(p: Params) -> Params:
    # Stiff arteries proxy: higher pressures for same volume
    return replace(
        p,
        arterial_compliance=1.0,
    )


def weak_pump(p: Params) -> Params:
    # Heart failure proxy: lower SV, optionally higher HR
    return replace(
        p,
        stroke_volume_ml=35.0,
        hr_bpm=max(p.hr_bpm, 90.0),
    )
