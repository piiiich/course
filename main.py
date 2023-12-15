import circuit
import sys
from view import View
from PyQt5.QtWidgets import QApplication, QMainWindow

#CIR_FILE = "course/DATA/Monaco.txt"
CIR_FILE = "DATA/Monaco.txt"

def main():
    app = QApplication(sys.argv)
    cir = circuit.from_file(CIR_FILE)
    view = View(cir)
    print(view.circuit.sectorLimits[1].coords)
    win = QMainWindow()
    win.setWindowTitle("Race")
    win.setCentralWidget(view)
    win.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
