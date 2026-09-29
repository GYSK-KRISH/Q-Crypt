"""
====================================================================
Q-Crypt: Desktop GUI Application Launcher
====================================================================
Run this script to launch the Q-Crypt graphical user interface:
    python main_gui.py
====================================================================
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gui import start_gui

if __name__ == "__main__":
    start_gui()
