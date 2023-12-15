from PyQt5.QtWidgets import QGraphicsEllipseItem
import numpy as np
import view

CAR_WIDTH = 100

class Voiture(QGraphicsEllipseItem):
    def __init__(self, ecurie, reach):
        super().__init__()
        self.ecurie = ecurie
        self.color = "Black"
        self.position = (self.x(), self.y())
        self.speed = ((0, 0), (0, 0))

        # if self.ecurie == "Ferrari" :
        #     self.color = "Red"
        # elif self.ecurie == "Red Bull":
        #     self.color = "Blue"
        # elif self.ecurie == "Mercedes":
        #     self.color = "Cyan"

    # On aura des problèmes d'échelle si on prend un circuit comme celui du prof ou comme celui de Monaco. les distances (en pixels) ne sont
    # pas équivalentes dans les deux cas si on les ramène à des metres
        self.range = [(-reach, -reach), (0, -reach), (+reach, -reach),
                      (-reach, 0)     , (0, 0)     , (+reach, 0)     ,
                      (-reach, +reach), (0, +reach), (+reach, +reach)]
        
    def move(self):
        max_dist = 0
        sector_end = (0, 0) #----- A COMPLETER -----
        dest = self.position
        for point in self.range:
            if (dist(self.position, point) > max_dist) and (dist(dest, sector_end) < dist(self.position, sector_end)) :
                # Faire avec le produit scalaire avec les bords
                max_dist = dist(self.position, point)
                dest = point
        self.setPos(self.x()+dest[0], self.y()+dest[1])
        
        

def dist(A, B):
    return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()