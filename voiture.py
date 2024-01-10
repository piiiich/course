from PyQt5.QtWidgets import QGraphicsEllipseItem
import numpy as np
import intersection as X

CAR_WIDTH = 70

class Voiture(QGraphicsEllipseItem):
    def __init__(self, ecurie, reach):
        super().__init__()
        self.ecurie = ecurie
        self.color = "Black"
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

    def position(self):
        return (self.x(), self.y())

    def move(self, circuit):
        max_dist = 0
        init_pos = self.position()
        init_speed = self.speed
        for point in self.range:
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])
            if (dist(self.position(), test_dest) > max_dist) and (not X.x_tracklimit(self, test_dest, init_pos, circuit)) and (X.direction_test(self, test_dest, init_pos, circuit)):
                # Faire avec le produit scalaire avec les bords
                max_dist = dist(self.position(), test_dest)
                self.speed = test_speed
                dest = test_dest
        self.setPos(self.x() + self.speed[0], self.y() + self.speed[1])
        crosses_sector, sectors_crossed = X.x_sector(self, dest, init_pos, circuit)
        if crosses_sector:
            self.current_sector += sectors_crossed
        
def dist(A, B):
    return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()