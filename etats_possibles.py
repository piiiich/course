import circuit, voiture 
import numpy as np

def calculer_trajectoire(position_actuelle, coups_restants):
    # Condition d'arrêt : la profondeur maximale est atteinte
    if coups_restants == 0:
        return [position_actuelle]

    # Déplacements possibles
    deplacements = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    trajectoire_optimale = []

    for deplacement in deplacements:
        # Calculer la nouvelle position
        nouvelle_position = effectuer_deplacement(position_actuelle, deplacement)

        # Récursion pour les coups suivants
        trajectoire_suivante = calculer_trajectoire(nouvelle_position, coups_restants - 1)

        # Combinaison des trajectoires actuelle et suivante
        trajectoire_optimale.extend([(position_actuelle, deplacement)] + traj for traj in trajectoire_suivante)

    return trajectoire_optimale


def effectuer_deplacement(position_actuelle, deplacement):
    # Simuler le déplacement de la voiture
    nouvelle_position = (
        position_actuelle[0] + deplacement[0],
        position_actuelle[1] + deplacement[1]
    )
    return nouvelle_position

# Position initiale
position_initiale = (0, 0)
# Nombre de coups à l'avance
coups_a_l_avance = 3

# Calculer la trajectoire optimale
trajectoire_optimale = calculer_trajectoire(position_initiale, coups_a_l_avance)

# Afficher la trajectoire optimale
for i, (position, deplacement) in enumerate(trajectoire_optimale):
    print(f'Étape {i + 1}: Position = {position}, Déplacement = {deplacement}')
