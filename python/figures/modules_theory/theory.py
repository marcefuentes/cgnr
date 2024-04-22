"""Functions for computing fitness and indifference curves."""

import numpy as np


def fitness(x, y, given, alpha, rho):
    """Compute fitness."""

    q_a = 1.0 - y
    q_b = y * (1.0 - given) + x * given
    w = q_a * q_b
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
    w[m] = pow(q_a[m], 1.0 - alpha[m]) * pow(q_b[m], alpha[m])
    m = ((w > 0.0) & (rho < 0.0)) | (rho > 0.0)
    w[m] = pow(
        (1.0 - alpha[m]) * pow(q_a[m], rho[m]) + alpha[m] * pow(q_b[m], rho[m]),
        1.0 / rho[m],
    )
    return w


def qbeq(given, alpha, rho):
    """Compute q_b*."""

    if given < 1.0:
        mrt = 1.0 - given
        q_b = 1.0 / (1.0 + pow(mrt * alpha / (1.0 - alpha), 1.0 / (rho - 1.0)))
    else:
        q_b = alpha * 0.0
    return q_b


def indifference(qs, w, alpha, rho):
    """Compute indifference curves."""

    q_b = np.full(qs.shape, 1000.0)
    for i, q in enumerate(qs):
        if rho == 0.0:
            q_b[i] = pow(w / pow(q, 1.0 - alpha), 1.0 / alpha)
        else:
            numerator = pow(w, rho) - (1.0 - alpha) * pow(q, rho)
            if numerator <= 0.0:
                if rho < 0.0:
                    q_b[i] = 1000.0
                else:
                    q_b[i] = -0.1
            else:
                q_b[i] = pow(numerator / alpha, 1.0 / rho)
    return q_b
