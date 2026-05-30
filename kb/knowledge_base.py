from .cell import Cell, CellStatus
from .definitions import GRID_SIZE, SPAWN, neighbors
from .explore_queue import ExploreQueue
from .navigator import navigate_to
from definitions import DIRECTIONS, VECTORS


class KnowledgeBase:
    def __init__(self):
        self._grid = None
        self._map: dict[tuple, Cell] = {}
        self._explore = ExploreQueue()
        self.wumpus_dead = False
        self.gold_grabbed = False

    def _cell(self, pos: tuple) -> Cell:
        cell = self._map.get(pos)
        if cell is None:
            cell = Cell(self._grid, pos, queue=self._explore)
            self._map[pos] = cell
        return cell

    def __getitem__(self, pos: tuple) -> Cell:
        return self._cell(pos)

    def __contains__(self, pos: tuple) -> bool:
        return pos in self._map

    def mark_visited(self, pos: tuple) -> bool:
        if self[pos].visited > 0:
            self[pos].visited += 1
            return False
        
        self[pos].visited += 1
        return True

    def mark_wall(self, prev_pos: tuple, facing_idx: int):
        dr, dc = VECTORS[DIRECTIONS[facing_idx]]
        r, c = prev_pos
        if dr != 0:
            line = [(r + dr, w) for w in range(GRID_SIZE)]
        else:
            line = [(w, c + dc) for w in range(GRID_SIZE)]
        for cell_pos in line:
            self[cell_pos].is_bump = True

    def mark_safe(self, pos: tuple):
        cell = self[pos]
        if cell.status == CellStatus.UNKNOWN:
            cell.is_safe = True 

    def mark_empty(self, pos: tuple):
        for n in neighbors(pos):
            self.mark_safe(n)

    def mark_breeze(self, pos: tuple):
        self[pos].has_breeze = True
        for n in neighbors(pos):
            if self[n].status == CellStatus.UNKNOWN:
                self[n].pit_score += 1

    def mark_stench(self, pos: tuple):
        self[pos].has_stench = True
        for n in neighbors(pos):
            if self[n].status == CellStatus.UNKNOWN:
                self[n].wumpus_score += 1

    def mark_glimmer(self, pos: tuple):
        self[pos].has_glimmer = True

    def next_action(self, pos: tuple, facing_idx: int) -> str:
        if self.gold_grabbed and pos == SPAWN:
            return 'EXIT'

        if self[pos].has_glimmer and not self.gold_grabbed:
            self.gold_grabbed = True
            return 'GRAB'

        if self.gold_grabbed:
            return navigate_to(self._grid, pos, SPAWN, facing_idx)

        target = self._explore.peek()
        if target is None:
            return navigate_to(self._grid, pos, SPAWN, facing_idx)
        return navigate_to(self._grid, pos, target, facing_idx)

    def reset(self, grid):
        self._grid = grid
        self._map = {}
        self._explore = ExploreQueue()
        self.wumpus_dead = False
        self.gold_grabbed = False
