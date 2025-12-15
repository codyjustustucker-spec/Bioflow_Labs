# BioFlow Lab v1

Interactive cardiovascular dynamics simulator that turns pressure/flow concepts into real-time intuition.

This is an educational, system-dynamics model (not a medical device, not a diagnostic tool).

## What it shows (v1)
- Closed-loop circulation (arterial ↔ venous)
- Heart pump waveform (HR + stroke volume)
- Compliance-driven pressure (volume → pressure)
- Nonlinear peripheral resistance (pressure → flow, sublinear scaling)
- Venous pooling reservoir (volume sequestered away from preload)
- Real-time visualization + plots + volume distribution

## Why it matters (the “pain”)
Cardiovascular behavior is hard to build intuition for because it’s dynamic, nonlinear, and delayed.
BioFlow Lab makes cause → propagation → consequence visible instantly.

## Tech
- Python
- PySide6 (Qt UI)
- NumPy
- PyQtGraph
- Pytest

## Install
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest


File structure (final v1) ------------------------------------------

bioflow-lab/
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── app.py
│
├── bioflow/
│   ├── __init__.py
│   ├── sim/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── heart.py
│   │   ├── vessels.py
│   │   ├── engine.py
│   │   ├── orchestrator.py
│   │   ├── presets.py
│   │   └── validate.py
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py
│       ├── controls.py
│       ├── loop_view.py
│       ├── plots.py
│       └── volume_bar.py
│
├── tests/
│   └── (all your tests)
│
└── assets/
    ├── screenshots/
    ├── gifs/
    └── diagrams/
