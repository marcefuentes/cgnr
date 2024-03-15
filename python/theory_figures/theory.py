
import numpy as np

alphamin = 0.1
alphamax = 0.9
logesmin = -5.0
logesmax = 5.0

def fitness(x, y, given, alpha, rho):
    qA = 1.0 - y
    qB = y*(1.0 - given) + x*given
    w = qA*qB
    if not isinstance(qA, np.ndarray):
        qA = np.array([qA])
    if not isinstance(qB, np.ndarray):
        qB = np.array([qB])
    if not isinstance(w, np.ndarray):
        w = np.array([w])
    if not isinstance(alpha, np.ndarray):
        alpha = np.full(w.shape, alpha)
    if not isinstance(rho, np.ndarray):
        rho = np.full(w.shape, rho)
    m = (w > 0.0) & (rho == 0.0)
    w[m] = pow(qA[m], 1.0 - alpha[m])*pow(qB[m], alpha[m])
    m = ((w > 0.0) & (rho < 0.0)) | (rho > 0.0)
    w[m] = pow((1.0 - alpha[m])*pow(qA[m], rho[m]) + alpha[m]*pow(qB[m], rho[m]), 1.0/rho[m])
    return w

def qBeq(given, alpha, rho):
    if given < 1.0:
        MRT = 1.0 - given
        Q = pow(MRT*alpha/(1.0 - alpha), 1.0/(rho - 1.0))
        qB = 1.0/(1.0 + Q)
    else:
        qB = alpha*0.0
    return qB

def indifference(qs, w, alpha, rho):
    qB = np.full(qs.shape, 1000.0)
    for i, q in enumerate(qs):
        if rho == 0.0:
            qB[i] = pow(w/pow(q, 1.0 - alpha), 1.0/alpha)
        else:
            A = pow(w, rho)
            B = (1.0 - alpha)*pow(q, rho)
            if A <= B:
                if rho < 0.0:
                    qB[i] = 1000.0
                else:
                    qB[i] = -0.1
            else:
                qB[i] = pow((A - B)/alpha, 1.0/rho)
    return qB
