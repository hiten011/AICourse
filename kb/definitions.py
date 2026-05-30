GRID_SIZE = 32
SPAWN = (13, 13)

_DIRS = [(0, -1), (1, 0), (-1, 0), (0, 1)]


def neighbors(pos: tuple) -> list[tuple]:
    r, c = pos
    return [(r + dr, c + dc) for dr, dc in _DIRS]
