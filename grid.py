from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from turtle import bgcolor
from bfs_agent import BfsAgent
from domain import (
    IAgent,
    IGrid,
    Position,
    Dimensions,
    COLOR_NORM,
    COLOR_PATH,
    COLOR_QUEUE,
    COLOR_VISITED,
)
from utils import int_input_with_limits, translate

import domain

from enum import Enum


class PositionChar(Enum):
    AGENT = "A"
    START = "S"
    GOAL = "G"
    WALL = "#"
    VISITED = "o"
    QUEUE = "*"
    PATH = "="
    DEFAULT = " "


class ElevationColor(Enum):
    LOWEST = "\033[38;5;21m"  # Deep Blue
    LOW = "\033[38;5;51m"  # Cyan
    MID = "\033[38;5;46m"  # Green
    HIGHER = "\033[38;5;226m"  # Yellow
    HIGH = "\033[38;5;214m"  # Orange
    HIGHEST = "\033[38;5;196m"  # Red


# Example usage
def print_elevation(elevation):
    color = ElevationColor(elevation).value
    print(f"{color}Elevation Level {elevation}\033[0m")


# Map elevations from 0 to 5 to their corresponding enum members
elevation_mapping = {
    0: ElevationColor.LOWEST,
    1: ElevationColor.LOW,
    2: ElevationColor.MID,
    3: ElevationColor.HIGHER,
    4: ElevationColor.HIGH,
    5: ElevationColor.HIGHEST,
}

# Example: Printing elevation levels


def new_grid(
    dimensions: Dimensions, start: Position, goal: Position, walls: list[Position]
) -> IGrid:
    return Grid(dimensions, start, goal, walls)


class Grid(domain.IGrid):
    def __init__(
        self,
        dimensions: Dimensions,
        start: Position,
        goal: Position,
        walls: list[Position],
    ):
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
        self.el_map: list[list[int]] = [
            [0 for _ in range(self._dimensions.width)]
            for _ in range(self._dimensions.height)
        ]

    def get_el(self, pos: Position) -> int:
        return self.el_map[pos.x_coord][pos.y_coord]

    def set_el(self, pos: Position, el: int):
        self.el_map[pos.x_coord][pos.y_coord] = el

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

    def is_valid(self, pos: Position) -> bool:
        valid_x = 0 <= pos.x_coord <= (self._dimensions.width - 1)
        valid_y = 0 <= pos.y_coord <= (self._dimensions.height - 1)
        not_wall = pos not in self._walls
        return valid_x and valid_y and not_wall

    def _color(self, pos: Position) -> str:
        el = self.get_el(pos)
        return elevation_mapping[el].value

    def _char(self, pos: Position) -> str:
        if pos in self._agents[0].seen():
            if pos == self._goal:
                return PositionChar.GOAL.value
            if pos == self._start:
                return PositionChar.START.value
            if pos in self._walls:
                return PositionChar.WALL.value
            for agent in self._agents:
                if pos == agent.position():
                    return PositionChar.AGENT.value
                if type(agent) == BfsAgent:
                    if pos in agent.shortest_path:
                        return PositionChar.PATH.value
                if pos in agent.visited():
                    return PositionChar.VISITED.value
                if pos in agent.to_explore():
                    return PositionChar.QUEUE.value
        return PositionChar.DEFAULT.value

    def render(self) -> None:
        padding = 2
        gap_str = " " * padding
        print()
        for row in range(self._dimensions.height):
            for column in range(self._dimensions.width):
                curr_pos = Position(column, row)
                print(
                    f"{self._color(curr_pos)}{self._char(curr_pos)}{COLOR_NORM}",
                    end=gap_str,
                )
            print()
        print()


def user_input_grid() -> domain.IGrid:
    """Get input via command line for grid dimensions, start position and goal position."""
    width = int_input_with_limits(0, 50, "Enter grid width: ")
    height = int_input_with_limits(0, 50, "Enter grid height: ")
    dimensions = Dimensions(width, height)
    start_x = int_input_with_limits(
        0, dimensions.width - 1, "Enter starting x coordinate: "
    )
    start_y = int_input_with_limits(
        0, dimensions.height - 1, "Enter starting y coordinate: "
    )
    start = Position(start_x, start_y)
    goal_x = int_input_with_limits(0, dimensions.width - 1, "Enter goal x coordinate: ")
    goal_y = int_input_with_limits(
        0, dimensions.height - 1, "Enter goal y coordinate: "
    )
    goal = Position(goal_x, goal_y)
    done_walls = False
    walls: list[Position] = []
    while not done_walls:
        done_walls_input = input('Enter walls? (any key for yes, or "N" for no): ')
        done_walls = done_walls_input.lower() == "n"
        if done_walls:
            break
        wall_count = 1
        wall_x = int(input(f"Enter wall {wall_count} x coordinate"))
        assert 0 <= wall_x < width
        wall_y = int(input(f"Enter wall {wall_count} y coordinate"))
        assert 0 <= wall_y < height
        wall = Position(wall_x, wall_y)
        walls.append(wall)
    return Grid(dimensions, start, goal, walls)


def generate_random() -> tuple[Dimensions, Position, Position]:
    raise NotImplementedError


def hard_coded_grid() -> IGrid:
    walls = [
        Position(5, 6),
        Position(6, 14),
        Position(17, 12),
        Position(16, 12),
        Position(15, 12),
        Position(14, 12),
        Position(13, 12),
        Position(13, 13),
        Position(13, 14),
        Position(13, 15),
        Position(13, 16),
        Position(13, 17),
        Position(13, 18),
        Position(13, 19),
        Position(13, 19),
        Position(19, 18),
        Position(8, 9),
        Position(6, 4),
    ]
    grid = Grid(Dimensions(20, 20), Position(2, 3), Position(16, 18), walls)
    for i in range(15):
        grid.set_el(Position(i, 4), 1)
    for i in range(15):
        grid.set_el(Position(i + 5, 5), 2)
    for i in range(15):
        grid.set_el(Position(i, 6), 3)
    return grid
