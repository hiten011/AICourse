from pathfinder import bfs
from .definitions import GRID_SIZE
from definitions import DIRECTIONS, VECTORS

_cached_target: tuple | None = None
_cached_path: list[tuple] = []


def reset_cache():
    global _cached_target, _cached_path
    _cached_target = None
    _cached_path = []


def action_toward(current_pos: tuple, target_pos: tuple, facing_idx: int) -> str:
    dr = target_pos[0] - current_pos[0]
    dc = target_pos[1] - current_pos[1]
    target_facing = next(i for i, d in enumerate(DIRECTIONS) if VECTORS[d] == (dr, dc))
    if facing_idx == target_facing:
        return 'FORWARD'
    diff = (target_facing - facing_idx) % 4
    return 'RIGHT' if diff == 1 else 'LEFT'

def navigate_to(grid, pos: tuple, target: tuple, facing_idx: int) -> str | None:
    global _cached_target, _cached_path

    if target == _cached_target and _cached_path:
        action = action_toward(pos, _cached_path[-1], facing_idx)
        if action == 'FORWARD':
            _cached_path.pop()
        return action

    saved = grid[target[0]][target[1]]
    grid[target[0]][target[1]] = "."
    path = bfs(pos, target, (GRID_SIZE, GRID_SIZE), grid)
    grid[target[0]][target[1]] = saved

    if not path:
        _cached_target = None
        _cached_path = []
        return 'NO_ACTION'

    _cached_target = target
    _cached_path = list(reversed(path))

    action = action_toward(pos, _cached_path[-1], facing_idx)
    if action == 'FORWARD':
        _cached_path.pop()
    return action
