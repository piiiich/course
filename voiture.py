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
    
    def destination_test(self, circuit, init_pos, init_speed):
        # teste les différentes positions possibles depuis init_pos avec init_speed
        max_dist = 0
        # liste_coups = [] 
        for point in self.range:

            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])

            further = (dist(self.position(), test_dest) > max_dist)
            in_circuit = (not X.x_tracklimit(self, test_dest, init_pos, circuit))
            towards_end = (X.direction_test(self, test_dest, init_pos, circuit))

            if further and in_circuit and towards_end :
                max_dist = dist(self.position(), test_dest)
                self.speed = test_speed
                dest = test_dest 
                # dest.append(test_dest) 
        # sort 

        return dest
    
    def recursive_destination_test(self, circuit, init_pos, init_speed, depth):
        level = depth
        pos = init_pos
        speed = init_speed
        if level == 1:
            return self.destination_test(circuit, pos, speed)
        else :
            pass

    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        dest = self.recursive_destination_test(circuit, init_pos, init_speed, 1)

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