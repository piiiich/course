from PyQt5.QtWidgets import QGraphicsEllipseItem
import numpy as np
import intersection as X

CAR_WIDTH = 100

class Voiture(QGraphicsEllipseItem):
    def __init__(self, ecurie, reach):
        super().__init__()
        self.ecurie = ecurie
        self.color = "Black"
        self.position = (self.x(), self.y())
        self.speed = (0, 0)
        self.current_sector = 0

        # if self.ecurie == "Ferrari" :
        #     self.color = "Red"
        # elif self.ecurie == "Red Bull":
        #     self.color = "Blue"
        # elif self.ecurie == "Mercedes":
        #     self.color = "Cyan"

    # On aura des problèmes d'échelle si on prend un circuit comme celui du prof ou comme celui de Monaco. les distances (en pixels) ne sont
    # pas équivalentes dans les deux cas si on les ramène à des metres
        # 8 états possibles par défaut de la voiture
        self.range = [(-reach, -reach), (0, -reach), (+reach, -reach),
                      (-reach, 0)     , (0, 0)     , (+reach, 0)     ,
                      (-reach, +reach), (0, +reach), (+reach, +reach)]
        
    def move(self, circuit):
        max_dist = 0
        init = self.position
        dest = init
        for point in self.range:
            if (dist(self.position, point) > max_dist) and ('''Condition pour vérifier que ça avance dans le bon sens''') and ('''contition pour tracklimits'''):
                # Faire avec le produit scalaire avec les bords
                max_dist = dist(self.position, point)
                dest = tuple(self.speed[i] + point[i] for i in [0, 1])
        self.speed = dest
        self.setPos(self.x() + self.speed[0], self.y() + self.speed[1])
        if X.segment_intersection(dest, init, circuit.sectorLimits[self.current_sector+1].coords[0], circuit.sectorLimits[self.current_sector+1].coords[1]):
            self.current_sector += 1

# Problèmes lignes 35, 38, 39, 40, 41 avec notamment la définition du vectuer vitesse
        
        
def dist(A, B):
    return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()