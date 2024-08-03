"""Repeat a value for a matrix."""


def fill_matrix(value, matrix):
    """Repeat a value for a matrix."""

    return [[value for _ in row] for row in matrix]
