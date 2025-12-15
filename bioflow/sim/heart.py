from __future__ import annotations
import math


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def pump_flow_ml_s(
    t_s: float,
    hr_bpm: float,
    stroke_volume_ml: float,
    systole_fraction: float = 0.35,
) -> float:
    """
    Returns instantaneous pump flow (mL/s) from veins -> arteries.
    Waveform: half-sine during systole, 0 during diastole.

    Key property: integral over one beat == stroke_volume_ml.
    """
    hr = clamp(hr_bpm, 20.0, 250.0)
    sv = clamp(stroke_volume_ml, 0.0, 400.0)
    sf = clamp(systole_fraction, 0.10, 0.70)

    if hr <= 0.0 or sv <= 0.0:
        return 0.0

    period = 60.0 / hr
    systole = sf * period
    phase = t_s % period

    if phase >= systole:
        return 0.0

    # Half-sine shape on [0, systole]
    x = phase / systole  # 0..1
    shape = math.sin(math.pi * x)  # 0..1..0

    # Scale so ∫ shape dt over systole == 2*systole/pi
    # We want ∫ Q dt = SV => A*(2*systole/pi) = SV => A = SV*pi/(2*systole)
    A = sv * math.pi / (2.0 * systole)
    return A * shape
