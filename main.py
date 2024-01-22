''' 
Dans ce module on va créer la fenêtre principale de l'application : on appelle tous nos fichiers
'''

import circuit
import sys
from view import View
from PyQt5.QtWidgets import QApplication, QMainWindow

# Nom du fichier texte contenant les caractéristiques de notre circuit
CIR_FILE = "DATA/Monaco.txt"

def main():
    app = QApplication(sys.argv)
    cir = circuit.from_file(CIR_FILE)
    view = View(cir)
    win = QMainWindow()
    win.setWindowTitle(" Course de F1 - Monaco Grand Prix ")
    win.setCentralWidget(view)
    win.showMaximized()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
