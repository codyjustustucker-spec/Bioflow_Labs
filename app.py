# app.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow


def main() -> int:
    app = QApplication(sys.argv)

    win = QMainWindow()
    win.setWindowTitle("BioFlow Lab")
    win.resize(1200, 700)
    win.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
