from dataclasses import dataclass
from enum import Enum, auto


class CellStatus(Enum):
    UNKNOWN       = auto()
    SAFE          = auto()
    DANGER_PIT    = auto()
    DANGER_WUMPUS = auto()
    WALL          = auto()


@dataclass
class Cell:
    status:       CellStatus = CellStatus.UNKNOWN
    visited:      bool       = False
    has_stench:   bool       = False
    has_breeze:   bool       = False
    is_bump:      bool       = False
    pit_score:    int        = 0
    wumpus_score: int        = 0

    def __post_init__(self):
        object.__setattr__(self, '_ready', True)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != 'status' and getattr(self, '_ready', False):
            self.evaluate_status()

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
