# Introduction
# This assignment introduces students to the implementation of Artificial Intelligence
# search algorithms using Python.
# Objectives
# Implementing a grid-based search algorithm in Python using functions, arrays, and
# 2D arrays. The assignment focuses on building a modular and structured program
# through step-by-step process.


import time
import bfs_agent
import dfs_agent
from domain import IAgent
from grid import (
    Grid,
    hard_coded_grid,
    user_input_grid,
    COLOR_NORM,
    COLOR_PATH,
    COLOR_QUEUE,
    COLOR_VISITED,
    int_input_with_limits,
    elevation_mapping,
    PositionChar,
)
import os

import ufs_agent


def print_stats(agent: IAgent) -> None:
    print(
        f"visited ({PositionChar.VISITED.value}): ",
        len((agent.visited())),
    )
    print(
        f"queue ({PositionChar.QUEUE.value}): ",
        len(set(agent.to_explore())),
    )
    if type(agent) == bfs_agent.BfsAgent:
        print(
            f"optimal path ({PositionChar.PATH.value}) steps: ",
            len((agent.shortest_path)),
        )
    for elevation in range(6):
        color_code = elevation_mapping[elevation].value
        print(f"{color_code}Elevation {elevation}\033[0m")
    if type(agent) == ufs_agent.UfsAgent:
        print(f"agent._cost: {agent._cost}")


if __name__ == "__main__":

    grid = hard_coded_grid()
    print(f"Welcome to Will Lapinel's {COLOR_VISITED}BFS Simulator!{COLOR_NORM}")
    custom = input('Customize settings? "Y" (any other key to use default settings)? ')
    if custom.lower() == "y":
        grid = user_input_grid()
    agent_type_prompt = """
                       Enter agent type:\n
                       1. Breadth-First Search agent\n
                       2. Depth-First Search agent\n
                       3. Uniform Cost Search agent\n
                       """
    agent_type = int_input_with_limits(1, 3, agent_type_prompt)
    agent = None
    if agent_type == 1:
        agent = bfs_agent.new_bfs_agent()
    elif agent_type == 2:
        agent = dfs_agent.new_dfs_agent()
    elif agent_type == 3:
        agent = ufs_agent.new_ufs_agent()
    else:
        raise ValueError
    grid.add_agent(agent)
    max_iterations = 1000
    print("\033[?25l", end="")
    for i in range(max_iterations):
        print("\033[H", end="")
        if i != max_iterations - 1:
            if os.name == "nt":
                os.system("cls")
            # For Mac and Linux
            else:
                os.system("clear")
        if grid.is_finished():
            print("Goal reached!")
            print_stats(agent)
            grid.render()
            time.sleep(2)
            print("\033[?25h", end="")
            exit()
        grid.move_agents()
        print_stats(agent)
        grid.render()
        time.sleep(0.1)
    print("Max iterations reached!")
