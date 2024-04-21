""" Update data in artists. """

from matplotlib import cm
import numpy as np

def update(given, kwargs):
    """ Update data in artists. """

    budget_private = (1.0 - kwargs["x_data"])*(1.0 - given)
    for i, alpha in enumerate(kwargs["alphas"]):
        for j, rho in enumerate(kwargs["rhos"]):
            qb_eq = get_qbeq(given, alpha, rho)
            kwargs["artists"][0, 0, i, j].set_ydata(budget_private + qb_eq * given)
            for w_isocline in kwargs["w_isoclines"]:
                kwargs["artists"][0, 1, i, j].set_ydata(indifference(kwargs["x_data"], w_isocline, alpha, rho))
                print(indifference(kwargs["x_data"], w_isocline, alpha, rho))
                print(w_isocline)
            w_max = fitness(qb_eq, qb_eq, given, alpha, rho)
            kwargs["artists"][0, 0, i, j].set_ydata(indifference(w_max, given, alpha, rho))
            color = cm.Reds(w_max)
            kwargs["artists"][0, 0, i, j].set_color(color)
            kwargs["artists"][0, 1, i, j].set_ydata(fitness(qb_eq, kwargs["x_data"], given, alpha, rho))
    
    return kwargs["artists"].flatten()

def fitness(x, y, given, alpha, rho):
    """Compute fitness."""

    q_a = 1.0 - y
    q_b = y*(1.0 - given) + x*given
    w = q_a*q_b
    if not isinstance(q_a, np.ndarray):
        q_a = np.array([q_a])
    if not isinstance(q_b, np.ndarray):
        q_b = np.array([q_b])
    if not isinstance(w, np.ndarray):
        w = np.array([w])
    if not isinstance(alpha, np.ndarray):
        alpha = np.full(w.shape, alpha)
    if not isinstance(rho, np.ndarray):
        rho = np.full(w.shape, rho)
    m = (w > 0.0) & (rho == 0.0)
    w[m] = pow(q_a[m], 1.0 - alpha[m])*pow(q_b[m], alpha[m])
    m = ((w > 0.0) & (rho < 0.0)) | (rho > 0.0)
    w[m] = pow((1.0 - alpha[m])*pow(q_a[m], rho[m]) + alpha[m]*pow(q_b[m], rho[m]), 1.0/rho[m])
    return w

def get_qbeq(given, alpha, rho):
    """Compute qB*."""

    if given < 1.0:
        mrt = 1.0 - given
        q_b = 1.0/(1.0 + pow(mrt*alpha/(1.0 - alpha), 1.0/(rho - 1.0)))
    else:
        q_b = alpha*0.0
    return q_b

def indifference(qs, w, alpha, rho):
    """Compute indifference curves."""

    q_b = np.full(qs.shape, 1000.0)
    for i, q in enumerate(qs):
        if rho == 0.0:
            q_b[i] = pow(w/pow(q, 1.0 - alpha), 1.0/alpha)
        else:
            numerator = pow(w, rho) - (1.0 - alpha)*pow(q, rho)
            if numerator <= 0.0:
                if rho < 0.0:
                    q_b[i] = 1000.0
                else:
                    q_b[i] = -0.1
            else:
                q_b[i] = pow(numerator/alpha, 1.0/rho)
    return q_b
