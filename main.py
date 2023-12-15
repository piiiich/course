# Dans ce module on va créer la fenêtre principale de l'application : on appelle tous nos fichiers

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
    # Create the QMainWindow to hold both radar view and flight inspector
    
    win = QMainWindow()
    win.setWindowTitle("Race")
    win.setCentralWidget(view)
    win.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
