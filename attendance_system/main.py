import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from attendance_system package
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from attendance_system.ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


