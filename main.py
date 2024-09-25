
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
import grid_agent
import os

def print_stats(agent: IAgent)->None:
            print('AGENT POSITION: ', agent.position())
            print('visited: ', len((agent.visited())), f' (marked in {grid_agent.COLOR_VISITED}green{grid_agent.COLOR_NORM})')
            print('queue: ', len(set(agent.to_explore())), f' (marked  in {grid_agent.COLOR_QUEUE}blue{grid_agent.COLOR_NORM})')
            if (type(agent)==bfs_agent.BfsAgent):
                print('optimal path steps: ', len((agent.shortest_path)), f' (marked  in {grid_agent.COLOR_PATH}red{grid_agent.COLOR_NORM})')
            print('Current neighbors: ')
            for neighbor in agent.neighbors():
                 print(neighbor)


if __name__ == '__main__':

    grid = grid_agent.hard_coded_grid()
    print(f"Welcome to Will Lapinel's {grid_agent.COLOR_VISITED}BFS Simulator!{grid_agent.COLOR_NORM}")
    custom = input('Customize settings? "Y" (any other key to use default settings)? ')
    if custom.lower() == 'y':
         grid = grid_agent.user_input_grid()
    agent_type_prompt = '''
                       Enter agent type:\n
                       1. Breadth-first agent\n
                       2. Depth-first agent\n
                       '''
    agent_type = grid_agent.int_input_with_limits(1, 2, agent_type_prompt)
    agent = None
    if agent_type == 1: 
        agent = bfs_agent.new_bfs_agent()
    elif agent_type == 2:
        agent = dfs_agent.new_dfs_agent()
    else:
         raise ValueError
    grid.add_agent(agent)
    max_iterations=1000
    print("\033[?25l", end="")
    for i in range(max_iterations):
        print("\033[H", end="")
        if i != max_iterations - 1:
            if os.name == 'nt':
                os.system('cls')
            # For Mac and Linux
            else:
                os.system('clear')
        if grid.is_finished():
            print('Goal reached!')
            print_stats(agent)
            grid.render()
            time.sleep(2)
            print("\033[?25h", end="")
            exit() 
        grid.move_agents()
        print_stats(agent)
        grid.render()
        time.sleep(0.1)
    print('Max iterations reached!')






