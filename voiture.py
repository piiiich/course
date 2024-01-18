''' Baptiste
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
       

    def dest_is_valid(self, dest, pos, circuit):
        in_circuit = (not X.x_tracklimit(self, dest, pos, circuit))
        towards_end = X.direction_test(self, dest, pos, circuit)
        return (in_circuit and towards_end)


    def coups_possibles(self, init_pos, init_speed, circuit):
        ''' 
        Cette fonction renvoie une liste de listes des 9 coups possibles de la forme
        [destination_testee_(x,y), vitesse_testee, distance_a_l'origine] 
        init_pos : position actuelle de la voiture
        init_speed : vitesse actuelle de la voiture
        circuit : circuit sur lequel se déroule la course
        ''' 
        liste_coups = []
        # On parcours la matrice des 9 coups envisages
        for point in self.range: 
            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])  # Vitesse obtenue pour le point testé 
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])  # (x, y) de la destination testée
            test_dist = dist(init_pos, test_dest)  # Distance à l'origine par rapport au point testé
            # ERROR: Dest is valid donne des points qu'on devrait pas pouvoir atteindre
            
            if self.dest_is_valid(test_dest, init_pos, circuit):
                # On rajoute le point testé et ses caractéristiques a la liste des coups possibles
                liste_coups.append([test_dest, test_speed, test_dist]) 
        
        return liste_coups


    def tri_liste_coups(self, pos, speed, circuit):  
        ''' 
        Cette fonction trie la liste des coups possibles par distance au point de départ décroissante 
        pos : position actuelle de la voiture
        speed : vitesse actuelle de la voiture
        '''
        liste_coups = self.coups_possibles(pos, speed, circuit)
        liste_coups_triee = sorted(liste_coups, key = lambda x : x[2], reverse=True)
        return liste_coups_triee
    

    def dest_in_list(self, List, pos, circuit):
        ''' 
        Cette fonction renvoie la première destination valide de la liste des coups possibles 
        List : liste des coups possibles
        pos : position actuelle de la voiture
        circuit : circuit sur lequel se déroule la course
        '''
        for dest in List:
            if self.dest_is_valid(dest, pos, circuit):
                return dest
            else:
                print("le code marche pas")
                pass
        # Si on rentre dans cette condition, c'est que dest_is_valid ne fonctionne pas correctement car il y a toujours une destination valide
        # Ou qu'on se trouve hors du circuit
        # Si on ne trouve pas de destination valide, on renvoie la position actuelle et une vitesse nulle
        return (self.position(), (0,0))


    def find_dests(self, circuit, init_pos, init_speed, depth):
        ''' 
        Cette fonction renvoie la destination optimale pour la voiture en fonction de son couple (position ,vitesse) initial. 
        On réalise un parcours en profondeur.
        circuit : circuit sur lequel se déroule la course
        init_pos : position actuelle de la voiture
        init_speed : vitesse actuelle de la voiture
        depth : profondeur de l'arbre de recherche
        '''
        # pos = init_pos
        # speed = init_speed
        # Dests_list = []
        
        # def recursive_destination_test(List, depth):
        #     level = depth
        #     # Condition d'arrêt si on atteint la profondeur voulue
        #     if level == 0:
        #         Final_dest = self.dest_in_list(List, pos, circuit)
        #         Dests_list.append(Final_dest)
        #         return Final_dest
            
        #     else :
        #         for dest in List:
        #             if self.dest_is_valid(dest, pos, circuit):
        #                 Dests_list.append(dest)
        #                 next_pos, next_speed = dest[0], tuple(speed[i]+dest[1][i] for i in (0, 1))
        #                 # next_list = self.tri_liste_distances(next_pos, next_speed)
        #                 next_list = self.coups_possibles(next_pos, next_speed)
        #                 next_dest = recursive_destination_test(next_list, level-1)
        #                 if next_dest != None:
        #                     return next_dest
        #                 else :
        #                     Dests_list.pop()
            
        # dest = recursive_destination_test(self.tri_liste_distances(pos, speed), depth)
        def creer_arbre_racine_profondeur(racine, profondeur_max):
            
            if profondeur_max == 0:
                return racine
            
            coups = self.tri_liste_coups(racine.valeur[0], racine.valeur[1], circuit)

            for coup in coups:
                valeur_enfant = coup
                enfant = Noeud(valeur_enfant, racine)
                racine.enfants.append(enfant)
                creer_arbre_racine_profondeur(enfant, profondeur_max - 1)

        # Exemple d'utilisation
        racine = Noeud((init_pos, init_speed, 0))
        profondeur_max = depth
        creer_arbre_racine_profondeur(racine, profondeur_max)
        # Max distance
        print(racine.enfants)
        

        '''
        max_node = [racine]
        print(racine.enfants)
        def depth_first_search(node):
            # Traiter le nœud courant
            # ICI IL FAUT GARDER LE MEILLEUR NOEUD (QUI A LA DISTANCE LA PLUS GRANDE)
            max_node[0] = max(max_node[0], node, key=lambda x: x.valeur[2])

            # Parcourir les enfants du nœud courant
            for child in node.enfants:
                depth_first_search(child)
            
        depth_first_search(racine)
        max_node = max_node[0]
        if max_node == racine:
            print("On est dans le cas où on ne peut pas bouger")
            return max_node.valeur[0], max_node.valeur[1]
        while max_node.parent is not racine:
            max_node = max_node.parent
        return max_node.valeur[0], max_node.valeur[1]
        '''

    def move(self, circuit):
        init_pos = self.position()
        init_speed = self.speed

        prochain_etat = self.find_dests(circuit, init_pos, init_speed, 1)
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


# Méthode pour générer un arbre de profondeur donnée
# IL faut générer un arbre de possibilités
# L'idée c'est que profondeur de l'arbre = nombre de coups d'affilée et chaque noeud de l'arbre correspond à une position et une vitesse
class Noeud:
    def __init__(self, valeur, parent=None):
        self.valeur = valeur
        self.parent = parent
        self.enfants = []
    def __repr__(self):
        return f"Position : {self.valeur[0]}, Speed : {self.valeur[1]}, Distance : {self.valeur[2]}"

    


# # exemple d'utilisation
# tree = create_tree()


# Méthode de parcours en profondeur 



# Après que tu aies trouvé le meilleur noeud, il faut que tu récupères le parent de ce noeud tant 
# qu'on n'est pas juste avant la racine (depth = 1)
# Puisque depth = 0 correspond à la postion actuelle
    
# # Exemple d'utilisation
# tree = Node("A", [
#     Node("B", [ Node("C"), Node("D")]),
#     Node("E", [Node("F"), Node("G"), Node("H") ])
# ])

# depth_first_search(tree)