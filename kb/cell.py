from enum import Enum, auto


class CellStatus(Enum):
    UNKNOWN       = auto()
    SAFE          = auto()
    DANGER_PIT    = auto()
    DANGER_WUMPUS = auto()
    WALL          = auto()


class Cell:
    def __init__(self):
        self.status       = CellStatus.UNKNOWN
        self.visited      = False
        self.has_stench   = False
        self.has_breeze   = False
        self.has_glimmer  = False
        self.is_bump      = False
        self.pit_score    = 0
        self.wumpus_score = 0  # evaluate_status fires from here onward

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != 'status' and hasattr(self, 'wumpus_score'):
            self.evaluate_status()

    def safe_probability(self) -> int:
        if self.status == CellStatus.SAFE and not self.visited:
            return 3   # safe, unexplored — highest priority

        if self.status == CellStatus.SAFE and self.visited:
            return 2   # safe but already seen — revisit only if needed

        if self.status == CellStatus.UNKNOWN:
            return 1   # uncertain — worth considering if nothing better
            
        return 0       # DANGER_PIT, DANGER_WUMPUS, WALL — never enter

    def evaluate_status(self):
        if self.visited or self.has_breeze or self.has_stench:
            self.status = CellStatus.SAFE

        elif self.is_bump:
            self.status = CellStatus.WALL
            
        elif self.status == CellStatus.UNKNOWN:
            if self.wumpus_score == 4:
                self.status = CellStatus.DANGER_WUMPUS
            elif self.pit_score == 4:
                self.status = CellStatus.DANGER_PIT
