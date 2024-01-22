'''
Dans ce module on teste l'intersection de deux segments de droite à partir de calculs de déterminants.
Dans notre cas, on teste si la voiture a traversé une limite de secteur ou de piste.
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


def vect(a, b):
    """ Calcule le vecteur AB """
    return tuple(b[i] - a[i] for i in range(2))


def segment_intersection(A, B, C, D):
    """ Renvoie True si les segments [AB] et [CD] s'intersectent, False sinon """

    AB = vect(A, B)
    AC = vect(A, C)
    AD = vect(A, D)
    CD = vect(C, D)
    CA = vect(C, A)
    CB = vect(C, B)

    return clockwise(AB, AC) * clockwise(AB, AD) <= 0 and clockwise(CD, CA) * clockwise(CD, CB) <= 0


# def direction_test(car, dest, init, circuit):
#     """ Renvoie True si la voiture va dans la bonne direction, False sinon """
#     u = vect(init, dest)
#     v = vect(circuit.trackLimits[0].coords[car.current_sector], circuit.trackLimits[0].coords[car.current_sector+1])
#     return np.dot(u, v) > 0


def dest_sector(dest, init, init_sector, circuit):
    ''' Renvoie l'indice de portion de la destination '''

    sector = init_sector
    while True:
        sector = (sector + 1) % len(circuit.sectorLimits)
        a, b = circuit.sectorLimits[sector].coords
        if not segment_intersection(init, dest, a, b): break
    
    return sector - 1


def tracklimit(dest, init, sector, circuit):
    ''' Renvoie si le déplacement sort du circuit '''

    a, b = circuit.sectorLimits[sector].coords
    c, d = circuit.sectorLimits[(sector + 1) % len(circuit.sectorLimits)].coords

    return (segment_intersection(init, dest, a, c) or
            segment_intersection(init, dest, b, d))


def backward(dest, init, init_sector, circuit):
    ''' Renvoie si la voiture revient vers la portion précédente '''

    a, b = circuit.sectorLimits[init_sector].coords
    ab = vect(a, b)
    d_init = np.linalg.det([ab, vect(a, init)])
    d_dest = np.linalg.det([ab, vect(a, dest)])

    return d_init * d_dest < 0


def main():
    pass

if __name__ == '__main__':
    main()
