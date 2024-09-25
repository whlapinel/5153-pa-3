
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from turtle import bgcolor
from bfs_agent import BfsAgent
from domain import IAgent, IGrid, Position, Dimensions, COLOR_NORM, COLOR_PATH, COLOR_QUEUE, COLOR_VISITED
from utils import int_input_with_limits, translate

import domain


class Grid(domain.IGrid):
    def __init__(self, dimensions: Dimensions, start: Position, goal: Position, walls: list[Position]):
        self._dimensions = dimensions
        self._start = start
        assert start not in walls, "Start cannot be on a wall."
        assert 0 <= self._start.x_coord <= (dimensions.width - 1)
        assert 0 <= self._start.y_coord <= (dimensions.height - 1)
        self._goal = goal
        assert goal not in walls, "Goal cannot be on a wall."
        assert 0 <= self._goal.x_coord <= (dimensions.width - 1)
        assert 0 <= self._goal.y_coord <= (dimensions.height - 1)
        assert start != goal
        self._agents: list[IAgent] = []
        self._walls: list[Position] = walls
        self._finished = False
    
    def start(self):
        return self._start
    
    def goal(self):
        return self._goal
    
    def width(self) -> int:
        return self._dimensions.width
    
    def height(self) -> int:
        return self._dimensions.height
    
    def add_agent(self, agent: IAgent):
        self._agents.append(agent)
        agent.set_grid(self)

    def move_agents(self):
        for agent in self._agents:
            agent.next()

    def set_finished(self):
        self._finished = True

    def is_finished(self) -> bool:
        return self._finished

    def walls(self) -> list[Position]:
        return self._walls
            
    def render(self)->None:
        padding = 2
        gap_str = ' '*padding
        print()
        for row in range(self._dimensions.height):
            for column in range(self._dimensions.width):
                curr_pos = Position(column, row)
                agent_at_start = False
                for agent in self._agents:
                    color = COLOR_NORM
                    if curr_pos in agent.visited():
                        color = COLOR_VISITED
                    else:
                        color = COLOR_NORM
                    if agent.position() == curr_pos:
                        print(f'A', end=gap_str)
                        if agent.position() == self._start:
                            agent_at_start = True
                    elif self._start == curr_pos and not agent_at_start:
                        print('S', end=gap_str)
                    elif self.goal() == curr_pos:
                        print('G', end=gap_str)
                    elif curr_pos in self._walls:
                        print('#', end=gap_str)
                    else:
                        if curr_pos in agent.to_explore():
                            color = COLOR_QUEUE
                        if type(agent) == BfsAgent:
                            if curr_pos in agent.shortest_path:
                                color = COLOR_PATH
                        print(f'{color}.{COLOR_NORM}', end=gap_str)
            print()
        print()

    


        



def user_input_grid()->domain.IGrid:
    """Get input via command line for grid dimensions, start position and goal position."""
    width = int_input_with_limits(0, 50, 'Enter grid width: ')
    height = int_input_with_limits(0, 50, 'Enter grid height: ')
    dimensions = Dimensions(width, height)
    start_x = int_input_with_limits(0, dimensions.width-1, 'Enter starting x coordinate: ')
    start_y = int_input_with_limits(0, dimensions.height-1, 'Enter starting y coordinate: ')
    start = Position(start_x, start_y)
    goal_x = int_input_with_limits(0, dimensions.width-1, 'Enter goal x coordinate: ')
    goal_y = int_input_with_limits(0, dimensions.height-1, 'Enter goal y coordinate: ')
    goal = Position(goal_x, goal_y)
    done_walls = False
    walls: list[Position] = []
    while not done_walls:
        done_walls_input = input('Enter walls? (any key for yes, or "N" for no): ')
        done_walls = done_walls_input.lower() == 'n'
        if done_walls: 
            break
        wall_count = 1
        wall_x = int(input(f'Enter wall {wall_count} x coordinate'))
        assert 0 <= wall_x < width
        wall_y = int(input(f'Enter wall {wall_count} y coordinate'))
        assert 0 <= wall_y < height
        wall = Position(wall_x, wall_y)
        walls.append(wall)
    return Grid(dimensions, start, goal, walls)

def generate_random()->tuple[Dimensions, Position, Position]:
    raise NotImplementedError

def hard_coded_grid()->IGrid:
    walls = [
        Position(5,6), 
        Position(6,14), 
        Position(17,12), 
        Position(16,12), 
        Position(15,12), 
        Position(14,12), 
        Position(13,12), 
        Position(13,13), 
        Position(13,14), 
        Position(13,15), 
        Position(13,16), 
        Position(13,17), 
        Position(13,18), 
        Position(13,19), 
        Position(13,19), 
        Position(19,18), 
        Position(8,9),
        Position(6,4), 
        ]
    return Grid(Dimensions(20, 20), Position(2,3), Position(16,18), walls)
