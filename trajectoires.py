
import numpy as np

def clockwise(u, v):
    '''
    fonction de test si les segments u et v sont séquents
    '''
    d = numpy.linalg.det([u, v])
    if d < 0 or u[0]*v[0] < 0 or u[1]*v[1] < 0 :
        return -1 #si orientation dans le sens inverse des aiguilles d'une montre
    
    elif d > 0 or numpy.dot(u, u) < numpy.dot(v, v):
        return 1  #si orientation dans le sens des aiguilles d'une montre
    
    else :
        return 0 #si colinéaires
  
def are_vectors_sequent(u, v):
    orientation = clockwise(u, v)
    return orientation in [1, -1, 0]

# Test
u = numpy.array([1, 1])
v = numpy.array([0, 2])
result = are_vectors_sequent(u, v)
print(result)

