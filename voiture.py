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
    
    def sorted_dests(self, init_pos, init_speed):
        # Trier la liste des 9 coups 
        liste_coups = []
        # On parcours la matrice des 9 coups envisages
        for point in self.range:
            # Vitesse obtenue pour le point sur lequel on boucle 
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])
            # Destination ocle 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])
            # On rajoute la destination a la liste des coups
            liste_coups.append([test_dest, test_speed])
        
        # max_dist = 0
        liste_distances = []
        # liste_coups_triee = []
        for dests in liste_coups:
            distance =  dist(init_pos, dests) #distance entre point de départ et point d'arrivée
            liste_distances.append((dests , distance))
        
        n = len(liste_distances)
        # tri bubble
        for i in range(n):
            for j in range(0, n-i, j):
                if liste_distances[j] > liste_distances[j + 1]:
                    liste_distances[j], liste_distances[j+1] = liste_distances[j+1], liste_distances[j]
        
        return [coup for coup in liste_distances[2]]
            

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

def bubble_sort(input_list):
    n = len(input_list)

    for i in range(n):
        # La boucle externe parcourt toute la liste
        for j in range(0, n-i-1):
            # La boucle interne parcourt la liste jusqu'à n-i-1
            # Échange les éléments si ils sont dans le mauvais ordre
            if input_list[j] > input_list[j+1]:
                input_list[j], input_list[j+1] = input_list[j+1], input_list[j]

def main():
    pass

if __name__ == "__main__":
    main()

