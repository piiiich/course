import numpy as np

#u = [ux, uy]
#v = [vx, vy]

def clockwise(u,v):
    d = np.det(u, v)
    if d < 0 :
        return -1
    elif d > 0 :
        return 1
    #elif ux*vx < 0 or uy*vy < 0 :
    elif u[0]*v[0] < 0 or u[1]*v[1] < 0 :
        return -1
    #elif u.u < v.v :
    elif np.dot(u, u) < np.dot(v, v) :
        return 1
    else :
        return 0
    
