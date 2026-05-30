"""
Author: Dr Zhibin Liao
Organisation: School of Computer Science and Information Technology, Adelaide University
Date: 26-Apr-2026
Description: This Python script illustrates how we may assess your agent in Gradescope.
Your version of this file won't be used in Gradescope Autographing.

The script is a part of Assignment 3 made for the course ARTI 2003 Artificial Intelligence for the year
of 2026. Public distribution of this source code is strictly forbidden.
"""


from my_agent import MyAgent
from random_agent import RandomAgent
from console import PygameApp
from utils import load_config
import numpy as np

agent = MyAgent()
# agent = RandomAgent()
scores = []
num_runs = 10000
config = load_config(cave_name='large')
for i in range(num_runs):
    score, _ = PygameApp(agent=agent, config=config).run()
    scores.append(score)
print(f'Success rate: ', np.sum((np.array(scores) > 0))/num_runs)