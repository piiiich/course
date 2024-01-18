'''
Mathis et Gaspard
Dans ce module, on crée la classe Voiturame pour définir les voitures de la course et leurs déplacements. 
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
        
        #On trie ensuite la liste des coups par ordre décroissant de distances parcourues
        liste_coups_triee = sorted(liste_coups, key = lambda x : x[2], reverse=True)
        return liste_coups_triee


    
    def dest_is_valid(self, dest, pos, circuit):
        """
        Cette méthode vérifie que la destination proposée est valide c'est à dire qu'elle est dans le circuit et qu'elle ne va pas en arrière
        On utilise X ~ intersection pour vérifier qu'on ne croise pas les limites du circuit
        """
        in_circuit = (not X.x_tracklimit(self, dest, pos, circuit))
        towards_end = X.direction_test(self, dest, pos, circuit)

        return (in_circuit and towards_end)  #Le booléen retourné ne sera vrai que si les deux conditions sont réunies.
    

    def find_dests(self, circuit, init_pos, init_speed, depth):
        ''' 
        Cette méthode renvoie la destination optimale pour la voiture en fonction de sa position 
        et de sa vitesse. On réalise un parcours en profondeur de profondeur "depth".
        '''
        pos = init_pos
        speed = init_speed
        path = []
        
        def recursive_destination_test(pos, speed, depth):
            level = depth
            # Condition d'arrêt si on atteint la profondeur voulue
            if level == 0:
                return [pos, speed]
                    
            else :
                List = self.liste_distances(pos, speed, circuit)
                for dest in List:
                    next_pos, next_speed = dest, tuple(speed[i]+dest[1][i] for i in (0, 1))
                    return [pos, speed], recursive_destination_test(next_pos, next_speed, level-1)
            # trouver un format pour que find_dest renvoie un tableau de tous les points du chemin à parcourir
        for dest in recursive_destination_test(pos, speed, depth):
            path.append(dest)
        return path


    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        prochain_etat = self.find_dests(circuit, init_pos, init_speed, 2)
        print(prochain_etat)
        dest = prochain_etat[-1][0]
        self.speed = prochain_etat[-1][1]        

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

