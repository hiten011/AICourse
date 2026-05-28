import numpy as np
from pathfinder import bfs
from .cell import CellStatus
from definitions import DIRECTIONS, VECTORS


def action_toward(current_pos: tuple, target_pos: tuple, facing_idx: int) -> str:
    """Return single next action (rotate or FORWARD) to move toward adjacent target."""
    dr = target_pos[0] - current_pos[0]
    dc = target_pos[1] - current_pos[1]
    target_facing = next(i for i, d in enumerate(DIRECTIONS) if VECTORS[d] == (dr, dc))
    if facing_idx == target_facing:
        return 'FORWARD'
    diff = (target_facing - facing_idx) % 4
    return 'RIGHT' if diff == 1 else 'LEFT'


def best_neighbor(kb_map: dict, pos: tuple) -> tuple | None:
    """Return safest adjacent cell to explore, or None if all are blocked."""
    r, c = pos
    neighbours = [
        (r + 1, c),
        (r,     c + 1),
        (r - 1, c),
        (r,     c - 1),
    ]
    neighbours.sort(key=lambda p: kb_map[p].safe_probability())
    best = neighbours[0]
    return None if kb_map[best].safe_probability() >= 999 else best


def navigate_to(kb_map: dict, pos: tuple, target: tuple, facing_idx: int, map_size: tuple) -> str | None:
    """Return next action toward target via BFS; only SAFE cells are traversable."""
    rows, cols = map_size
    grid = np.full((rows, cols), "X", dtype=object)

    for cell_pos, cell in kb_map.items():
        r, c = cell_pos
        if 0 <= r < rows and 0 <= c < cols and cell.status == CellStatus.SAFE:
            grid[r][c] = 1

    path = bfs(pos, target, map_size, grid)
    if not path:
        return None

    return action_toward(pos, path[0], facing_idx)
