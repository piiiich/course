import geometry

TRK_LIM_WIDTH = 50
SEC_LIM_WIDTH = 10

class TrackLimit:
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

class Circuit:
    def __init__(self, name, trackLimits):
        self.name = name
        self.trackLimits = trackLimits

def xys_to_points(str_xy_list):
    """ xys_to_points(str list) returns Point tuple: converts x,y str list to Point tuple"""

    def xy_to_point(str_xy):
        x, y = map(int, str_xy.split(','))
        return geometry.Point(x, y)

    return tuple(xy_to_point(str_xy) for str_xy in str_xy_list)

def from_file(filename):
    print(f'Loading circuit {filename} ...')
    file = open(filename)
    name = file.readline().strip()
    Ext, Int, Dep = [], [], []
    for line in file:
        words = line.strip().split()
        if words[0] == "Exterieur":
            for x in words[1:2]:
                Ext.append((int(x)))
            for y_index in range(len(Ext)):
                Ext[y_index] += int(words[2::2][y_index])
        elif words[0] == "Interieur":
            for x in words[1:2]:
                Int.append((int(x)))
            for y_index in range(len(Int)):
                Int[y_index] += int(words[2::2][y_index])
        elif words[0] == "Depart":
            Dep = [(int(words[1]), int(words[2])), (int(words[3]), int(words[4]))]
    file.close()
    return Circuit(name, (Ext, Int))

def main():
    pass

if __name__ == '__main__':
    main()