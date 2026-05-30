# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Assignment Context

ARTI 2003 Assignment 3 (Adelaide Uni, 2026). Implement `MyAgent` in `my_agent.py` — a logical agent that navigates Wumpus World caves, collects gold, avoids hazards, and exits with a positive score. Only `my_agent.py` and any helper `.py` files you create are submitted; all other files are provided by the course and must not be modified.

## What to Implement

`MyAgent` must:
1. Explore a cave grid (4×4 default, up to 6×6 for `large`)
2. Collect gold (+100 pts)
3. Avoid pits (−100 death) and Wumpus (−100 death)
4. EXIT at spawn cell `(0,0)` with positive score

Override `reset()`, `update()`, and `act()` in `my_agent.py`. No other files are submitted.

## Running the Agent

```bash
# Install deps
python -m pip install -r requirements.txt
```

Makefile shortcuts (preferred):

| Target | What it does |
|--------|-------------|
| `make 1`–`make 5` | Visual run of each graded cave (window) |
| `make 1s`–`make 5s` | Silent run of each graded cave (fast, no window) |
| `make replay` | Rerun last saved map (needs `save_last_map: true`) |
| `make human` | Play `default` cave yourself |
| `make benchmark` | 100-run benchmark via `assessor.py` |

```bash
# Or run directly with a fixed seed for reproducibility
python my_agent.py --cave default --seed 42

# Measure success rate over 100 runs (mirrors Gradescope)
python assessor.py
```

Human agent key bindings (useful for understanding game behavior):
- `Space` — move forward, `Left`/`Right` — rotate, `Z` — shoot, `X` — grab gold
- `Q` — exit at spawn, `N` — new cave, `R` — reveal/hide full cave

## Architecture

The emulator drives a strict game loop:
1. `agent.update(senses)` — emulator pushes percepts
2. `agent.act()` — agent returns action string
3. Emulator applies action, updates score, repeats

`update()` and `act()` alternate exactly — one sense per action, first `update()` fires before first `act()`.

Key files:
- `my_agent.py` — **your work lives here**
- `agent.py` — base `Agent` class; `update()` stores `self.last_senses`, `act()` returns `NO_ACTION`; `remember_action(action)` validates and stores the action — call it instead of returning raw strings
- `console.py` — `PygameApp` runs visual/silent game loop via `_run_visual()` / `_run_silent()`
- `cave.py` — world state, `apply_action()`, `senses()`
- `pathfinder.py` — provided `bfs(start, target, map_size, grid)` and `ucs(...)` solvers
- `definitions.py` — `ACTIONS`, `SENSE_NAMES`, `DIRECTIONS`, `VECTORS` — do not modify
- `cave_config.yaml` — cave profiles; `game_config.yaml` — scoring + emulator settings

## Senses (received in `update()`)

| Key | Meaning |
|-----|---------|
| `Stench` | Wumpus in adjacent cell (N/E/S/W) |
| `Breeze` | Pit in adjacent cell (N/E/S/W) |
| `Glimmer` | Gold in **current** cell (not adjacent) |
| `Bump` | Last FORWARD hit a wall — position did NOT change |
| `Scream` | Wumpus was just killed (heard everywhere) |

**Critical:** Negative percepts are equally informative. No Stench → no Wumpus adjacent → all neighbors safe (wumpus-wise). No Breeze → no pit adjacent → all neighbors safe (pit-wise).

## Actions (return from `act()`)

| Action | Effect | Cost |
|--------|--------|------|
| `FORWARD` | Move one step in facing direction | −1 |
| `LEFT` | Rotate 90° left (no move) | −1 |
| `RIGHT` | Rotate 90° right (no move) | −1 |
| `GRAB` | Pick up gold if present | −1 |
| `SHOOT` | Fire arrow in facing direction (one-use) | −10 total |
| `EXIT` | Exit cave (only scores if at spawn) | −1 |
| `NO_ACTION` | Do nothing | 0 (but counts toward 1000-step cap) |

## Coordinate System

- Internal: zero-based `(row, col)` tuples
- UI display: one-based `[row, col]`
- Agent starts at internal `(0,0)` = display `[1,1]`, facing East
- `VECTORS = {"N":(1,0), "E":(0,1), "S":(-1,0), "W":(0,-1)}`
- `LEFT`/`RIGHT` rotate facing; `FORWARD` moves one step in current facing direction
- `Bump` on `FORWARD` means wall ahead — position does not change

## State You MUST Track Manually

The emulator gives you NO position or facing info — track it yourself.

### Facing Direction

```python
DIRECTION_ORDER = ["N", "E", "S", "W"]
facing_idx = 1  # start facing East

# LEFT:  facing_idx = (facing_idx - 1) % 4
# RIGHT: facing_idx = (facing_idx + 1) % 4
```

### Position

```python
# On FORWARD: compute candidate position
dr, dc = VECTORS[DIRECTIONS[facing_idx]]
candidate = (pos[0] + dr, pos[1] + dc)
# If Bump=True in NEXT update() → position didn't change, revert candidate
```

Apply FORWARD optimistically, revert if next `update()` has `Bump=True`.

### Cave Size

Not given. Infer from Bump events. For `default` always 4×4; for `large` is 5–6 wide/tall.

### Knowledge Base

```python
visited = set()       # cells stepped on
safe = set()          # confirmed no hazard (visited or inferred)
stench_cells = set()  # cells where Stench was True
breeze_cells = set()  # cells where Breeze was True
danger = set()        # confirmed dangerous (do not enter)
wumpus_dead = False   # True after Scream received
gold_grabbed = False
```

## Core Algorithm

### Decision loop in `act()`:

1. If `Glimmer` and not grabbed → GRAB
2. If `gold_grabbed` and at `(0,0)` → EXIT
3. If action queue non-empty → pop and return next action
4. Compute safe frontier (unvisited neighbors of safe cells, excluding danger)
5. If safe frontier → BFS to nearest safe frontier cell, convert path to action queue
6. Else → EXIT (no safe moves left)

### Inference rules:

```python
# At cell C, no Stench:  all neighbors → safe from Wumpus
# At cell C, no Breeze:  all neighbors → safe from pits
# At cell C, Stench:     Wumpus in one of unvisited neighbors (don't enter without more info)
# At cell C, Breeze:     Pit in one of unvisited neighbors
# Scream received:       wumpus_dead = True → clear Wumpus danger from all cells
```

## Converting BFS Path to Actions

`bfs()` returns `[(row,col), ...]` — convert to LEFT/RIGHT/FORWARD sequence:

```python
def path_to_actions(path, current_pos, facing_idx):
    actions = []
    pos = current_pos
    fi = facing_idx
    for next_pos in path:
        dr = next_pos[0] - pos[0]
        dc = next_pos[1] - pos[1]
        for i, d in enumerate(DIRECTIONS):
            if VECTORS[d] == (dr, dc):
                target_fi = i
                break
        while fi != target_fi:
            diff = (target_fi - fi) % 4
            if diff == 1:
                actions.append("RIGHT"); fi = (fi + 1) % 4
            else:
                actions.append("LEFT"); fi = (fi - 1) % 4
        actions.append("FORWARD")
        pos = next_pos
    return actions
```

## `pathfinder.py` Usage

```python
from pathfinder import bfs
import numpy as np

# Build grid: 1 = traversable, "X" = blocked
grid = np.ones((rows, cols), dtype=object)
grid[blocked_row][blocked_col] = "X"

path = bfs(start=(0,0), target_position=(2,3), map_size=(rows, cols), grid=grid)
# Returns list of (row, col) steps from start+1 through target, or None

# ucs() works identically but grid cells hold numeric costs instead of 1
# Use bfs for uniform grids; ucs for weighted cost maps
```

## Scoring

```
action:    -1   (every action including SHOOT)
shoot:     -9   (additional, so SHOOT costs -10 total)
death:    -100
gold:     +100
NO_ACTION:   0  (no penalty but counts toward 1000-action silent-mode cap)
```

## Graded Caves

| Cave | Hazards | Min Success Rate | Key Challenge |
|------|---------|-----------------|---------------|
| `gold` | none | 99% | Just find and return gold |
| `breeze_and_gold` | 2 pits | 60% | Reason around fixed pits |
| `default` | 1 Wumpus, 1–3 pits | 60% | Random layout each run |
| `siege` | Wumpus + pit adjacent to spawn | 70% | Don't die immediately |
| `large` | 5×5–6×6, random corner start, 2–4 pits | 70% | Unknown cave size |

## Debugging Tips

### game_config.yaml tweaks (safe to change locally):

| Setting | Value | Effect |
|---------|-------|--------|
| `suppress_agent_output` | `false` | `print()` shows in terminal during silent runs |
| `save_last_map` | `true` | Saves cave to `maps/last.txt` after each run |
| `agent_action_delay_ms` | `500`–`1000` | Slows visual playback |

### Debug workflow:

```bash
# 1. Reproduce failing run
python my_agent.py --cave default --seed 42

# 2. Save the map of a failing run:
#    Set save_last_map: true in game_config.yaml, then run
#    Map saved to maps/last.txt

# 3. Replay exact layout:
python my_agent.py --cave last

# 4. Benchmark (first edit assessor.py line 20):
#    agent = MyAgent()   ← change from RandomAgent()
python assessor.py
```

### Internal map printer (add to MyAgent):

```python
def _debug_map(self):
    for r in range(self.rows - 1, -1, -1):
        row_str = ""
        for c in range(self.cols):
            cell = (r, c)
            if cell == self.pos:        row_str += "A"
            elif cell in self.danger:   row_str += "X"
            elif cell in self.visited:  row_str += "."
            elif cell in self.safe:     row_str += "s"
            else:                       row_str += "?"
        print(f"row {r}: {row_str}")
    print(f"facing={DIRECTIONS[self.facing_idx]} pos={self.pos}")
```

## Common Gotchas

1. **Bump revert**: `Bump=True` in `update()` means FORWARD that just ran didn't move — revert your position.
2. **N = row+1** (North goes up = higher row). S = row−1. E = col+1. W = col−1.
3. **EXIT only scores at spawn** `(0,0)`. Exiting anywhere else = no gold points.
4. **Arrow one-use only**. Set `wumpus_dead=True` on `Scream`, then reclassify stench-only cells.
5. **Glimmer = current cell only**, not adjacent.
6. **NO_ACTION has 0 penalty** but still burns the 1000-step budget.
7. **First `update()` fires before first `act()`** — process initial percepts at spawn.
8. **`reset()` called before each new cave** — reinitialize all state there, not in `__init__`.
9. **Cave size unknown** — infer from Bump or assume 4×4 for `default`.
10. **`assessor.py` uses `RandomAgent` by default** — change line 20 to `agent = MyAgent()` to benchmark your agent.
