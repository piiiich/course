"""
Nom du projet : Course de voitures à deux joueurs
Auteurs : Gaspard PICHON, Emma PAILLART, Mathis GIRAUD, Julie CASTAGNET
Date de création : de novembre 2023 à janvier 2024
Description : Cet ensemble de modules crée une course de voitures. Les voitures se déplacent sur un circuit en 
essayant d'optimiser leurs trajectoires. Le but pour la voiture est de franchir la ligne d'arrivée en ayant fait le moins de coups possibles.
Contenu et modules utilisés : main.py ; intersection.py ; pan_zoom_view.py ; view.py ; voiture.py ; circuit.py
"""


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
    win = QMainWindow()
    win.setWindowTitle("Race")
    win.setCentralWidget(view)
    win.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
