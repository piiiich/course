from PyQt5.QtCore import QCoreApplication, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeySequence, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItemGroup,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsRectItem, QGraphicsScene, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QShortcut,
                             QSlider, QVBoxLayout, QWidget)
import circuit
from pan_zoom_view import PanZoomView


WIDTH = 800
HEIGHT = 450

CIR_COLOR = "grey"
TRK_LIM_COLOR = "red"
SEC_LIM_COLOR = "lightgrey"

CIR_BRUSH = QBrush(QColor(CIR_COLOR))
TRK_LIM_BRUSH = QBrush(QColor(TRK_LIM_COLOR))
SEC_LIM_BRUSH = QBrush(QColor(SEC_LIM_COLOR))


class View(QWidget):
    def __init__(self, circuit):
        super().__init__()

        self.circuit = circuit

        self.setWindowTitle(f'Race at {None}')
        self.resize(WIDTH, HEIGHT)

        root_layout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = PanZoomView(self.scene)

        self.show()

    def add_circuit_items(self):
        circuit_group = QGraphicsItemGroup()
        self.scene.addItem(circuit_group)

        #Track limits
        pen = QPen(QColor(TRK_LIM_COLOR), circuit.TRK_LIM_WIDTH)
        pen.setCapStyle(Qt.RoundCap)

        for line in self.circuit.trackLimits:
            path = QPainterPath()
            path.moveTo(line.coords[0].x, line.coords[0].y)
            for xy in line.coords[1:]:
                path.lineTo(xy.x, xy.y)
            item = QGraphicsPathItem(path, circuit_group)
            item.setPen(pen)
            item.setToolTip(f'{line.name} LINE')

        # Sector limits
        pen = QPen(QColor(SEC_LIM_COLOR), circuit.SEC_LIM_WIDTH)
        # for runway in self.circuit.runways:
        #     (p1, p2) = runway.coords
        for sector_lim_i in range(len(self.circuit.trackLimits[0].coords)):
            (p1, p2) = (self.circuit.trackLimits[0].coords[sector_lim_i], self.circuit.trackLimits[1].coords[sector_lim_i])
            item = QGraphicsLineItem(p1.x, p1.y, p2.x, p2.y, circuit_group)
            item.setPen(pen)
            item.setToolTip(f'SECTOR {None}/{None} LIMIT')
        
def main():
    pass
if __name__ == '__main__':
    main()