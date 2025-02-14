"""
@file app.py
@brief Main entry point for the RSSI application.
@author Divya Dharshini
@date 31-01-2025
"""

# ====================Main Application===============================
# This is the main entry point for the RSSI application.

import sys
from PyQt6.QtWidgets import QApplication
from RSSI_libs.RSSI_GUI import MainWindow

def main ():
    """
    Main function to run the RSSI application.
    This function initializes the QApplication, 
    creates the main window, and starts the event loop.
    """
    RSSI_GUI = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    RSSI_GUI.exec()

if __name__ == "__main__":
    main()