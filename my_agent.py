"""
MyAgent — logical Wumpus World agent.

Coordinate system: internal (row, col), spawn = (0,0), facing East (idx=1).
DIRECTIONS = ["N","E","S","W"], VECTORS: N=(1,0), E=(0,1), S=(-1,0), W=(0,-1).
"""

import argparse
from collections import deque

import numpy as np

from agent import Agent
from console import PygameApp
from definitions import DIRECTIONS, VECTORS
from pathfinder import bfs
from utils import load_config

_DIR = ["N", "E", "S", "W"]


class MyAgent(Agent):

    # ------------------------------------------------------------------ setup

    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()

        self.pos = (0, 0)
        self.facing_idx = 1          # East
        self.prev_pos = (0, 0)

        # Grid bounds (tightened on each bump; internal coords)
        self.min_r = -50
        self.max_r = 50
        self.min_c = -50
        self.max_c = 50

        # Knowledge sets
        self.visited   = set()       # stepped-on cells (alive there ⇒ safe)
        self.no_pit    = set()       # confirmed pit-free
        self.no_wumpus = set()       # confirmed wumpus-free
        self.walls     = set()       # out-of-bounds cells
        self.breeze_at = set()       # cells where Breeze == True
        self.stench_at = set()       # cells where Stench == True

        # Flags / tracking
        self.wumpus_dead    = False
        self.gold_grabbed   = False
        self.has_arrow      = True
        self.glimmer_pending = False
        self.shoot_target   = None   # cell targeted by last SHOOT

        self.action_queue = deque()

        # Spawn is safe by definition
        self.visited.add((0, 0))
        self.no_pit.add((0, 0))
        self.no_wumpus.add((0, 0))

    # --------------------------------------------------------------- helpers

    def _neighbors(self, pos):
        """4-connected neighbors within known bounds, excluding walls."""
        r, c = pos
        result = []
        for d in _DIR:
            dr, dc = VECTORS[d]
            n = (r + dr, c + dc)
            nr, nc = n
            if (n not in self.walls
                    and self.min_r <= nr <= self.max_r
                    and self.min_c <= nc <= self.max_c):
                result.append(n)
        return result

    def _safe_cells(self):
        """Cells confirmed safe: pit-free AND (wumpus-free or wumpus dead)."""
        if self.wumpus_dead:
            return self.no_pit
        return self.no_pit & self.no_wumpus

    # ---- Inference ----------------------------------------------------------

    def _infer(self):
        """Propagate safety information until fixed point."""
        changed = True
        while changed:
            changed = False

            # No breeze at visited cell ⇒ all in-bounds neighbours are pit-free
            for pos in self.visited:
                if pos not in self.breeze_at:
                    for n in self._neighbors(pos):
                        if n not in self.no_pit:
                            self.no_pit.add(n)
                            changed = True

            # No stench at visited cell ⇒ neighbours are wumpus-free (if wumpus alive)
            if not self.wumpus_dead:
                for pos in self.visited:
                    if pos not in self.stench_at:
                        for n in self._neighbors(pos):
                            if n not in self.no_wumpus:
                                self.no_wumpus.add(n)
                                changed = True

    def _possible_pit_nbrs(self, breeze_cell):
        return [n for n in self._neighbors(breeze_cell)
                if n not in self.no_pit and n not in self.walls and n not in self.visited]

    def _possible_wumpus_nbrs(self, stench_cell):
        if self.wumpus_dead:
            return []
        return [n for n in self._neighbors(stench_cell)
                if n not in self.no_wumpus and n not in self.walls and n not in self.visited]

    def _confirmed_pits(self):
        """Cells with confirmed pit (sole possible neighbour of a breeze cell)."""
        pits = set()
        for bc in self.breeze_at:
            possible = self._possible_pit_nbrs(bc)
            if len(possible) == 1:
                pits.add(possible[0])
        return pits

    def _confirmed_wumpus(self):
        """Cell(s) confirmed to contain the wumpus (intersection of all stench sources)."""
        if self.wumpus_dead or not self.stench_at:
            return set()
        candidates = None
        for sc in self.stench_at:
            possible = set(self._possible_wumpus_nbrs(sc))
            candidates = possible if candidates is None else candidates & possible
        return candidates if candidates else set()

    # ---- Pathfinding --------------------------------------------------------

    def _build_grid(self, extra=None):
        """Numpy grid over traversable cells (safe ∪ visited, minus walls)."""
        traversable = (self.visited | self._safe_cells()) - self.walls
        if extra:
            traversable |= extra
        if not traversable:
            return None, None, 0, 0

        all_pts = traversable | {self.pos}
        rmin = min(p[0] for p in all_pts)
        cmin = min(p[1] for p in all_pts)
        rmax = max(p[0] for p in all_pts)
        cmax = max(p[1] for p in all_pts)

        rows, cols = rmax - rmin + 1, cmax - cmin + 1
        grid = np.full((rows, cols), "X", dtype=object)
        for cell in traversable:
            gr, gc = cell[0] - rmin, cell[1] - cmin
            if 0 <= gr < rows and 0 <= gc < cols:
                grid[gr][gc] = 1
        return grid, (rows, cols), rmin, cmin

    def _navigate_to(self, target, extra=None):
        """Action list from current pos to target through safe/visited cells."""
        if self.pos == target:
            return []
        grid, size, rmin, cmin = self._build_grid(extra)
        if grid is None:
            return None
        tr, tc = target[0] - rmin, target[1] - cmin
        pr, pc = self.pos[0] - rmin, self.pos[1] - cmin
        if not (0 <= tr < size[0] and 0 <= tc < size[1]):
            return None
        if not (0 <= pr < size[0] and 0 <= pc < size[1]):
            return None
        grid[tr][tc] = 1  # open target cell
        path = bfs((pr, pc), (tr, tc), size, grid)
        if path is None:
            return None
        world = [(p[0] + rmin, p[1] + cmin) for p in path]
        return self._path_to_actions(world)

    def _path_to_actions(self, path):
        actions = []
        pos, fi = self.pos, self.facing_idx
        for nxt in path:
            dr, dc = nxt[0] - pos[0], nxt[1] - pos[1]
            tfi = next(i for i, d in enumerate(_DIR) if VECTORS[d] == (dr, dc))
            while fi != tfi:
                diff = (tfi - fi) % 4
                if diff == 3:           # 1 LEFT is cheaper than 3 RIGHTs
                    actions.append("LEFT");  fi = (fi - 1) % 4
                else:
                    actions.append("RIGHT"); fi = (fi + 1) % 4
            actions.append("FORWARD")
            pos = nxt
        return actions

    def _rotations_to(self, target_pos):
        """Minimum rotations from current facing to face target_pos."""
        dr, dc = target_pos[0] - self.pos[0], target_pos[1] - self.pos[1]
        try:
            tfi = next(i for i, d in enumerate(_DIR) if VECTORS[d] == (dr, dc))
        except StopIteration:
            return 99
        diff = (tfi - self.facing_idx) % 4
        return min(diff, 4 - diff)

    # ---- Decision helpers ---------------------------------------------------

    def _nearest_safe_frontier(self):
        """Closest unvisited safe cell, or None."""
        safe = self._safe_cells()
        frontier = safe - self.visited - self.walls
        if not frontier:
            return None

        traversable = (self.visited | safe) - self.walls
        all_pts = traversable | {self.pos}
        rmin = min(p[0] for p in all_pts)
        cmin = min(p[1] for p in all_pts)
        rmax = max(p[0] for p in all_pts)
        cmax = max(p[1] for p in all_pts)
        rows, cols = rmax - rmin + 1, cmax - cmin + 1
        grid = np.full((rows, cols), "X", dtype=object)
        for cell in traversable | frontier:
            gr, gc = cell[0] - rmin, cell[1] - cmin
            if 0 <= gr < rows and 0 <= gc < cols:
                grid[gr][gc] = 1

        pr, pc = self.pos[0] - rmin, self.pos[1] - cmin
        if not (0 <= pr < rows and 0 <= pc < cols):
            return next(iter(frontier))

        best, best_d = None, float("inf")
        for tgt in frontier:
            tr, tc = tgt[0] - rmin, tgt[1] - cmin
            if not (0 <= tr < rows and 0 <= tc < cols):
                continue
            path = bfs((pr, pc), (tr, tc), (rows, cols), grid)
            if path and len(path) < best_d:
                best_d, best = len(path), tgt
        return best

    def _plan_confirmed_shoot(self):
        """
        If wumpus location is confirmed, return an action list that navigates
        to a safe adjacent cell, faces the wumpus, and SHOOTs. Else None.
        """
        if not self.has_arrow or self.wumpus_dead:
            return None
        confirmed = self._confirmed_wumpus()
        if not confirmed:
            return None
        wpos = next(iter(confirmed))
        return self._build_shoot_plan(wpos)

    def _build_shoot_plan(self, wpos):
        """
        Build [nav…, rotate…, SHOOT] to shoot wpos from a safe adjacent cell.
        """
        for d in _DIR:
            dr, dc = VECTORS[d]
            shoot_from = (wpos[0] + dr, wpos[1] + dc)
            if shoot_from in self.walls:
                continue
            if shoot_from not in self.visited and shoot_from not in self._safe_cells():
                continue
            # Direction from shoot_from toward wpos
            facing_toward = (_DIR.index(d) + 2) % 4   # opposite of d

            nav = self._navigate_to(shoot_from)
            if nav is None:
                continue

            # Simulate facing after nav
            fi = self.facing_idx
            for a in nav:
                if a == "LEFT":  fi = (fi - 1) % 4
                elif a == "RIGHT": fi = (fi + 1) % 4

            while fi != facing_toward:
                diff = (facing_toward - fi) % 4
                if diff == 3:
                    nav.append("LEFT");  fi = (fi - 1) % 4
                else:
                    nav.append("RIGHT"); fi = (fi + 1) % 4
            nav.append("SHOOT")
            return nav
        return None

    def _plan_speculative_shoot(self):
        """
        When stuck (no safe frontier) and wumpus unconfirmed, speculatively
        shoot in the direction requiring fewest rotations among possible wumpus
        neighbours.  Returns action list or None.
        """
        if not self.has_arrow or self.wumpus_dead:
            return None
        if self.pos not in self.stench_at:
            return None

        possible = self._possible_wumpus_nbrs(self.pos)
        if not possible:
            return None

        # Pick target requiring fewest rotations (ties broken by tuple order)
        target = min(possible, key=lambda p: (self._rotations_to(p), p))

        dr, dc = target[0] - self.pos[0], target[1] - self.pos[1]
        tfi = next((i for i, d in enumerate(_DIR) if VECTORS[d] == (dr, dc)), None)
        if tfi is None:
            return None

        nav = []
        fi = self.facing_idx
        while fi != tfi:
            diff = (tfi - fi) % 4
            if diff == 3:
                nav.append("LEFT");  fi = (fi - 1) % 4
            else:
                nav.append("RIGHT"); fi = (fi + 1) % 4
        nav.append("SHOOT")
        self.shoot_target = target
        return nav

    def _risky_target(self):
        """
        Best cell to explore when no safe frontier exists.

        Score = pit_adjacency*2 + wumpus_adjacency.
        Tiebreak: fewest rotations (prefer direction already faced), then tuple order.
        """
        confirmed_danger = self._confirmed_pits() | self._confirmed_wumpus()

        candidates = []
        for vc in self.visited:
            for n in self._neighbors(vc):
                if (n not in self.visited
                        and n not in self.walls
                        and n not in self._safe_cells()
                        and n not in confirmed_danger):
                    candidates.append(n)
        if not candidates:
            return None

        def score(cell):
            pit_adj    = sum(1 for bc in self.breeze_at
                             if cell in self._neighbors(bc))
            wumpus_adj = sum(1 for sc in self.stench_at
                             if cell in self._neighbors(sc))
            return (pit_adj * 2 + wumpus_adj, self._rotations_to(cell), cell)

        return min(candidates, key=score)

    # ---------------------------------------------------------------- update

    def update(self, senses):
        super().update(senses)

        if senses["Bump"]:
            # FORWARD hit a wall — revert position
            self.pos = self.prev_pos
            dr, dc = VECTORS[_DIR[self.facing_idx]]
            wall = (self.prev_pos[0] + dr, self.prev_pos[1] + dc)
            self.walls.add(wall)
            self.no_pit.discard(wall)
            self.no_wumpus.discard(wall)
            # Tighten grid bounds
            r, c = self.prev_pos
            if dr ==  1 and r < self.max_r: self.max_r = r
            if dr == -1 and r > self.min_r: self.min_r = r
            if dc ==  1 and c < self.max_c: self.max_c = c
            if dc == -1 and c > self.min_c: self.min_c = c
            # Invalidate queued plan (path may use the now-known wall)
            self.action_queue.clear()
            return

        # Successfully entered self.pos
        self.visited.add(self.pos)
        self.no_pit.add(self.pos)
        self.no_wumpus.add(self.pos)

        if senses["Scream"]:
            self.wumpus_dead = True
            if self.shoot_target is not None:
                # Wumpus killed there → no pit (no overlap rule)
                self.no_pit.add(self.shoot_target)
                self.no_wumpus.add(self.shoot_target)
            self.shoot_target = None

        if senses["Glimmer"]:
            self.glimmer_pending = True

        if senses["Breeze"]:
            self.breeze_at.add(self.pos)

        if senses["Stench"]:
            self.stench_at.add(self.pos)

        # No-scream after a SHOOT → that cell is wumpus-free
        if (self.last_action == "SHOOT"
                and not senses.get("Scream", False)
                and self.shoot_target is not None):
            self.no_wumpus.add(self.shoot_target)
            self.shoot_target = None

        self._infer()

    # ------------------------------------------------------------------- act

    def act(self):
        self.prev_pos = self.pos

        def execute(action):
            if action == "LEFT":
                self.facing_idx = (self.facing_idx - 1) % 4
            elif action == "RIGHT":
                self.facing_idx = (self.facing_idx + 1) % 4
            elif action == "FORWARD":
                dr, dc = VECTORS[_DIR[self.facing_idx]]
                self.pos = (self.pos[0] + dr, self.pos[1] + dc)
            elif action == "SHOOT":
                self.has_arrow = False
            elif action == "GRAB":
                self.gold_grabbed  = True
                self.glimmer_pending = False
            return self.remember_action(action)

        # ---- Follow existing plan ----------------------------------------
        if self.action_queue:
            return execute(self.action_queue.popleft())

        # ---- Grab gold ---------------------------------------------------
        if self.glimmer_pending:
            return execute("GRAB")

        # ---- Exit with gold ----------------------------------------------
        if self.gold_grabbed:
            if self.pos == (0, 0):
                return execute("EXIT")
            actions = self._navigate_to((0, 0))
            if actions:
                self.action_queue = deque(actions[1:])
                return execute(actions[0])
            return execute("EXIT")

        # ---- Explore safe frontier ---------------------------------------
        target = self._nearest_safe_frontier()
        if target is not None:
            actions = self._navigate_to(target)
            if actions:
                self.action_queue = deque(actions[1:])
                return execute(actions[0])

        # ---- Shoot confirmed wumpus ------------------------------------
        plan = self._plan_confirmed_shoot()
        if plan:
            # Track the shoot target (last cell before SHOOT in the plan)
            fi = self.facing_idx
            tmp_pos = self.pos
            for a in plan[:-1]:   # everything except SHOOT
                if a == "LEFT":   fi = (fi - 1) % 4
                elif a == "RIGHT": fi = (fi + 1) % 4
                elif a == "FORWARD":
                    dr, dc = VECTORS[_DIR[fi]]
                    tmp_pos = (tmp_pos[0] + dr, tmp_pos[1] + dc)
            dr, dc = VECTORS[_DIR[fi]]
            self.shoot_target = (tmp_pos[0] + dr, tmp_pos[1] + dc)
            self.action_queue = deque(plan[1:])
            return execute(plan[0])

        # ---- Speculative shoot when stuck with stench -------------------
        spec = self._plan_speculative_shoot()
        if spec:
            # shoot_target already set inside _plan_speculative_shoot
            self.action_queue = deque(spec[1:])
            return execute(spec[0])

        # ---- Risky exploration ------------------------------------------
        risky = self._risky_target()
        if risky is not None:
            actions = self._navigate_to(risky, extra={risky})
            if actions:
                self.action_queue = deque(actions[1:])
                return execute(actions[0])

        # ---- Give up: return to spawn and exit --------------------------
        if self.pos == (0, 0):
            return execute("EXIT")
        actions = self._navigate_to((0, 0))
        if actions:
            self.action_queue = deque(actions[1:])
            return execute(actions[0])

        return execute("EXIT")


# ----------------------------------------------------------------- launcher

def _parse_args():
    parser = argparse.ArgumentParser(description="Run Wumpus World with MyAgent.")
    parser.add_argument("--config",       default="game_config.yaml")
    parser.add_argument("--cave",         default="empty")
    parser.add_argument("--show-window",  default="true")
    parser.add_argument("--seed",         default=None)
    return parser.parse_args()


def main():
    args = _parse_args()
    agent  = MyAgent()
    config = load_config(args.config, cave_name=args.cave,
                         show_window=args.show_window, seed=args.seed)
    PygameApp(agent=agent, config=config).run()


if __name__ == "__main__":
    main()
