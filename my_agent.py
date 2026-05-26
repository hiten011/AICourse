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
        self.facing_idx = 1          # start facing East
        super().__init__()

    def reset(self):
        super().reset()
        self.kb.reset()
        self.pos = (0, 0)
        self.facing_idx = 1

    def update(self, senses):
        super().update(senses)

    def act(self):
        return ACTIONS[6]

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
