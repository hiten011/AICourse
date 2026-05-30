from definitions import DIRECTIONS, VECTORS

GRID_SIZE = 32
SPAWN = (13, 13)

def neighbors(pos: tuple, facing_idx: int = None) -> list[tuple]:
    r, c = pos
    order = [(facing_idx + i) % 4 for i in range(1, 5)]
    return [(r + VECTORS[DIRECTIONS[i]][0], c + VECTORS[DIRECTIONS[i]][1]) for i in order]
