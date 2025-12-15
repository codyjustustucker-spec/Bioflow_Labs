from __future__ import annotations

from dataclasses import replace
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QSlider, QHBoxLayout, QPushButton
)

from bioflow.sim.orchestrator import SimOrchestrator


class _SliderRow(QWidget):
    """
    Integer QSlider with a scale factor -> float value.
    """

    def __init__(
        self,
        title: str,
        unit: str,
        vmin: float,
        vmax: float,
        v0: float,
        step: float,
    ) -> None:
        super().__init__()

        self.title = title
        self.unit = unit
        self.vmin = vmin
        self.vmax = vmax
        self.step = step

        self.label = QLabel()
        self.slider = QSlider(Qt.Horizontal)

        # map float range to int ticks
        self._imin = 0
        self._imax = int(round((vmax - vmin) / step))
        self.slider.setRange(self._imin, self._imax)

        self.set_value(v0)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        self._refresh_label()

        self.slider.valueChanged.connect(self._refresh_label)

    def _refresh_label(self) -> None:
        self.label.setText(f"{self.title}: {self.value():.2f} {self.unit}")

    def value(self) -> float:
        i = self.slider.value()
        v = self.vmin + i * self.step
        # clamp in float space
        if v < self.vmin:
            v = self.vmin
        if v > self.vmax:
            v = self.vmax
        return v

    def set_value(self, v: float) -> None:
        if v < self.vmin:
            v = self.vmin
        if v > self.vmax:
            v = self.vmax
        i = int(round((v - self.vmin) / self.step))
        self.slider.blockSignals(True)
        self.slider.setValue(i)
        self.slider.blockSignals(False)
        self._refresh_label()


class ControlsPanel(QWidget):
    def __init__(self, sim: SimOrchestrator) -> None:
        super().__init__()
        self.sim = sim

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        title = QLabel("Controls")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        root.addWidget(title)

        box = QGroupBox("Hemodynamics")
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(10)

        p = self.sim.params

        # Sliders (bounds are educational, not clinical)
        self.hr = _SliderRow("Heart Rate", "bpm", 40, 180, p.hr_bpm, 1)
        self.sv = _SliderRow("Stroke Volume", "mL", 20,
                             180, p.stroke_volume_ml, 1)
        self.R = _SliderRow("Resistance (R0)", "mmHg·s/mL",
                            0.2, 6.0, p.peripheral_resistance, 0.05)
        self.Ca = _SliderRow("Arterial Compliance", "mL/mmHg",
                             0.5, 6.0, p.arterial_compliance, 0.05)
        self.pool = _SliderRow(
            "Venous Pooling Target", "% total", 0, 40, p.venous_pooling_target * 100.0, 1)

        for row in (self.hr, self.sv, self.R, self.Ca, self.pool):
            box_layout.addWidget(row)

        root.addWidget(box)

        btn_row = QHBoxLayout()
        self.btn_pause = QPushButton("Pause")
        self.btn_play = QPushButton("Play")
        self.btn_reset = QPushButton("Reset")

        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_play)
        btn_row.addWidget(self.btn_reset)
        root.addLayout(btn_row)

        root.addStretch(1)

        # Wiring
        self.hr.slider.valueChanged.connect(self.apply)
        self.sv.slider.valueChanged.connect(self.apply)
        self.R.slider.valueChanged.connect(self.apply)
        self.Ca.slider.valueChanged.connect(self.apply)
        self.pool.slider.valueChanged.connect(self.apply)

        self.btn_pause.clicked.connect(self.sim.pause)
        self.btn_play.clicked.connect(self.sim.play)
        self.btn_reset.clicked.connect(self._on_reset)

    def _on_reset(self) -> None:
        self.sim.reset(keep_params=True)
        # sync sliders to current params
        p = self.sim.params
        self.hr.set_value(p.hr_bpm)
        self.sv.set_value(p.stroke_volume_ml)
        self.R.set_value(p.peripheral_resistance)
        self.Ca.set_value(p.arterial_compliance)
        self.pool.set_value(p.venous_pooling_target * 100.0)

    def apply(self) -> None:
        # Convert pooling percent back to 0..1 fraction
        pooling_frac = self.pool.value() / 100.0

        self.sim.update_params(
            hr_bpm=self.hr.value(),
            stroke_volume_ml=self.sv.value(),
            peripheral_resistance=self.R.value(),
            arterial_compliance=self.Ca.value(),
            venous_pooling_target=pooling_frac,
        )
