import numpy as np

def clockwise(u, v):
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
    AB = B - A
    AC = C - A
    AD = D - A
    CD = D - C
    CA = A - C
    CB = B - C
    #print(clockwise(AB, AC))
    #print(clockwise(AB, AD))
    #print(clockwise(CD, CA))
    #print(clockwise(CD, CB))
    if (
        clockwise(AB, AC) * clockwise(AB, AD) <= 0
        and clockwise(CD, CA) * clockwise(CD, CB) <= 0
    ):
        return True
    else:
        return False

# Test
#A = np.array([1, 1])
#B = np.array([4, 4])
#C = np.array([2, 5])
#D = np.array([5, 8])

#result = segment_intersection(A, B, C, D)
#print(result)
