# Dans ce module on va récupérer les limites de la piste et les secteurs et créer l'objet circuit correspondant

import numpy as np

TRK_LIM_WIDTH = 50 # Largeur de la piste
SEC_LIM_WIDTH = 20 # Largeur des secteurs

class TrackLimit: # Limites de la piste
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

class SectorLimit: # Limites des secteurs
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.position = (np.mean([self.coords[0][0], self.coords[1][0]]), 
                         np.mean([self.coords[0][1], self.coords[1][1]]))

class Circuit:
    def __init__(self, name, trackLimits, dep):
        self.name = name
        self.trackLimits = trackLimits
        self.sectorLimits = []
        for sector_index in range(len(self.trackLimits[0].coords)):
            # On crée les secteurs et leurs limites en utilisant les limites de la piste
            self.sectorLimits.append(SectorLimit(str(sector_index), [self.trackLimits[i].coords[sector_index] for i in [0, 1]]))
        self.dep = dep

def coords_line(list):
    # list représente une ligne de coordonnées dans le fichier texte [x0, y0, x1, y1, ...]
    xys = []
    for i in range(len(list)//2):
        xys.append((int(list[2*i]), int(list[2*i+1])))
    # Renvoie une liste de coordonnées (x, y)
    return xys 

def from_file(filename):
    # filename est le nom du fichier texte contenant les données du circuit
    print(f'Loading circuit {filename} ...')
    file = open(filename)
    # On lit le nom du circuit
    name = file.readline().strip() 
    Ext, Int= [], []
    # On lit les limites intérieure et extérieure de la piste et les coordonnées du départ
    for line in file:
        words = line.strip().split()
        if words[0] == "Exterieur":
            Ext = coords_line(words[1:])
        elif words[0] == "Interieur":
            Int = coords_line(words[1:])
        elif words[0] == "Depart":
            Dep = [(int(words[1]), int(words[2])), (int(words[3]), int(words[4]))]
    file.close()
    # On crée le circuit
    return Circuit(name, (TrackLimit("EXTERIOR", Ext), TrackLimit("INTERIOR", Int)), Dep)

def main():
    pass

if __name__ == '__main__':
    main()

