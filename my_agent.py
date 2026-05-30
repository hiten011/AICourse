import argparse

import numpy as np

from agent import Agent
from console import PygameApp
from utils import load_config
from definitions import DIRECTIONS, VECTORS
from kb import KnowledgeBase, GRID_SIZE, SPAWN


class MyAgent(Agent):

    def __init__(self):
        self.kb = KnowledgeBase()
        self.pos = SPAWN
        self.prev_pos = SPAWN
        self.facing_idx = 1          # start facing East
        self.grid = np.full((GRID_SIZE, GRID_SIZE), "X", dtype=object)
        super().__init__()

    def reset(self):
        super().reset()
        self.pos = SPAWN
        self.prev_pos = SPAWN
        self.facing_idx = 1
        self.grid = np.full((GRID_SIZE, GRID_SIZE), "X", dtype=object)
        self.kb.reset(self.grid)

    def update(self, senses):
        super().update(senses)

        if senses['Bump']:
            self.kb.mark_wall(self.prev_pos, self.facing_idx)
            self.pos = self.prev_pos
            return

        if not self.kb.mark_visited(self.pos):
            return

        if senses['Breeze']:
            self.kb.mark_breeze(self.pos, self.facing_idx)

        if senses['Stench']:
            self.kb.mark_stench(self.pos, self.facing_idx)

        if senses['Glimmer']:
            self.kb.mark_glimmer(self.pos)

        if senses['Scream']:
            print(f"[{self.pos}] Scream")

        if not any(senses.values()):
            self.kb.mark_empty(self.pos, self.facing_idx)

    def act(self):
        self.prev_pos = self.pos

        action = self.kb.next_action(self.pos, self.facing_idx)

        if action == 'LEFT':
            self.facing_idx = (self.facing_idx - 1) % 4
        elif action == 'RIGHT':
            self.facing_idx = (self.facing_idx + 1) % 4
        elif action == 'FORWARD':
            dr, dc = VECTORS[DIRECTIONS[self.facing_idx]]
            self.pos = (self.pos[0] + dr, self.pos[1] + dc)

        return self.remember_action(action)

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
