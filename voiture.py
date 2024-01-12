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
    
    '''
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

            if in_circuit and towards_end and further :
                max_dist = dist(self.position(), test_dest)
                self.speed = test_speed
                dest = test_dest 
                # dest.append(test_dest) 
        # sort 

        return dest'''
    
    ''' Proposition en compréhension : 
    def sorted_dests(self, init_pos, init_speed):
    liste_coups = [
        [
            tuple(init_pos[i] + (init_speed[i] + point[i]) for i in [0, 1]),
            tuple(init_speed[i] + point[i] for i in [0, 1])
        ]
        for point in self.range
        
        liste_distances = [(dests, dist(init_pos, dests)) for dests in liste_coups]
        n = len(liste_distances)
        
        # Tri bubble
        for i in range(n):
            for j in range(0, n-i, j):
                if liste_distances[j] > liste_distances[j+1]:
                    liste_distances[j], liste_distances[j+1] = liste_distances[j+1], liste_distances[j]
    ]
    return liste_coups  
    '''

    def sorted_dests(self, init_pos, init_speed):
        # Objectif : trier la liste des 9 coups 
        liste_coups = []
        for point in self.range:   # On parcours la matrice des 9 coups envisages
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])   # Vitesse obtenue pour le point sur lequel on boucle 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])   # (x, y) de la destination
            liste_coups.append([test_dest, test_speed])   # On rajoute la destination a la liste des coups

        liste_distances = [(dests, dist(init_pos, dests)) for dests in liste_coups]
        n = len(liste_distances)

        # Tri bubble
        for i in range(n):
            for j in range(0, n-i, j):
                if liste_distances[j] > liste_distances[j+1]:
                    liste_distances[j], liste_distances[j+1] = liste_distances[j+1], liste_distances[j]
        
        return [((coup[0], coup[1]), speed) for (coup, speed, _) in liste_distances]
            

    def find_dest(self, circuit, init_pos, init_speed, depth):
        pos = init_pos
        speed = init_speed
        
        def recursive_destination_test(List, depth):
            level = depth
            if level == 0:
                return self.dest_in_list(List, pos, circuit)
            else :
                current_list = self.sorted_dests(pos, speed)
                for dest in current_list:
                    next_pos, next_speed = dest[0], dest[1]
                    next_list = self.sorted_dests(next_pos, next_speed)
                    return recursive_destination_test(next_list, level-1)
            
        dest = recursive_destination_test(self.sorted_dests(pos, speed), depth)
        return dest

    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        dest = self.find_dest(circuit, init_pos, init_speed, 1)

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

