'''
Dans ce module on va récupérer les limites de la piste et des secteurs et créer l'objet circuit correspondant
'''

import numpy as np
import intersection as intersection  

# Largeur de la piste
TRK_LIM_WIDTH = 50

# Largeur des secteurs
SEC_LIM_WIDTH = 20 

# Limites de la piste
class TrackLimit: 
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

# Limites d'un secteur
class SectorLimit: 
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

# Créer un circuit
class Circuit:
    def __init__(self, name, trackLimits, dep):
        self.name = name
        self.trackLimits = trackLimits
        self.sectorLimits = []
        for sector_index in range(len(self.trackLimits[0].coords)):
            # On crée les secteurs et leurs limites en utilisant les limites de la piste
            self.sectorLimits.append(SectorLimit(str(sector_index), [self.trackLimits[i].coords[sector_index] for i in [0, 1]]))
        # Point de départ 
        self.dep = dep

    # Correction JBG
    def dest_sector(self, dest, init, init_sector, circuit):
        # Renvoie l'indice de portion de dest
        sector = init_sector
        while True:
            sector = (sector + 1) % len(circuit.sectorLimits)
            a, b = circuit.sectorLimits[sector].coords
            if not intersection.segment_intersection(init, dest, a, b): break
        return sector - 1

    def tracklimit(self, dest, init, sector, circuit):
        # Renvoie si le déplacement sort du circuit
        a, b = circuit.sectorLimits[sector].coords
        c, d = circuit.sectorLimits[(sector + 1) % len(circuit.sectorLimits)].coords
        return (intersection.segment_intersection(init, dest, a, c) or
                intersection.segment_intersection(init, dest, b, d))


def coords_line(lst):
    '''list représente une ligne de coordonnées dans le fichier texte [x0, y0, x1, y1, ...]'''
    # On récupère une coordonnée sur deux pour avoir des couples (x, y)
    return [(int(lst[2*i]), int(lst[2*i+1])) for i in range(len(lst)//2)]


def from_file(filename):
    ''' Créer un circuit à partir d'un fichier texte contenant les caractéristiques du circuit'''
    print(f'Loading circuit {filename} ...')
    with open(filename) as file:
        # On lit le nom du circuit
        name = file.readline().strip()
        # On initialise les limites extérieures et intérieures à None
        ext_limits, int_limits, dep = None, None, None
        # On lit les limites intérieure et extérieure de la piste et les coordonnées du départ
        for line in file:
            words = line.strip().split()
            if words[0] == "Exterieur":
                ext_limits = coords_line(words[1:])
            elif words[0] == "Interieur":
                int_limits = coords_line(words[1:])
            elif words[0] == "Depart":
                dep = [(int(words[1]), int(words[2])), (int(words[3]), int(words[4]))]
        # On vérifie si les limites extérieures et intérieures sont spécifiées
        if ext_limits is None or int_limits is None:
            raise ValueError("Both exterior and interior limits must be specified in the file.")
        # On crée le circuit
        return Circuit(name, (TrackLimit("EXTERIOR", ext_limits), TrackLimit("INTERIOR", int_limits)), dep)



def main():
    pass

if __name__ == '__main__':
    main()
