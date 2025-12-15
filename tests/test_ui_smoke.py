import sys
import pytest
from PySide6.QtWidgets import QApplication

from bioflow.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_main_window_constructs(qapp):
    w = MainWindow()
    # Don’t show; just ensure it builds and has a title
    assert "BioFlow" in w.windowTitle()
    w.close()
