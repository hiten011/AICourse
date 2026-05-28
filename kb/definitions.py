from definitions import DIRECTIONS, VECTORS

_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def neighbors(pos: tuple) -> list[tuple]:
    r, c = pos
    return [(r + dr, c + dc) for dr, dc in _DIRS]


def action_toward(current_pos: tuple, target_pos: tuple, facing_idx: int) -> str:
    """Return single next action (rotate or FORWARD) to move toward adjacent target."""
    dr = target_pos[0] - current_pos[0]
    dc = target_pos[1] - current_pos[1]

    target_facing = next(i for i, d in enumerate(DIRECTIONS) if VECTORS[d] == (dr, dc))

    if facing_idx == target_facing:
        return 'FORWARD'

    diff = (target_facing - facing_idx) % 4
    return 'RIGHT' if diff == 1 else 'LEFT'
