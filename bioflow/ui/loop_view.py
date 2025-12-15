from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget

from bioflow.sim.state import State


class LoopView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumWidth(420)
        self._phase = 0.0
        self._q = 0.0
        self._p_art = 0.0
        self._p_ven = 0.0

    def update_from_state(self, s: State) -> None:
        self._q = float(s.Q_periph_ml_s)
        self._p_art = float(s.P_art_mmHg)
        self._p_ven = float(s.P_ven_mmHg)

        # speed scales with flow magnitude (clamped)
        speed = max(min(abs(self._q) * 0.002, 0.08), 0.002)
        self._phase = (self._phase + speed) % 1.0
        self.update()

    def paintEvent(self, _ev) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        w = self.width()
        h = self.height()

        # Loop rectangle
        pad = 40
        x0, y0 = pad, pad
        x1, y1 = w - pad, h - pad

        pen = QPen(Qt.white)
        pen.setWidth(3)
        p.setPen(pen)
        p.drawRoundedRect(x0, y0, x1 - x0, y1 - y0, 18, 18)

        # Labels (simple)
        p.setPen(Qt.white)
        p.drawText(x0 + 10, y0 + 25, f"ART  P={self._p_art:.1f} mmHg")
        p.drawText(x0 + 10, y1 - 10, f"VEN  P={self._p_ven:.1f} mmHg")
        p.drawText(x1 - 180, y0 + 25, f"Q(periph)={self._q:.1f} mL/s")

        # Moving dots along perimeter (visual flow)
        # Use 12 dots, spaced, phase-shifted
        dot_count = 12
        for i in range(dot_count):
            t = (self._phase + i / dot_count) % 1.0
            cx, cy = self._point_on_rect(x0, y0, x1, y1, t)
            p.setBrush(Qt.white)
            p.setPen(Qt.NoPen)
            p.drawEllipse(int(cx) - 4, int(cy) - 4, 8, 8)

        p.end()

    @staticmethod
    def _point_on_rect(x0: int, y0: int, x1: int, y1: int, t: float) -> tuple[float, float]:
        # perimeter param t in [0,1)
        per = 2 * ((x1 - x0) + (y1 - y0))
        d = t * per

        top = (x1 - x0)
        right = (y1 - y0)
        bottom = top
        left = right

        if d < top:  # top edge
            return x0 + d, y0
        d -= top
        if d < right:  # right edge
            return x1, y0 + d
        d -= right
        if d < bottom:  # bottom edge
            return x1 - d, y1
        d -= bottom
        # left edge
        return x0, y1 - d
