from enum import Enum, auto


class CellStatus(Enum):
    UNKNOWN       = auto()
    SAFE          = auto()
    DANGER_PIT    = auto()
    DANGER_WUMPUS = auto()
    WALL          = auto()


class Cell:
    def __init__(self, grid, pos, queue=None):
        self._queue       = queue
        self.grid         = grid
        self.gpos         = pos
        self.status       = CellStatus.UNKNOWN
        self.visited      = 0
        self.has_stench   = False
        self.has_breeze   = False
        self.has_glimmer  = False
        self.is_bump      = False
        self.is_safe      = False
        self.pit_score    = 0
        self.wumpus_score = 0 

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != 'status' and hasattr(self, 'wumpus_score'):
            self.evaluate_status()

    def evaluate_status(self):
        if self.is_bump:
            self.status = CellStatus.WALL
            self._queue.discard(self.gpos)

        elif self.visited > 0:
            self.status = CellStatus.SAFE
            self.grid[self.gpos[0]][self.gpos[1]] = "."

            self._queue.discard(self.gpos)

        elif self.is_safe:
            self.status = CellStatus.SAFE
            self.grid[self.gpos[0]][self.gpos[1]] = "."

            self._queue.discard(self.gpos)
            self._queue.add(self.gpos, 0)

        elif self.status == CellStatus.UNKNOWN:
            if self.wumpus_score >= 4:
                self.status = CellStatus.DANGER_WUMPUS
                self._queue.discard(self.gpos) 
            elif self.pit_score >= 4:
                self.status = CellStatus.DANGER_PIT
                self._queue.discard(self.gpos) 
            else:
                self._queue.discard(self.gpos)
                self._queue.add(self.gpos, 1 + self.pit_score + self.wumpus_score) 
