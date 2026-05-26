## Task Description

This section walks you through the main components you need to change to complete the assignment.

You will implement a `MyAgent` in a file called `my_agent.py`. Your agent class should inherit from the `Agent` class defined in [agent.py](../agent.py).
You will mainly implement the `update` and `act` functions shown below. There are also a few other class functions that you should read and may want to modify.

```python
from agent import Agent
class MyAgent(Agent):
    def update(self, senses):
        ...

    def act(self):
        ...
```

If you choose not to inherit from the `Agent` class, that is probably fine, but please make sure the file name, class name,
and required functions match exactly. Otherwise, the Gradescope autograder will fail.


### Sense Updates

For the `update()` function, the `senses` input is a dictionary of booleans containing the five senses provided by the emulator:
```Python
senses = {
    "Stench": True, # A Wumpus causes Stench in adjacent locations
    "Breeze": False, # A pit (hole) causes Breeze in adjacent locations
    "Glimmer": False, # Gold causes Glimmer in its own location
    "Bump": False, # Bump happens when the agent runs into a wall
    "Scream": False, # Scream is broadcast to adjacent locations when the Wumpus is dead.
}
```

The `update()` function in the parent `Agent` class automatically records this in `self.last_senses`.

### Performing Actions

The `act()` function is where you decide which action the agent should take. The agent can perform one of the following actions:

```
ACTIONS = ["FORWARD", "LEFT", "RIGHT", "GRAB", "SHOOT", "EXIT", "NO_ACTION"]
```

Here are a few important details about these actions:

1. `FORWARD` can result in a `Bump` if the agent runs into a wall.
2. `SHOOT` is a one-time action. The emulator tracks whether the arrow has already been used. If it has, further `SHOOT` actions have no effect, but they still count as actions and still incur the `-10` penalty.
3. `GRAB` and `EXIT` can be used any number of times. Using `GRAB` on a square without gold, or `EXIT` away from the spawn location, is allowed but has no effect other than the normal action penalty of `-1`.
4. `NO_ACTION` is still an action. If your agent needs to do nothing for a turn, for example while changing internal state, you may return `NO_ACTION`, which does not incur an action penalty. However, in silent mode it still counts toward the action limit so the grader does not get stuck in an infinite no-action loop. The limit is controlled by `emulator.max_agent_actions: 1000` in [game_config.yaml](../game_config.yaml).

Here is the scoring configuration table from [game_config.yaml](../game_config.yaml):
```yaml
scoring: # Score values applied by the emulator.
  action: -1 # Score change for every valid action. no action is also an action, agent should return no action is no action is made
  shoot: -9 # Additional score change when shooting the arrow.
  death: -100 # Score change when the agent dies.
  gold: 100 # Score change for each collected gold piece.
  no_action: 0 # NO_ACTION has no score penalty, but it still increases the step count in the silent mode.
```

### Simplification

1. The Wumpus, gold, and pits will not overlap in the same location.
2. There is always one Wumpus and one gold.
3. For the cave maps `empty`, `gold`, `breeze_and_gold`, and `default`, you can assume the agent spawns at location `[1,1]`.

### Game Execution

The emulator will run your agent in the following kind of game loop. The real game loop looks slightly different.
If you are interested, please take a look at `_run_visual()` and `_run_silent()` in the [console.py](../console.py).

```python
while agent_active
    agent.update({'STENCH': True, 'BREEZE':False, 'GLIMMER':False, 'BUMP':False, 'SCREAM':False})
    agent_move = agent.act()
    updateGame(agent_move)
```

In other words, the game loop passes in the most recent senses based on the agent's last action, after which the agent must choose a new action. `updateGame()` then changes the game state based on the chosen action.
In [console.py](../console.py), you will not find an exact function called `updateGame()`. That logic is captured in the following block from `_run_visual()`, and similarly in `_run_silent()`:
```python
if action:
    start_position = self.game.position
    action_applied = self.game.apply_action(action)
    if action_applied:
        senses = self.game.senses()
        self.agent.update(senses)
        self.game.log_senses(action, senses, start_position=start_position)
        self.last_agent_action_time = pygame.time.get_ticks()
else:
    raise ValueError('Agent must not return None as an action. If no action is required, return "NO_ACTION"')
```


### Game Finishing Conditions

A score is kept for each cave.
The score is finalised when the player exits the cave, is killed by the Wumpus, or falls into a pit.
In silent mode, a game is forcibly ended when the action count reaches the limit.
In visual mode, the `New Cave` and `Exit Game` interface buttons can interrupt the game.

### Example Agent

If you find it difficult to make your own agent from scratch, try `random_agent.py` as an example starting point.

```bash
python random_agent.py --cave gold
```


### Cave Grid Indexing in the Emulator

- Internal coordinates use zero-based `(row, column)` tuples.
- The UI displays one-based `[row, column]` positions.

### Agent Initial Knowledge

The emulator does not tell the agent where it is or which direction it faces. In general, this is not really an issue.
At first, you may assume that the agent starts at `[1, 1]` and faces east, since this is the emulator's default setting for the initial levels.
Once you clear all levels of the game, you will find that these initial assumptions do not matter.

The agent always carries an arrow at the start of each cave. There is only one gold and one Wumpus in the assessable levels.

### Submission

Please only submit your `my_agent.py` and any necessary helper `.py` files **you created**. We will not use any of the files
we release to you, even if you submit them, in case you accidentally modified the game behaviour.

Portals:
* [Main Page](../README.md)
* Task Description <--- you are here
* [Evaluation](evaluation.md)
* [Support Functions](support_functions.md)
* [Tips](tips.md)
