'''
Dans ce module, on va créer la vue du circuit à l'aide de PyQt5. 
On va afficher le circuit, les limites de piste et de secteurs et les voitures.
'''

# import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsItemGroup, QGraphicsLineItem, QGraphicsPathItem, QGraphicsScene, QVBoxLayout, QWidget)
import circuit
import voiture
from pan_zoom_view import PanZoomView

# Largeur et hauteur de la fenêtre
WIDTH = 800
HEIGHT = 450

# Couleurs des tracés (piste, limites, secteurs)
CIR_COLOR = "grey"
TRK_LIM_COLOR = "red"
SEC_LIM_COLOR = "black"

# Pinceaux pour les tracés
CIR_BRUSH = QBrush(QColor(CIR_COLOR))
TRK_LIM_BRUSH = QBrush(QColor(TRK_LIM_COLOR))
SEC_LIM_BRUSH = QBrush(QColor(SEC_LIM_COLOR))

# Vue du circuit
class View(QWidget): 
    def __init__(self, circuit):
        super().__init__()
        self.circuit = circuit

        # Création de la fenêtre
        self.setWindowTitle(f'Course de voiture at {self.circuit.name}')
        self.resize(WIDTH, HEIGHT)

        # Affichage du circuit
        root_layout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = PanZoomView(self.scene)
        # self.view = PyQt5.QtWidgets.QGraphicsView(self.scene)
        
        # Ajout des tracés
        self.add_circuit_items()
        self.add_car_items()
        self.view.fit_scene_in_view()
        # self.view.fitInView(self.view.sceneRect(), PyQt5.QtCore.Qt.KeepAspectRatio)

        root_layout.addWidget(self.view)

        self.view.keyPressEvent = self.keyPressEvent
        self.show()

    def add_circuit_items(self):
        """ Ajoute tous les tracés du circuit """
        circuit_group = QGraphicsItemGroup()
        self.scene.addItem(circuit_group)

        # Limites de la piste
        pen = QPen(QColor(TRK_LIM_COLOR), circuit.TRK_LIM_WIDTH)
        pen.setCapStyle(Qt.RoundCap)

        for line in self.circuit.trackLimits:
            path = QPainterPath()
            path.moveTo(line.coords[0][0], line.coords[0][1])
            for xy in line.coords[1:]:
                path.lineTo(xy[0], xy[1])
            item = QGraphicsPathItem(path, circuit_group)
            item.setPen(pen)
            item.setToolTip(f'{line.name} LINE')

        # Limites des secteurs
        pen = QPen(QColor(SEC_LIM_COLOR), circuit.SEC_LIM_WIDTH)
        # for runway in self.circuit.runways:
        #     (p1, p2) = runway.coords
        for sector_lim_i in range(len(self.circuit.trackLimits[0].coords)):
            (p1, p2) = (self.circuit.trackLimits[0].coords[sector_lim_i], self.circuit.trackLimits[1].coords[sector_lim_i])
            item = QGraphicsLineItem(p1[0], p1[1], p2[0], p2[1], circuit_group)
            item.setPen(pen)
            item.setToolTip(f'SECTOR {None}/{None} LIMIT')

    def add_car_items(self):
        """ Ajoute les voitures sur la ligne de départ """
        car = voiture.Voiture("Ferrari", 150)
        self.scene.addItem(car)
        car.setRect(0, 0, voiture.CAR_WIDTH, voiture.CAR_WIDTH)
        car.setPen(QPen(QColor(car.color), voiture.CAR_WIDTH))
        # car.setPos(-75+(self.circuit.dep[0][0]+self.circuit.dep[1][0])//2, -75+(self.circuit.dep[0][1]+self.circuit.dep[1][1])//2)
        car.setPos((self.circuit.dep[0][0]+self.circuit.dep[1][0])//2,
                   -100 + (self.circuit.dep[0][1]+self.circuit.dep[1][1])//2)
    def move_car_items(self, car):
        """ Déplace la voiture """
        car.move(self.circuit)

    def keyPressEvent(self, event): 
        """ Déplace la voiture avec les touches directionnelles """
        if event.key() == Qt.Key_Right:
            car = self.scene.items()[0]
            self.move_car_items(car)

def main():
    pass

if __name__ == '__main__':
    main()
