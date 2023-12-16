import circuit, voiture 

#déterminer tous les états suivants possibles 
#tester si on ne croise pas les bords ext et int de la section 
#si on passe par une limite de secteur, tester les bords ext et int de ce meme secteur
#si on passe par une deuxième limite de secteur, tester aussi 
#ne pas pouvoir retourner au secteur précédent, ou en arrière 
# AB.v >= 0 et CD.v >= 0

def suivi_de_la_voiture(section_precedente, bool_section_traversee):
    """ on suit le numero de section dans laquelle la voiture est : """
    if bool_section_traversee: 
        section_precedente += 1


def etats_possibles(voiture):
    """ à partir de l'etat d'une voiture a un moment donne, on determine les etats suivants possibles"""
    etats_possibles = [0 for _ in range(9)] # calculer les coordonnees des 9 nouvelles positions envisageables
    #déterminer dans quelle section on est 
    pass  