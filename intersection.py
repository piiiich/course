'''
Dans ce module on teste l'intersection de deux segments de droite à partir de calculs de déterminants
Dans notre cas, on teste si la voiture a traversé une limite de secteur ou de piste
'''

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
    AB = tuple([B[i]-A[i] for i in range(2)])
    AC = tuple([C[i]-A[i] for i in range(2)])
    AD = tuple([D[i]-A[i] for i in range(2)])
    CD = tuple([D[i]-C[i] for i in range(2)])
    CA = tuple([A[i]-C[i] for i in range(2)])
    CB = tuple([B[i]-C[i] for i in range(2)])
    return clockwise(AB, AC) * clockwise(AB, AD) <= 0 and clockwise(CD, CA) * clockwise(CD, CB) <= 0

def direction_test(car, dest, init, circuit):
    """ Renvoie True si la voiture va dans la bonne direction, False sinon """
    u = tuple(dest[i]-init[i] for i in (0, 1))
    v = tuple(circuit.trackLimits[0].coords[car.current_sector+1][i] - circuit.trackLimits[0].coords[car.current_sector][i] for i in (0, 1))
    return np.dot(u, v) > 0

def x_sector(car, dest, init, circuit):
    """ Renvoie un tuple avec True si la voiture a traversé une limite de secteur, False sinon et le nombre de secteurs traversés """
    test = False
    number = 0
    for i in range(10):
        if segment_intersection(dest, init, circuit.sectorLimits[car.current_sector+i+1].coords[0], circuit.sectorLimits[car.current_sector+i+1].coords[1]):
            test = True
            number += 1
    return test, number

def x_tracklimit(car, dest, init, circuit):
    """ Renvoie True si la voiture a traversé une limite de piste, False sinon """
    for i in range(10):
        crosses_ext = segment_intersection(dest, init, circuit.trackLimits[0].coords[car.current_sector+i], circuit.trackLimits[0].coords[car.current_sector+i+1])
        crosses_int = segment_intersection(dest, init, circuit.trackLimits[1].coords[car.current_sector+i], circuit.trackLimits[1].coords[car.current_sector+i+1])
        return (crosses_ext or crosses_int)