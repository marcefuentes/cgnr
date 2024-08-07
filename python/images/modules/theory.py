"""Functions for computing fitness and indifference curves."""

import numpy as np


game_map = {
    "allgames": lambda tt, rr, pp, ss: True,
    "harmony": lambda tt, rr, pp, ss: (tt < rr) & (rr > pp) & (pp < ss),
    "deadlock": lambda tt, rr, pp, ss: (tt > rr) & (rr < pp) & (pp > ss),
    "deadlock_ts": lambda tt, rr, pp, ss: (tt > rr)
    & (rr < pp)
    & (pp > ss)
    & (2.0 * pp < tt + ss),
    "prisoner": lambda tt, rr, pp, ss: (tt > rr) & (rr > pp) & (pp > ss),
    "prisoner_ts": lambda tt, rr, pp, ss: (tt > rr)
    & (rr > pp)
    & (pp > ss)
    & (2.0 * rr < tt + ss),
    "snowdrift": lambda tt, rr, pp, ss: (tt > rr) & (rr > pp) & (pp < ss),
    "snowdrift_ts": lambda tt, rr, pp, ss: (tt > rr)
    & (rr > pp)
    & (pp < ss)
    & (2.0 * rr < tt + ss),
    "drift": lambda tt, rr, pp, ss: pp == ss,
    "drift_ts": lambda tt, rr, pp, ss: (pp == ss) & (2.0 * rr < tt + ss),
    "diagonal": lambda tt, rr, pp, ss: rr == pp,
}


def get_fitness(x, y, given, alpha, rho):
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

    if rho > 0.0:
        w = pow(pow(q_a, rho) * (1.0 - alpha) + pow(q_b, rho) * alpha, 1.0 / rho)
        return w

    if q_a == 0.0 or q_b == 0.0:
        return 0.0

    w = pow(pow(q_a, rho) * (1.0 - alpha) + pow(q_b, rho) * alpha, 1.0 / rho)
    return w


def get_trps(high, low, given, alpha, rho):
    """Calculates the fitness of the four possible trait pairs."""

    tt = fitness(high, low, given, alpha, rho)
    rr = fitness(high, high, given, alpha, rho)
    pp = fitness(low, low, given, alpha, rho)
    ss = fitness(low, high, given, alpha, rho)
    return tt, rr, pp, ss


def get_fitness_curve(x, y, given, alpha, rho):
    """Compute fitness."""

    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")

        ws = np.zeros(len(x))
        for i, _ in enumerate(ws):
            ws[i] = get_fitness(x[i], y[i], given, alpha, rho)
        return ws

    if isinstance(x, np.ndarray) and not isinstance(y, np.ndarray):
        ws = np.zeros(len(x))
        for i, _ in enumerate(ws):
            ws[i] = get_fitness(x[i], y, given, alpha, rho)
        return ws

    if not isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        ws = np.zeros(len(y))
        for i, _ in enumerate(ws):
            ws[i] = get_fitness(x, y[i], given, alpha, rho)
        return ws

    w = get_fitness(x, y, given, alpha, rho)
    return w


def get_game_condition(game, tt, rr, pp, ss):
    """Compute the condition of the game."""

    if game not in game_map:
        raise ValueError("Invalid game name.")
    return game_map[game](tt, rr, pp, ss)


def get_icurves(qs, w, alpha, rho):
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


def get_qbeq(given, alpha, rho):
    """Compute q_b*."""

    if given < 1.0:
        mrt = 1.0 - given
        q_b = 1.0 / (1.0 + pow(mrt * alpha / (1.0 - alpha), 1.0 / (rho - 1.0)))
    else:
        q_b = 0.0
    return q_b
