## Tips

### Do I Need to Understand the Emulator?

Yes and no. It definitely helps if you understand the emulator logic, but it is not absolutely necessary. You can
assume the emulator will do:

1. Supply you with senses.
2. Execute your action.
3. Update the game window and calculate the score.
4. Repeat from step 1 unless the agent exits or dies.

### Build Conversion Tables

There are a few things that can be confusing, so it is better to make sure you get them right from the beginning:

1. How you index the agent's facing. Do you want to represent it as a direction or a coordinate offset, such as `W` or `(0, -1)`?
2. How you represent neighbouring locations relative to a location.
3. What the agent's new facing will be after a `LEFT` or `RIGHT` turn. It is often easiest to define this explicitly first.

Building conversion tables and reusing them whenever needed helps minimise errors, and even if a conversion is wrong,
you can correct it easily in one place. You may also want to build inverse mappings for already defined tables such as the one below.

```
VECTORS = {
    "N": (1, 0),
    "E": (0, 1),
    "S": (-1, 0),
    "W": (0, -1),
}
```

### Well Begun Is Half Done

Start coding by trying the `empty` cave. The logic you want to implement is:

Phase 1: Exploration

1. Travel all the locations in a cave until there is no location left to explore.
2. Transition to Phase 2.

Phase 2: Exit the cave

1. Go back to where the agent spawned.
2. Exit at the spawn location.

This is harder than it looks. Here your agent needs to build an internal model of the world. The emulator does not
tell the agent where it is, not even for the initial location.
Therefore, your agent needs to update its internal model with each newly discovered location, remember the senses encountered at
each location, and keep track of the cave boundary and unexplored frontier.
To do that, you will first need to implement a node data structure that records the locations your agent
enters and keeps track of their neighbours.
Many later steps depend on the functionality of this node data structure.

Here are some things you may find useful:
1. Your agent will probably want to maintain a `list` or `dict` of known nodes.
2. When you enter a new location, you probably want the previous location to be registered as a neighbour of the new node.
3. When you create a new node, you may want to add hypothetical **unexplored** neighbours to it,
and/or add those nodes to an unexplored `list`. Either approach makes it easier to track locations that have not been explored yet.
4. If `FORWARD` results in a `BUMP`, you probably know more than just the fact that the square in front is a wall.
You can assume the world is always rectangular, so bumping into a wall on the same side repeatedly is probably unnecessary.
5. After there are no more unexplored nodes, you want to enter phase 2 and go back to the initial location, regardless of
where you are. Does this sound familiar? Yes, this is what assignment 2 was all about. Please check the given
pathfinder implementations in [support_functions.md](support_functions.md).

### Find the Gold!

Once your agent can handle the `empty` level, congratulations, this part is easier.
Load the second map as `gold`. This will randomly place one piece of gold in the cave. Your goal is to find the gold and
return to the spawn location. This should give your agent a positive score unless it wanders too much
through the map.

Here, you need one or two additional phases, depending on how you think about it: namely, gold found and gold grabbed.
These phases are essentially the agent's internal representation of game state. You will want to define the states,
perhaps draw them on paper, and think carefully about which events, such as changed senses combined with prior actions,
define the transitions between them. Then ask yourself what the agent should do in each state.
The simplest version in this example is:
```
if Glimmer:
    state = GOLD_FOUND
    next_action = GRAB
elif not Glimmer:
    if last_action == GRAB:
        state = GOLD_GRABBED  # or state = EXIT
        next_action = plan_route_to_exit()
```

The structure used here is called a [Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine). If you have not heard of
the topic before, it pays to read about it.

### Dancing Around Pits

Use the `breeze_and_gold` cave option to activate this level.

Once the above is done, the logic part really begins. Here, you do not need to implement propositional
logic expressions, inference rules, or any of the pseudocode from the module reading. Simple if-else statements can
cover the logic just fine.

If there is a breeze, it indicates that at least one pit is nearby.
However, what you really want to know is whether a location is safe, given that some of its neighbours are breeze squares. If it is safe, your agent can move there.
If not, avoid going there or passing through it.

There will be situations in which you have not found the gold, but all safe locations have already been explored. In that case, you may need to take a risk
and try one of the unsafe locations suggested by a breeze. That means you should form a strategy for choosing the least risky location.

### Now Our Dear Wumpus

The Wumpus is the last thing we try to deal with because it has the most complex logic.
You can now try the `default` level, which gives you the full version of the game with one Wumpus, several pits, and one
gold.

We do not want to take the fun out of implementing this part, so here are a few questions that may help if you get stuck.

1. Does the Wumpus have to die?
2. What is the exact mechanical difference between a Wumpus and a pit?
3. What is the true purpose of SHOOT?

If you are unsure about the third question, try the `siege` map.

### Generalisation

After you have conquered the default level, congratulations: now we check your agent's generalisation ability.
You may have hardcoded certain knowledge in your agent, for example, the agent may assume it always starts at [1,1].
The `large` map will place your agent randomly at one of the four corners so you can check whether your agent fails
at one of those randomly generated maps.

### Debugging with Your Eyes

If you do not know how to use a modern IDE or how to place a breakpoint, it is unlikely that you will be able to make the
agent behave correctly. In fact, it is a warning sign if a student does not know how to debug yet submits a solution that
works perfectly. If you do not already know how to use breakpoints, please start learning today.

The emulator is designed with visual aids to help you understand what the action has done.
However, the agent itself has its own internal belief of the world, and it may differ from the actual world.
We would suggest that you create your own print function so you can display the agent's internal map of where
it is, where it is going, and where it believes the walls, pits, and Wumpus are. You can visually assess those details quite easily to help you
debug.


Portals:
* [Main Page](../README.md)
* [Task Description](task_description.md)
* [Evaluation](evaluation.md)
* [Support Functions](support_functions.md)
* Tips <--- you are here
