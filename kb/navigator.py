import numpy as np
from pathfinder import bfs
from .cell import CellStatus
from .definitions import Bounds, neighbors
from definitions import DIRECTIONS, VECTORS


def action_toward(current_pos: tuple, target_pos: tuple, facing_idx: int) -> str:
    dr = target_pos[0] - current_pos[0]
    dc = target_pos[1] - current_pos[1]
    target_facing = next(i for i, d in enumerate(DIRECTIONS) if VECTORS[d] == (dr, dc))
    if facing_idx == target_facing:
        return 'FORWARD'
    diff = (target_facing - facing_idx) % 4
    return 'RIGHT' if diff == 1 else 'LEFT'


def best_neighbor(kb_map: dict, pos: tuple, bounds: Bounds = None) -> tuple | None:
    """Return safest adjacent cell to explore within bounds, or None if all blocked."""
    candidates = neighbors(pos, bounds)
    candidates = [p for p in candidates if kb_map[p].safe_probability() < 999]
    if not candidates:
        return None
    return min(candidates, key=lambda p: kb_map[p].safe_probability())


def navigate_to(kb_map: dict, pos: tuple, target: tuple, facing_idx: int, bounds: Bounds) -> str | None:
    """Return next action toward target via BFS; only SAFE cells are traversable."""
    rows, cols = bounds.rows, bounds.cols
    map_size = (rows, cols)
    grid = np.full((rows, cols), "X", dtype=object)

    for cell_pos, cell in kb_map.items():
        gr, gc = bounds.to_grid(cell_pos)
        if 0 <= gr < rows and 0 <= gc < cols and cell.status == CellStatus.SAFE:
            grid[gr][gc] = 1

    grid_pos = bounds.to_grid(pos)
    grid_target = bounds.to_grid(target)

    path = bfs(grid_pos, grid_target, map_size, grid)
    if not path:
        return None

    world_next = (path[0][0] + bounds.bottom, path[0][1] + bounds.left)
    return action_toward(pos, world_next, facing_idx)
