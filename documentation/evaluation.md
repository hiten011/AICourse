## Evaluation

We will run your agent several times against fixed and randomly generated caves. Please make sure your agent is implemented
as the `MyAgent` class in `my_agent.py`.
We will initialise your agent as shown below:

```python
from my_agent import MyAgent

my_agent = MyAgent()
```

### Test Caves
The test caves are defined in the
[cave_config.yaml](../cave_config.yaml). Specifically, we test the following five caves:

1. `gold`: one piece of gold is placed randomly.
2. `breeze_and_gold`: there is one gold and two pits.
3. `default`: this has one gold, one to three pits, and one Wumpus.
4. `siege`: a 5x5 case in which the agent must take a risk. There is one Wumpus and one pit adjacent to the spawn location; the given siege map is only one possible arrangement.
5. `large`: a larger randomly generated map with a random corner start location and 2-4 pits.

The cave definitions are provided under the `maps` folder.
There are also several extra hardcoded caves you can try out.

### Evaluation Criteria

Successfully finishing a cave means achieving a score greater than zero.
In many cases, a logical agent will eventually have to guess, and it may die because of an unlucky
choice. Therefore, to test your code, we will use a Gradescope testing script similar to [assessor.py](../assessor.py), which
calculates your agent's probability of achieving a positive score:

```python
from my_agent import MyAgent
from random_agent import RandomAgent
from console import PygameApp
from utils import load_config
import numpy as np

# agent = MyAgent()
agent = RandomAgent()
scores = []
num_runs = 100
config = load_config(cave_name='gold')
for i in range(num_runs):
    score, _ = PygameApp(agent=agent, config=config).run()
    scores.append(score)
print(f'Success rate: ', np.sum((np.array(scores) > 0))/num_runs)
```

We set the passing bar for each level as follows:

| Level           | Minimum Success Rate | Awarded Marks |
|-----------------|----------------------|---------------|
| gold            | 0.99                 | 2             |
| breeze_and_gold | 0.60                 | 2             |
| default         | 0.60                 | 2             |
| siege           | 0.70                 | 2             |
| large           | 0.70                 | 2             |

Portals:
* [Main Page](../README.md)
* [Task Description](task_description.md)
* Evaluation <--- you are here
* [Support Functions](support_functions.md)
* [Tips](tips.md)
