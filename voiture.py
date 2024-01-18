'''
Mathis et Gaspard
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
        # if self.ecurie == "Ferrari" :
        #     self.color = "Red"
        # elif self.ecurie == "Red Bull":
        #     self.color = "Blue"
        # elif self.ecurie == "Mercedes":
        #     self.color = "Cyan"

    # On aura des problèmes d'échelle si on prend un circuit comme celui du prof ou comme celui de Monaco. 
    # les distances (en pixels) ne sont pas équivalentes dans les deux cas si on les ramène à des metres
        # 8 états possibles par défaut de la voiture
        self.range = [(-reach, -reach), (0, -reach), (+reach, -reach),
                      (-reach, 0)     , (0, 0)     , (+reach, 0)     ,
                      (-reach, +reach), (0, +reach), (+reach, +reach)]

    def position(self):
        return (self.x(), self.y())
       

    def liste_distances(self, init_pos, init_speed, circuit):
        ''' Cette fonction renvoie une liste de tuples (point_destination_(x,y), distance_a_l'origine) 
        pour chaque coup possible ''' 
        liste_coups = []
        for point in self.range: # On parcours la matrice des 9 coups envisages
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1]) # Vitesse obtenue pour le point sur lequel on boucle 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])  # (x, y) de la destination
            test_dist = dist(init_pos, test_dest) # Distance à l'origine
            if self.dest_is_valid(test_dest, init_pos, circuit):
                liste_coups.append([test_dest, test_speed, test_dist])     # On rajoute la destination a la liste des coups
        
        return liste_coups


    def coups_ok_sorted(self, pos, speed, circuit):  
        ''' Cette fonction renvoie une liste de tuples (point_destination_(x,y), vitesse, distance) '''
        liste_coups = self.liste_distances(pos, speed, circuit)
        liste_coups_triee = sorted(liste_coups, key = lambda x : x[2], reverse=True)
        return liste_coups_triee
    

    def dest_in_list(self, List, pos, circuit):
        for dest in List:
            if self.dest_is_valid(dest, pos, circuit):
                return dest
            else:
                pass
    
    def dest_is_valid(self, dest, pos, circuit):
        in_circuit = (not X.x_tracklimit(self, dest[0], pos, circuit))
        towards_end = X.direction_test(self, dest[0], pos, circuit)
        return (in_circuit and towards_end)

    def find_dests(self, circuit, init_pos, init_speed, depth):
        ''' 
        Cette fonction renvoie la destination optimale pour la voiture en fonction de sa position 
        et de sa vitesse. On réalise un parcours en profondeur de profondeur depth.
        '''
        pos = init_pos
        speed = init_speed
        Dests_list = []
        
        def recursive_destination_test(pos, speed, depth):
            List = self.tri_liste_distances(pos, speed)
            # Condition d'arrêt si on atteint la profondeur voulue
            if depth == 0:
                return (pos, speed)
            
            else :
                for dest in List:
                        Dests_list.append(dest)
                        next_pos, next_speed = dest[0], tuple(speed[i]+dest[1][i] for i in (0, 1))
                        next_list = self.tri_liste_distances(next_pos, next_speed)
                        next_dest = recursive_destination_test(next_list, depth-1)
                        if next_dest != None:
                            return next_dest
                        else :
                            Dests_list.pop()
            
        dest = recursive_destination_test(pos, speed, depth)
        return dest


    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        prochain_etat = self.find_dests(circuit, init_pos, init_speed, 0)
        dest = prochain_etat[0]
        self.speed = prochain_etat[1]

        self.setPos(self.x() + self.speed[0], self.y() + self.speed[1])

        crosses_sector, sectors_crossed = X.x_sector(self, dest, init_pos, circuit)
        if crosses_sector:
            self.current_sector += sectors_crossed


def dist(A, B):
    return np.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()

