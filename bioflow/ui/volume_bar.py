from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from bioflow.sim.state import State, Params


class VolumeBar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumWidth(220)
        self._art = 0.0
        self._ven = 0.0
        self._pool = 0.0
        self._total = 1.0

        # colors
        self.ARTERIAL_COLOR = QColor(200, 40, 40)
        self.VENOUS_COLOR = QColor(50, 90, 180)
        self.POOL_COLOR = QColor(120, 70, 140)

    def update_from_state(self, s: State, p: Params) -> None:
        self._art = float(s.V_art_ml)
        self._ven = float(s.V_ven_ml)
        self._pool = float(s.V_pool_ml)
        self._total = float(p.total_volume_ml)
        self.update()

    def paintEvent(self, _ev) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self.width()
        h = self.height()

        painter.fillRect(0, 0, w, h, Qt.black)

        pad = 20
        bar_w = w - 2 * pad
        bar_h = h - 2 * pad

        x = pad
        y = pad

        # background
        painter.setBrush(Qt.darkGray)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(x, y, bar_w, bar_h, 14, 14)

        # fractions
        tot = max(self._total, 1e-9)
        f_art = self._art / tot
        f_ven = self._ven / tot
        f_pool = self._pool / tot

        # stacked segments
        seg_art = int(bar_h * f_art)
        seg_ven = int(bar_h * f_ven)
        seg_pool = bar_h - seg_art - seg_ven

        # draw from bottom up
        yy = y + bar_h

        painter.setBrush(self.POOL_COLOR)   # pool
        yy -= seg_pool
        painter.drawRect(x, yy, bar_w, seg_pool)

        painter.setBrush(self.VENOUS_COLOR)  # veins
        yy -= seg_ven
        painter.drawRect(x, yy, bar_w, seg_ven)

        painter.setBrush(self.ARTERIAL_COLOR)  # arteries
        yy -= seg_art
        painter.drawRect(x, yy, bar_w, seg_art)

        painter.setPen(Qt.black)
        painter.drawText(25, 35, "Volume Split")
        painter.drawText(25, 55, f"ART:  {self._art:.0f} mL")
        painter.drawText(25, 75, f"VEN:  {self._ven:.0f} mL")
        painter.drawText(25, 95, f"POOL: {self._pool:.0f} mL")

        painter.end()
