import enum
import geometry

LINE_WIDTH = 80

class NamedPoint(geometry.Point):
    """Named point of the airport, with the following attributes:
    - name: str (name of the point)
    - type: STAND | DEICING | RUNWAY_POINT (type of point)
    - x and y: coordinates of the point (inherited from Point)"""

    def __init__(self, name, pt_type, point):
        x, y = map(int, point.split(','))
        super().__init__(x, y)
        self.name = name
        self.type = pt_type

    def __repr__(self):
        return "<airport.Point {0}>".format(self.name)

def xys_to_points(str_xy_list):
    """ xys_to_points(str list) returns Point tuple: converts x,y str list to Point tuple"""

    def xy_to_point(str_xy):
        x, y = map(int, str_xy.split(','))
        return geometry.Point(x, y)

    return tuple(xy_to_point(str_xy) for str_xy in str_xy_list)

class Ext_line(geometry.PolyLine):
    """Exterior portion of the circuit, with the following attributes:
    - ext_line_name: str (name of the line)
    - sector: int (number of the sector this line belongs to)
    - coords: Point tuple (points composing the line, inherited from PolyLine)"""

    def __init__(self, ext_line_name, sector, coords):
        super().__init__(coords)
        self.ext_line_name = ext_line_name
        self.sector = sector

    def __repr__(self):
        return "<cirucit.Line {0}>".format(self.ext_line_name)


class Int_line(geometry.PolyLine):
    """Interior portion of the circuit, with the following attributes:
    - int_line_name: str (name of the line)
    - sector: int (number of the sector this line belongs to)
    - coords: Point tuple (points composing the line, inherited from PolyLine)"""

    def __init__(self, int_line_name, sector, coords):
        super().__init__(coords)
        self.int_line_name = int_line_name
        self.sector = sector

    def __repr__(self):
        return "<cirucit.Line {0}>".format(self.ext_line_name)

class Circuit:
    """Whole circuit description, with the following attributes:
    - name: str (name of the circuit)
    - points_ext: Point tuple (named exterior points of the circuit)
    - points_int: Point tuple (named interior points of the circuit)
    - dep: Point tuple (named departure points of the circuit)"""

    def __init__(self, name, points_ext, points_int, dep, ext_lines, int_lines):
        self.name = name
        self.points_ext = points_ext
        self.points_int = points_int
        self.dep = dep
        self.pt_ext_dict = {p.name: p for p in points_ext}
        self.pt_int_dict = {p.name: p for p in points_int}
        self.dep_dict = {p.name: p for p in dep}
        self.ext_lines = ext_lines
        self.int_lines = int_lines

    def __repr__(self):
        return "<circuit.Circuit {0}>".format(self.name)

    def get_point_ext(self, name):
        return self.pt_ext_dict[name]
    
    def get_point_int(self, name):
        return self.pt_int_dict[name]
    
    def get_dep(self, name):
        return self.dep_dict[name]


def from_file(filename):
    """from_file(str) return Cicuit: reads an circuit description file"""
    print("Loading circuit", filename + '...')
    file = open(filename)
    name = file.readline().strip()
    points_ext, points_int, dep, ext_lines, int_lines = [], [], [], [], []
    for line in file:
        words = line.strip().split()
        try:
            if words[0] == 'E':  # Points interieurs description
                points_ext.append(NamedPoint(words[2], words[1]))
            elif words[0] == 'I':  # Points exterieurs description
                points_int.append(NamedPoint(words[2], words[1]))
            elif words[0] == 'D':  # Points départ description
                dep.append(NamedPoint(words[2], words[1]))
        except Exception as error:
            print(error, line)
    file.close()

    for i in range(len(points_ext)): # Maybe try len(points_ext)-1
        ext_lines.append(Ext_line("ext_line"+str(i), i, xys_to_points([points_ext[i], points_ext[i+1]])))

    for i in range(len(points_int)): # Maybe try len(points_int)-1
        int_lines.append(Int_line("int_line"+str(i), i, xys_to_points([points_int[i], points_int[i+1]])))

    return Circuit(name, tuple(points_ext), tuple(points_int), tuple(dep), tuple(ext_lines), tuple(int_lines))
