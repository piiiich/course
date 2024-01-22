'''
Dans ce module, on crée la classe Voiture pour définir les voitures de la course et leurs déplacements. 
'''

from PyQt5.QtWidgets import QGraphicsEllipseItem
import numpy as np
import intersection as X # X représentant une intersection de segments

# Largeur de la voiture
CAR_WIDTH = 70


# Classe Etat pour définir les états de la voiture : position, vitesse, secteur et distance à l'origine
class Etat(QGraphicsEllipseItem):
    def __init__(self, pos, speed, sector):
        self.pos = pos
        self.speed = speed
        self.sector = sector
        self.dist = dist(pos, speed)  # Calcule la fistance à l'origine, definie en bas du programme


    def __repr__(self):
        return f"Etat({self.pos}, {self.speed}, {self.sector}, {self.dist})"


# Classe Voiture pour définir les caractéristiques des voitures de la course
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
            self.color = "#009999"

        """
        On aura des problèmes d'échelle selon le circuit choisi.  
        Effectivement, les distances en pixels ne sont pas équivalentes d'un circuit à l'autre,
        proportionnellement à des distances en mètres
        """
        # 8 états possibles par défaut de la voiture
        self.range = [(-reach, -reach), (0, -reach), (+reach, -reach),
                      (-reach, 0)     , (0, 0)     , (+reach, 0)     ,
                      (-reach, +reach), (0, +reach), (+reach, +reach)]


    def __repr__(self):
        return f"Voiture({self.color}, {self.speed}, {self.current_sector})"


    def position(self):
        return (self.x(), self.y())   #Les methodes x() et y() sont héritées de QGraphicsEllipseItem
       

    def liste_distances(self, init_pos, init_speed):
        ''' 
        Cette fonction renvoie une liste de listes  
        [point_destination_(x,y), vecteur_vitesse, distance_a_l'origine] 
        pour chaque coup
        ''' 
        
        liste_coups = []
        for point in self.range:                                           # On parcourt la matrice des 9 coups envisagés
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])   # Vitesse obtenue pour le point sur lequel on boucle 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1]) # (x, y) de la destination
            test_dist = dist(init_pos, test_dest)                          # Distance à l'origine
            liste_coups.append([test_dest, test_speed, test_dist])         # On rajoute la destination à la liste des coups
        
        return liste_coups


    def find_dest(self, circuit, depth):
        '''
        Renvoie un triplet (position, vitesse, portion) envisageable
        pour le prochain déplacement de la voiture. On parcours en profondeur. 
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
        ''' Déplace la voiture sur le circuit '''
        dest, self.speed, self.current_sector = self.find_dest(circuit, 6)
        self.setPos(self.x() + self.speed[0], self.y() + self.speed[1])


def dist(A, B):
    return np.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)


'''
Essais pour l'algorithme Min Max :
    def avoid_collision(self, other_car, circuit, depth):
        # Fonction pour éviter les collisions avec une autre voiture
        # Implémentation de l'algorithme Min Max 
        pass 

        
    def minimax(state, depth, maximizing_player):
        if depth == 0 or game_over(state):
            return evaluate_state(state)

        if maximizing_player:
            max_eval = float('-inf')
            for action in possible_actions(state):
                eval = minimax(result(state, action), depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for action in possible_actions(state):
                eval = minimax(result(state, action), depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

            
    def decide_next_move(current_state):
        best_value = float('-inf')
        best_action = None
        for action in possible_actions(current_state):
            eval = minimax(result(current_state, action), depth=3, maximizing_player=False)
            if eval > best_value:
                best_value = eval
                best_action = action
        return best_action

        
    def move_safely(self, circuit, other_cars):
        # Eviter les collisions avec d'autres voitures
        for other_car in other_cars:
            self.avoid_collision(other_car, circuit, depth=3)

        # Déplacer la voiture 
        self.move(circuit) 
'''

def main():
    pass

if __name__ == "__main__":
    main()

