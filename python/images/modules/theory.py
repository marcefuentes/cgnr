"""Functions for computing fitness and indifference curves."""

import numpy as np


def calculate_fitness(x, y, given, alpha, rho):
    """Calculate fitness for a single pair of x and y."""

    q_a = 1.0 - y
    q_b = y * (1.0 - given) + x * given

    if q_a == 0.0 and q_b == 0.0:
        return 0.0

    if rho == 0.0:
        if q_a == 0.0 or q_b == 0.0:
            return 0.0
        w = pow(q_a, 1.0 - alpha) * pow(q_b, alpha)
        return w

    if q_a == 0.0:
        denominator = alpha * pow(q_b, rho)
    elif q_b == 0.0:
        denominator = (1.0 - alpha) * pow(q_a, rho)
    else:
        denominator = (1.0 - alpha) * pow(q_a, rho) + alpha * pow(q_b, rho)

    w = pow(denominator, 1.0 / rho)
    return w


def fitness(x, y, given, alpha, rho):
    """Compute fitness."""

    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")

        ws = np.zeros(len(x))
        for i, _ in enumerate(ws):
            ws[i] = calculate_fitness(x[i], y[i], given, alpha, rho)
        return ws

    if isinstance(x, np.ndarray) and not isinstance(y, np.ndarray):
        ws = np.zeros(len(x))
        for i, _ in enumerate(ws):
            ws[i] = calculate_fitness(x[i], y, given, alpha, rho)
        return ws

    if not isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        ws = np.zeros(len(y))
        for i, _ in enumerate(ws):
            ws[i] = calculate_fitness(x, y[i], given, alpha, rho)
        return ws

    w = calculate_fitness(x, y, given, alpha, rho)
    return w


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


def qbeq(given, alpha, rho):
    """Compute q_b*."""

    if given < 1.0:
        mrt = 1.0 - given
        q_b = 1.0 / (1.0 + pow(mrt * alpha / (1.0 - alpha), 1.0 / (rho - 1.0)))
    else:
        q_b = alpha * 0.0
    return q_b
