from collections import defaultdict
from .cell import Cell, CellStatus
from .definitions import neighbors


class KnowledgeBase:
    def __init__(self):
        self._map: dict[tuple, Cell] = defaultdict(Cell)
        self.wumpus_dead = False
        self.gold_grabbed = False

    def __getitem__(self, pos: tuple) -> Cell:
        return self._map[pos]

    def __contains__(self, pos: tuple) -> bool:
        return pos in self._map

    def mark_visited(self, pos: tuple):
        cell = self._map[pos]
        cell.visited = True
        cell.status = CellStatus.SAFE

    def mark_wall(self, pos: tuple):
        self._map[pos].status = CellStatus.WALL

    def mark_safe(self, pos: tuple):
        cell = self._map[pos]
        if cell.status == CellStatus.UNKNOWN:
            cell.status = CellStatus.SAFE

    def mark_empty(self, pos: tuple):
        for neighbor in neighbors(pos):
            self.mark_safe(neighbor)

    def mark_danger_pit(self, pos: tuple):
        self._map[pos].status = CellStatus.DANGER_PIT

    def mark_danger_wumpus(self, pos: tuple):
        self._map[pos].status = CellStatus.DANGER_WUMPUS


    def reset(self):
        self._map = defaultdict(Cell)
        self.wumpus_dead = False
        self.gold_grabbed = False
