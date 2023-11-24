import numpy as  np
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QMainWindow

import circuit

if __name__ == "__main__":
    circuit = circuit.from_file("DATA/circuit.txt")

"""   
    # Create the QMainWindow to hold both radar view and flight inspector
    win = QMainWindow()
    win.setWindowTitle("Race Qt MainWindow & Dock")
    win.setCentralWidget(rad)
    win.addDockWidget(Qt.DockWidgetArea(1), insp_dock)
    # The QMainWindow is the root widget of this QApplication, so it must be explicitly shown...
    # win.resize(1000, 600)
    # win.show()         # either as a normal window...
    win.showMaximized()  # ...or in full screen mode

    # Create a second view (in another window)
    # second_view = PanZoomView(rad.scene)
    # second_view.scale(0.1, -0.1)
    # second_view.move(300, 300)
    # second_view.show()

    # Enter the main loop
    app.exec_()
"""