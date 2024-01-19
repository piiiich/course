'''Prof
Dans ce module, on crée la classe Voiture pour définir les voitures de la course et leurs déplacements. 
'''

from PyQt5.QtWidgets import QGraphicsEllipseItem
import numpy as np
import intersection as X

# Largeur de la voiture
CAR_WIDTH = 70

class Voiture(QGraphicsEllipseItem):
    def __init__(self, ecurie, reach):
        super().__init__()
        self.ecurie = ecurie
        self.color = "Black"
        self.speed = (0, 0)
        self.current_sector = 0
        if self.ecurie == "Ferrari" :
            self.color = "Red"
        elif self.ecurie == "Red Bull":
            self.color = "Blue"
        elif self.ecurie == "Mercedes":
            self.color = "Cyan"

    # On aura des problèmes d'échelle si on prend un circuit comme celui du prof ou comme celui de Monaco. 
    # les distances (en pixels) ne sont pas équivalentes dans les deux cas si on les ramène à des metres
        # 8 états possibles par défaut de la voiture
        self.range = [(-reach, -reach), (0, -reach), (+reach, -reach),
                      (-reach, 0)     , (0, 0)     , (+reach, 0)     ,
                      (-reach, +reach), (0, +reach), (+reach, +reach)]

    def position(self):
        return (self.x(), self.y())
       

    def liste_distances(self, init_pos, init_speed):
        ''' Cette fonction renvoie une liste de tuples (point_destination_(x,y), distance_a_l'origine) 
        pour chaque coup possible ''' 
        liste_coups = []
        for point in self.range: # On parcours la matrice des 9 coups envisages
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1]) # Vitesse obtenue pour le point sur lequel on boucle 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])  # (x, y) de la destination
            test_dist = dist(init_pos, test_dest) # Distance à l'origine
            liste_coups.append([test_dest, test_speed, test_dist])     # On rajoute la destination a la liste des coups
        
        return liste_coups


    def tri_liste_distances(self, pos, speed):  
        ''' Cette fonction renvoie une liste de tuples (point_destination_(x,y), vitesse, distance) '''
        liste_coups = self.liste_distances(pos, speed)
        liste_coups_triee = sorted(liste_coups, key = lambda x : x[2], reverse=True)
        return liste_coups_triee
    

    def dest_in_list(self, List, pos, circuit):
        for dest in List:
            if self.dest_is_valid(dest, pos, circuit):
                return dest
            else:
                pass
    
    def dest_is_valid(self, dest, pos, sector, circuit):
        in_circuit = (not X.tracklimit(self, dest, pos, sector, circuit))
        towards_end = X.direction_test(self, dest, pos, circuit) and (not X.backward(dest, pos, sector, circuit))
        return (in_circuit and towards_end)

    # def find_dests(self, circuit, init_pos, init_speed, depth):
    #     ''' 
    #     Cette fonction renvoie la destination optimale pour la voiture en fonction de sa position 
    #     et de sa vitesse. On réalise un parcours en profondeur de profondeur depth.
    #     '''
    #     pos = init_pos
    #     speed = init_speed
    #     Dests_list = []
        
    #     def recursive_destination_test(List, depth):
    #         level = depth
    #         # Condition d'arrêt si on atteint la profondeur voulue
    #         if level == 0:
    #             Final_dest = self.dest_in_list(List, pos, circuit)
    #             Dests_list.append(Final_dest)
    #             return Final_dest
            
    #         else :
    #             for dest in List:
    #                 if self.dest_is_valid(dest, pos, circuit):
    #                     Dests_list.append(dest)
    #                     next_pos, next_speed = dest[0], tuple(speed[i]+dest[1][i] for i in (0, 1))
    #                     next_list = self.tri_liste_distances(next_pos, next_speed)
    #                     next_dest = recursive_destination_test(next_list, level-1)
    #                     if next_dest != None:
    #                         return next_dest
    #                     else :
    #                         Dests_list.pop()
            
    #     dest = recursive_destination_test(self.tri_liste_distances(pos, speed), depth)
    #     return dest

    # Correction JBG
    def find_dest(self, circuit, depth):
        '''
        Renvoie un triplet (position, vitesse, portion) envisageable
        pour le prochain déplacement de la voiture
        '''
        def rec_find(pos, speed, sector, depth):
            # Renvoie None ou le triplet
            if depth == 0 or len(circuit.sectorLimits) <= sector:
                return (pos, speed, sector)
            else:
                moves = []

                for dest, new_speed, dist in self.liste_distances(pos, speed):
                    new_sector = X.dest_sector(dest, pos, sector, circuit)

                    if not (X.tracklimit(dest, pos, new_sector, circuit) or
                           X.backward(dest, pos, sector, circuit)):
                        
                        moves.append((dest, new_speed, new_sector, dist))

                moves.sort(key=lambda x:-x[3])

                for dest, new_speed, new_sector, dist in moves:
                    if rec_find(dest, new_speed, new_sector, depth - 1):
                        return (dest, new_speed, new_sector)

        return rec_find(self.position(), self.speed, self.current_sector, depth)
                

    
    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        # prochain_etat = self.find_dests(circuit, init_pos, init_speed, 5)
        dest, self.speed, self.current_sector = self.find_dest(circuit, 15)
        # self.speed = prochain_etat[1]

        self.setPos(self.x() + self.speed[0], self.y() + self.speed[1])

        
        # crosses_sector, sectors_crossed = X.x_sector(self, dest, init_pos, circuit)
        # if crosses_sector:
        #    self.current_sector += sectors_crossed

def dist(A, B):
    return np.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()

