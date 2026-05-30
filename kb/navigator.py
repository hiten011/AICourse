from pathfinder import bfs
from .definitions import GRID_SIZE
from definitions import DIRECTIONS, VECTORS


def action_toward(current_pos: tuple, target_pos: tuple, facing_idx: int) -> str:
    dr = target_pos[0] - current_pos[0]
    dc = target_pos[1] - current_pos[1]
    target_facing = next(i for i, d in enumerate(DIRECTIONS) if VECTORS[d] == (dr, dc))
    if facing_idx == target_facing:
        return 'FORWARD'
    diff = (target_facing - facing_idx) % 4
    return 'RIGHT' if diff == 1 else 'LEFT'

def navigate_to(grid, pos: tuple, target: tuple, facing_idx: int) -> str | None:
    saved = grid[target[0]][target[1]]
    grid[target[0]][target[1]] = "."

    path = bfs(pos, target, (GRID_SIZE, GRID_SIZE), grid)
    grid[target[0]][target[1]] = saved

    if not path:
        return 'NO_ACTION'

    return action_toward(pos, path[0], facing_idx)
