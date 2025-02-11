# main app.py file

# sys -> interact with system -> command-line arguments

from PyQt6.QtWidgets import QApplication
from RSSI_libs.RSSI_GUI import MainWindow
import sys


if __name__ == "__main__":
    RSSI_GUI = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    RSSI_GUI.exec()