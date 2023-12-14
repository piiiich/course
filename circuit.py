import numpy as np

TRK_LIM_WIDTH = 50
SEC_LIM_WIDTH = 20

class TrackLimit:
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

class SectorLimit:
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.position = (np.mean([self.coords[0][0], self.coords[1][0]]), np.mean([self.coords[0][1], self.coords[1][1]]))

class Circuit:
    def __init__(self, name, trackLimits, dep):
        self.name = name
        self.trackLimits = trackLimits
        self.sectorLimits = []
        for sector_index in range(len(self.trackLimits[0].coords)):
            self.sectorLimits.append(SectorLimit(str(sector_index), [self.trackLimits[i].coords[sector_index] for i in [0, 1]]))
        self.dep = dep

def coords_line(list):
    xys = []
    for i in range(len(list)//2):
        xys.append((int(list[2*i]), int(list[2*i+1])))
    return xys

def from_file(filename):
    print(f'Loading circuit {filename} ...')
    file = open(filename)
    name = file.readline().strip()
    Ext, Int= [], []
    for line in file:
        words = line.strip().split()
        if words[0] == "Exterieur":
            Ext = coords_line(words[1:])
        elif words[0] == "Interieur":
            Int = coords_line(words[1:])
        elif words[0] == "Depart":
            Dep = [(int(words[1]), int(words[2])), (int(words[3]), int(words[4]))]
    file.close()
    return Circuit(name, (TrackLimit("EXTERIOR", Ext), TrackLimit("INTERIOR", Int)), Dep)

def main():
    pass

if __name__ == '__main__':
    main()

