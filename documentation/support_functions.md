## Support Functions

We provide several support features. They are mainly designed to help you observe issues when your
agent is not doing what you intended.


### Emulator Side

#### Visual Aids

We added a number of visuals to the game window to help you debug.
1. `Bump` and `Shoot` leave a trace showing which location was affected.
2. The walls are drawn so you can easily see their location indices instead of tracking them mentally.
3. The gold and Wumpus images change after they are affected.
4. The start location is coloured differently to show where the agent spawned.
5. Reveal mode keeps explored and unexplored cells visually distinct.
6. Recent percepts are shown so you can see what happened.

#### Map (Cave Profile) Saver and Loader

This is a handy feature, but it is disabled by default. When you debug your code in visual mode, you may want to
turn it on so the emulator records the last generated cave map to `maps/last.txt`.
That gives you a reproducible map for debugging. Please make sure you copy the map to another file, similar to the other
hardcoded maps, and then reload it by extending `cave_config.yaml` with a new cave:

```yaml
  my_debug_cave:
    map_file: maps/my_debug_cave.txt
```
You can then select this cave by changing the `--cave` argument when running `my_agent.py`.
You may also define your own map by editing the existing maps.
By default, `emulator.save_last_map` is disabled to reduce I/O operations.

#### Hardcoded Map Format

Text maps are written one character per cell, with the first map row representing the top cave row.

Markers:

- `S`: start location
- `.`: empty
- `W`: Wumpus
- `P`: pit
- `G`: gold

#### Customising Random Caves

In `cave_config.yaml`, the cave profile section supports random cave generation via the following parameters:

- `width`, `height`
- `start`: the agent's spawn location
- `seed`: if you want to control the cave generation sequence
- `wumpus`: whether to place a Wumpus; for this assignment this is normally enabled
- `pit_probability`: controls how likely pits are to appear
- `pits`: lower and upper bounds on the number of pits
- `gold`: lower and upper bounds on the amount of gold
- `map_file`: if a map is given, the rest of the cave-generation parameters above are ignored

#### Other Game Configurations

If the agent is acting too fast, you can change `agent_action_delay_ms` in the [game_config.yaml](../game_config.yaml) to slow it down.

```yaml
emulator: # Visual emulator parameters.
  show_window: false # When false, run one agent game with no pygame window and print the final score.
  max_agent_actions: 1000 # Safety cap for no-window runs.
  suppress_agent_output: true # When running without a window, hide agent debug prints and show only final score.
  recent_percepts_limit: 15 # Number of recent percept entries to show.
  agent_action_delay_ms: 250 # Minimum delay between agent actions in milliseconds.
  window_width: 1100 # Width of the pygame window in pixels.
  window_height: 780 # Height of the pygame window in pixels.
  board_left: 48 # Left pixel position of the board.
  board_top: 72 # Top pixel position of the board.
  cell_size: 116 # Width and height of each board cell in pixels.
  save_last_map: false # Whether to dump the spawned cave map after each new world is created.
  last_map_file: maps/last.txt # Text map path used when save_last_map is enabled.
```

## Agent Side

At some point, you will probably want a function that tells you how to navigate from location A to
location B. That should sound familiar: it is what assignment 2 was about. To avoid repeating that work by reading from a text file and
printing to the screen again, we provide implementations of pathfinding algorithms.
If you want to keep using your own assignment 2 pathfinders, please feel free to do so.

### BFS and UCS Functions
We provide `pathfinder.py` with vibe-coded `bfs` and `ucs` solvers. Please read the function descriptions for
their intended usage. The input arguments follow the assignment 2 specification, except that the values in the `grid`
mean something different here. Any numeric values you put in the grid represent travel cost rather than elevation.
This simplifies the calculation and makes the grid easier to construct.
You can also use `X` to indicate a location you do not want the agent to travel through, although an arbitrarily
large value would also work.
In this assignment, `bfs` is sufficient, but `ucs` gives you fine-grained travel control if you need.

Portals:
* [Main Page](../README.md)
* [Task Description](task_description.md)
* [Evaluation](evaluation.md)
* Support Functions <--- you are here
* [Tips](tips.md)
