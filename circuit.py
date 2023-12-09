TRK_LIM_WIDTH = 5
SEC_LIM_WIDTH = 2

class TrackLimit:
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

class Circuit:
    def __init__(self, name, trackLimits):
        self.name = name
        self.trackLimits = trackLimits

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
    return Circuit(name, (TrackLimit("EXTERIOR", Ext), TrackLimit("INTERIOR", Int)))

def main():
    pass

if __name__ == '__main__':
    main()

