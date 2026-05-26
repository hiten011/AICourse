import argparse
from collections import deque

from agent import Agent
from console import PygameApp
from utils import load_config
from definitions import ACTIONS, SENSE_NAMES, DIRECTIONS, VECTORS
from kb import KnowledgeBase, CellStatus


class MyAgent(Agent):

    def __init__(self):
        self.kb = KnowledgeBase()
        self.pos = (0, 0)
        self.prev_pos = (0, 0)
        self.facing_idx = 1          # start facing East
        super().__init__()

    def reset(self):
        super().reset()
        self.kb.reset()
        self.pos = (0, 0)
        self.prev_pos = (0, 0)
        self.facing_idx = 1

    def update(self, senses):
        super().update(senses)
        self.kb.mark_visited(self.pos)

        if senses['Breeze']:
            print(f"[{self.pos}] Breeze")
            self.kb.mark_breeze(self.pos)
            
        if senses['Stench']:
            print(f"[{self.pos}] Stench")
            self.kb.mark_stench(self.pos)

        if senses['Glimmer']:
            print(f"[{self.pos}] Glimmer")
            self.kb.mark_glimmer(self.pos)

        if senses['Bump']:
            print(f"[{self.pos}] Bump")
            self.kb.mark_wall(self.pos)
            self.pos = self.prev_pos # back to prev position

        if senses['Scream']:
            print(f"[{self.pos}] Scream")

        if not any(senses.values()):
            print(f"[{self.pos}] Empty Cell")
            self.kb.mark_empty(self.pos)

    def act(self):
        self.prev_pos = self.pos

        # TODO: replace with real decision logic
        return self.remember_action('NO_ACTION')

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
