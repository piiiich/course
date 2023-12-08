import geometry as geo
import view
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QMainWindow

def main():
    # Create the QMainWindow to hold both radar view and flight inspector
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Race Qt MainWindow & Dock")
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
