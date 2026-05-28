from collections import defaultdict
from .cell import Cell, CellStatus
from .definitions import neighbors
from .navigator import action_toward, navigate_to


class KnowledgeBase:
    def __init__(self):
        self._map: dict[tuple, Cell] = defaultdict(Cell)
        self.wumpus_dead = False
        self.gold_grabbed = False

    def __getitem__(self, pos: tuple) -> Cell:
        return self._map[pos]

    def __contains__(self, pos: tuple) -> bool:
        return pos in self._map

    def mark_visited(self, pos: tuple) -> bool:
        already = self._map[pos].visited > 0
        self._map[pos].visited += 1
        return not already

    def mark_wall(self, pos: tuple):
        self._map[pos].is_bump = True

    def mark_safe(self, pos: tuple):
        cell = self._map[pos]
        if cell.status == CellStatus.UNKNOWN:
            cell.status = CellStatus.SAFE      

    def mark_empty(self, pos: tuple):
        for neighbor in neighbors(pos):
            self.mark_safe(neighbor)

    def mark_breeze(self, pos: tuple):
        self._map[pos].has_breeze = True
        for n in neighbors(pos):
            if self._map[n].status == CellStatus.UNKNOWN:
                self._map[n].pit_score += 1

    def mark_stench(self, pos: tuple):
        self._map[pos].has_stench = True     

    def mark_glimmer(self, pos: tuple):
        self._map[pos].has_glimmer = True

    def mark_danger_pit(self, pos: tuple):
        self._map[pos].pit_score = 4           # evaluate_status auto-sets DANGER_PIT

    def mark_danger_wumpus(self, pos: tuple):
        self._map[pos].wumpus_score = 4        # evaluate_status auto-sets DANGER_WUMPUS

    def next_action(self, pos: tuple, facing_idx: int, map_size: tuple) -> str:
        if self.gold_grabbed and pos == (0, 0):
            return 'EXIT'

        if self._map[pos].has_glimmer and not self.gold_grabbed:
            self.gold_grabbed = True
            return 'GRAB'

        if self.gold_grabbed:
            action = navigate_to(self._map, pos, (0, 0), facing_idx, map_size)
            return action if action is not None else 'NO_ACTION'

        r, c = pos
        neighbours = [
            (r + 1, c),     # N
            (r,     c + 1), # E
            (r - 1, c),     # S
            (r,     c - 1), # W
        ]

        neighbours.sort(key=lambda p: self[p].safe_probability())

        best = neighbours[0]
        if self[best].safe_probability() >= 999:
            return 'NO_ACTION'

        return action_toward(pos, best, facing_idx)

    def reset(self):
        self._map = defaultdict(Cell)
        self.wumpus_dead = False
        self.gold_grabbed = False
