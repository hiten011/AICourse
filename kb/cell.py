from dataclasses import dataclass, field
from enum import Enum, auto


class CellStatus(Enum):
    UNKNOWN = auto()
    SAFE    = auto()
    DANGER  = auto()
    WALL    = auto()


@dataclass
class Cell:
    status:       CellStatus = CellStatus.UNKNOWN
    visited:      bool       = False
    has_stench:   bool       = False
    has_breeze:   bool       = False
    pit_score:    int        = 0 
    wumpus_score: int        = 0   # number of corners with breezes
