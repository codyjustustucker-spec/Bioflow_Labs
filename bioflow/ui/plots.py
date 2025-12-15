from __future__ import annotations

from collections import deque

import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout

from bioflow.sim.state import State


class PlotsPanel(QWidget):
    def __init__(self, seconds: float = 10.0, dt_hint: float = 0.01) -> None:
        super().__init__()

        self._maxlen = int(seconds / dt_hint)

        self.t = deque(maxlen=self._maxlen)
        self.p_art = deque(maxlen=self._maxlen)
        self.p_ven = deque(maxlen=self._maxlen)
        self.q_per = deque(maxlen=self._maxlen)

        layout = QVBoxLayout(self)

        pg.setConfigOptions(antialias=True)

        self.p_plot = pg.PlotWidget(title="Pressure (mmHg)")
        self.p_plot.showGrid(x=True, y=True, alpha=0.2)
        self.p_art_curve = self.p_plot.plot()
        self.p_ven_curve = self.p_plot.plot()

        self.q_plot = pg.PlotWidget(title="Flow (mL/s)")
        self.q_plot.showGrid(x=True, y=True, alpha=0.2)
        self.q_curve = self.q_plot.plot()

        layout.addWidget(self.p_plot, 1)
        layout.addWidget(self.q_plot, 1)

    def update_from_state(self, s: State) -> None:
        self.t.append(float(s.t))
        self.p_art.append(float(s.P_art_mmHg))
        self.p_ven.append(float(s.P_ven_mmHg))
        self.q_per.append(float(s.Q_periph_ml_s))

        # update curves
        xs = list(self.t)
        self.p_art_curve.setData(xs, list(self.p_art))
        self.p_ven_curve.setData(xs, list(self.p_ven))
        self.q_curve.setData(xs, list(self.q_per))

    def reset(self) -> None:
        self.t.clear()
        self.p_art.clear()
        self.p_ven.clear()
        self.q_per.clear()

        self.p_art_curve.clear()
        self.p_ven_curve.clear()
        self.q_curve.clear()
