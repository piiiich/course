# Dans ce module on définit la vue du circuit que l'on trace à l'aide de PyQt5

from PyQt5.QtCore import QCoreApplication, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeySequence, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItemGroup,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsRectItem, QGraphicsScene, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QShortcut,
                             QSlider, QVBoxLayout, QWidget)
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


class View(QWidget): # Vue du circuit
    def __init__(self, circuit):
        super().__init__()

        self.circuit = circuit

        # Création de la fenêtre
        self.setWindowTitle(f'Race at {self.circuit.name}')
        self.resize(WIDTH, HEIGHT)

        # Affichage du circuit
        root_layout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = PanZoomView(self.scene)

        # Ajout des tracés
        self.add_circuit_items()
        self.add_car_items()
        self.view.fit_scene_in_view()
        root_layout.addWidget(self.view)

        self.show()

    def add_circuit_items(self):
        circuit_group = QGraphicsItemGroup()
        self.scene.addItem(circuit_group)

        #Track limits
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

        # Sector limits
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
        car = voiture.Voiture("", 150)
        self.scene.addItem(car)
        car.setRect(0, 0, voiture.CAR_WIDTH, voiture.CAR_WIDTH)
        car.setPen(QPen(QColor(car.color), voiture.CAR_WIDTH))
        car.setPos(-75+(self.circuit.dep[0][0]+self.circuit.dep[1][0])//2, -75+(self.circuit.dep[0][1]+self.circuit.dep[1][1])//2)
    
    def move_car_items(self):
        pass
        
def main():
    pass
if __name__ == '__main__':
    main()