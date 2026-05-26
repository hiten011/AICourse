import argparse
from agent import Agent
from console import PygameApp
from utils import load_config
from definitions import ACTIONS, SENSE_NAMES, DIRECTIONS, VECTORS

# ─── SENSES (received in update()) ───────────────────────────────────────────
# Stench   → Wumpus is in an adjacent cell (N/E/S/W). Does NOT mean current cell.
# Breeze   → Pit is in an adjacent cell (N/E/S/W). Does NOT mean current cell.
# Glimmer  → Gold is in the CURRENT cell (not adjacent).
# Bump     → Last FORWARD hit a wall — position did NOT change, must revert.
# Scream   → Wumpus just died (arrow hit). Heard globally; set wumpus_dead=True.
#
# Negative percepts matter equally:
#   No Stench → no Wumpus in any adjacent cell → all neighbors Wumpus-safe.
#   No Breeze → no Pit in any adjacent cell    → all neighbors pit-safe.

# ─── ACTIONS (returned from act()) ───────────────────────────────────────────
# FORWARD    → Move one step in current facing direction. Cost: -1.
#              If wall ahead, position unchanged and next update() has Bump=True.
# LEFT       → Rotate 90° counter-clockwise (no movement). Cost: -1.
# RIGHT      → Rotate 90° clockwise (no movement). Cost: -1.
# GRAB       → Pick up gold if present in current cell. Cost: -1.
# SHOOT      → Fire arrow straight ahead (one-use only). Cost: -10 total.
#              If Wumpus is in that line, it dies and Scream percept fires.
# EXIT       → Leave the cave. Cost: -1.
#              Only scores gold/win if standing at spawn cell (0,0).
# NO_ACTION  → Do nothing. Cost: 0, but still burns 1000-step budget.


class MyAgent(Agent):

    def __init__(self):
        super(MyAgent, self).__init__()


    def reset(self):
        super(MyAgent, self).reset()


    def act(self):
        return ACTIONS[0]

    def update(self, senses):
        super(MyAgent, self).update(senses)

        # Print all senses received this tick
        for s in SENSE_NAMES:
            print(s + " " + ('True' if senses[s] else 'False') + "\n")


def parse_args():
    """Read command-line options for launching the logic-agent emulator."""
    parser = argparse.ArgumentParser(description="Run Wumpus World with the logic agent.")
    parser.add_argument("--config", default="game_config.yaml", help="YAML config file for game parameters.")
    parser.add_argument("--cave", default="empty", help="Named cave profile from the YAML config.")
    parser.add_argument("--show-window", default="true", help="Override emulator.show_window from the config.")
    parser.add_argument("--seed", help="Override cave.seed from the config with an integer.")
    return parser.parse_args()


def main():
    """Create a MyAgent and launch the pygame emulator in auto-play mode."""
    args = parse_args()

    agent = MyAgent()
    config = load_config(args.config, cave_name=args.cave, show_window=args.show_window, seed=args.seed)
    PygameApp(agent=agent, config=config).run()

if __name__ == "__main__":
    main()
