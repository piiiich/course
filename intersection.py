# Dans ce module on teste l'intersection de deux segments de droite

import numpy as np

def clockwise(u, v):
    """ Renvoie 1 si v est à droite de u, -1 si v est à gauche de u, 0 si u et v sont colinéaires """
    d = np.linalg.det([u, v])
    if d < 0:
        return -1
    elif d > 0:
        return 1
    elif u[0] * v[0] < 0 or u[1] * v[1] < 0:
        return -1
    elif np.dot(u, u) < np.dot(v, v):
        return 1
    else:
        return 0

def segment_intersection(A, B, C, D):
    """ Renvoie True si les segments [AB] et [CD] s'intersectent, False sinon """
    AB = B - A
    AC = C - A
    AD = D - A
    CD = D - C
    CA = A - C
    CB = B - C
    return clockwise(AB, AC) * clockwise(AB, AD) <= 0 and clockwise(CD, CA) * clockwise(CD, CB) <= 0

def x_sector(car, dest, init, circuit):
    return segment_intersection(dest, init, circuit.sectorLimits[car.current_sector+1].coords[0], circuit.sectorLimits[car.current_sector+1].coords[1])

def x_tracklimit(car, dest, init, circuit):
    return segment_intersection(dest, init, circuit.trackLimits[car.current_sector].coords[0], circuit.trackLimits[car.current_sector].coords[1])

# Test
#A = np.array([1, 1])
#B = np.array([4, 4])
#C = np.array([2, 5])
#D = np.array([5, 8])

#result = segment_intersection(A, B, C, D)
#print(result)
