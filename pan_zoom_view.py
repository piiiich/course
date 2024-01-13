''' 
Dans ce module on définit la vue interactive du circuit qui permettra de zoomer et de se déplacer avec la souris 
'''

import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

class PanZoomView(QGraphicsView):
    """ Une vue interactive qui supporte les fonctions Pan et Zoom"""
    def __init__(self, scene):
        super().__init__(scene)

        # permet d'avoir des lignes plus lisses
        self.setRenderHint(QPainter.Antialiasing)

        # permet de déplacer la vue avec la souris
        self.setDragMode(self.ScrollHandDrag)

    def fit_scene_in_view(self):
        """ On vérifie que la scène est affichée dans son intégralité par la vue """
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def zoom_view(self, factor):
        """ On met à jour le facteur de zoom de la vue """
        self.setTransformationAnchor(self.AnchorUnderMouse)
        super().scale(factor, factor)

    def wheelEvent(self, event):
        """ Permet de zoomer avec la molette de la souris """
        factor = math.pow(1.001, event.angleDelta().y())
        self.zoom_view(factor)
