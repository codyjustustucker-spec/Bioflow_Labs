from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from bioflow.sim.orchestrator import SimOrchestrator
from bioflow.sim.validate import assess

from .loop_view import LoopView
from .plots import PlotsPanel
from .volume_bar import VolumeBar
from .controls import ControlsPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BioFlow Lab")
        self.resize(1200, 700)

        self.sim = SimOrchestrator()
        self.sim.play()

        self.loop_view = LoopView()
        self.plots = PlotsPanel()
        self.volbar = VolumeBar()

        root = QWidget()
        layout = QHBoxLayout(root)

        self.controls = ControlsPanel(self.sim)

        self.status = QLabel("OK")
        self.status.setStyleSheet("padding: 6px; font-weight: 600;")

        loop_wrap = QWidget()
        loop_layout = QVBoxLayout(loop_wrap)
        loop_layout.setContentsMargins(0, 0, 0, 0)
        loop_layout.addWidget(self.status, 0)
        loop_layout.addWidget(self.loop_view, 1)

        layout.addWidget(self.controls, 1)
        layout.addWidget(loop_wrap, 2)
        layout.addWidget(self.plots, 2)
        layout.addWidget(self.volbar, 1)

        self.setCentralWidget(root)

        self.timer = QTimer(self)
        self.timer.setInterval(16)  # ~60 FPS UI
        self.timer.timeout.connect(self.on_tick)
        self.timer.start()

    def on_tick(self) -> None:
        # Run multiple sim steps per UI frame for stability
        steps_per_frame = 3
        self.sim.tick(steps_per_frame)
        s = self.sim.state

        h = assess(s, self.sim.params)
        if h.level == "OK":
            self.status.setText("OK — Stable")
            self.status.setStyleSheet("padding: 6px; font-weight: 600;")
        else:
            self.status.setText(f"WARN — {h.message}")
            self.status.setStyleSheet("padding: 6px; font-weight: 600;")

        self.loop_view.update_from_state(s)
        self.plots.update_from_state(s)
        self.volbar.update_from_state(s, self.sim.params)
