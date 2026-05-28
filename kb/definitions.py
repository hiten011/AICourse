from dataclasses import dataclass, field
from definitions import DIRECTIONS, VECTORS

_DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


@dataclass
class Bounds:
    left:   int = -1
    right:  int =  1
    top:    int =  1
    bottom: int = -1
    left_confirmed:   bool = False
    right_confirmed:  bool = False
    top_confirmed:    bool = False
    bottom_confirmed: bool = False

    def expand(self, pos: tuple):
        r, c = pos
        if not self.top_confirmed:    self.top    = max(self.top, r)
        if not self.bottom_confirmed: self.bottom = min(self.bottom, r)
        if not self.right_confirmed:  self.right  = max(self.right, c)
        if not self.left_confirmed:   self.left   = min(self.left, c)

    def confirm_wall(self, prev_pos: tuple, facing_idx: int):
        """Confirm cave boundary. prev_pos = last valid cell before bump."""
        r, c = prev_pos
        dr, dc = VECTORS[DIRECTIONS[facing_idx]]
        if   dr ==  1: self.top    = r; self.top_confirmed    = True
        elif dr == -1: self.bottom = r; self.bottom_confirmed = True
        elif dc ==  1: self.right  = c; self.right_confirmed  = True
        elif dc == -1: self.left   = c; self.left_confirmed   = True

    def is_valid(self, pos: tuple) -> bool:
        r, c = pos
        if self.top_confirmed    and r > self.top:    return False
        if self.bottom_confirmed and r < self.bottom: return False
        if self.right_confirmed  and c > self.right:  return False
        if self.left_confirmed   and c < self.left:   return False
        return True

    @property
    def rows(self) -> int:
        return self.top - self.bottom + 1

    @property
    def cols(self) -> int:
        return self.right - self.left + 1

    def to_grid(self, pos: tuple) -> tuple:
        return (pos[0] - self.bottom, pos[1] - self.left)


def neighbors(pos: tuple, bounds: Bounds = None) -> list[tuple]:
    r, c = pos
    candidates = [(r + dr, c + dc) for dr, dc in _DIRS]
    if bounds is None:
        return candidates
    return [p for p in candidates if bounds.is_valid(p)]
