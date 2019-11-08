import numpy as np
# Distance
def groundDistance(x1, x2, norm=2):
    """
    L-norm distance
    Default norm = 2
    """
    return np.linalg.norm(x1 - x2, norm)

def WCD(p0,p1,q0,q1):
    Avg1 = np.dot(np.transpose(p0),p1)
    Avg2 = np.dot(np.transpose(q0),q1)
    return groundDistance(Avg1,Avg2)

def getWCD(P,Q):
    return WCD(P[0],P[1],Q[0],Q[1])
if __name__ == '__main__':
    features1 = np.array([[100, 40, 22],
                          [211, 20, 2],
                          [32, 190, 150],
                          [2, 100, 100]])
    weights1 = np.array([0.4, 0.3, 0.2, 0.1])

    features2 = np.array([[0, 0, 0],
                          [50, 100, 80],
                          [255, 255, 255]])
    weights2 = np.array([0.5, 0.3, 0.2])

    signature1 = (features1, weights1)
    signature2 = (features2, weights2)
    print getWCD(signature1, signature2)
