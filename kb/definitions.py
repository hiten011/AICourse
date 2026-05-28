from definitions import DIRECTIONS, VECTORS

_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def neighbors(pos: tuple) -> list[tuple]:
    r, c = pos
    return [(r + dr, c + dc) for dr, dc in _DIRS]
