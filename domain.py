from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterable


Direction = tuple[int, int]

Directions = list[Direction]

UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
RIGHT: Direction = (1, 0)
LEFT: Direction = (-1, 0)

COLOR_VISITED = "\033[92m"
COLOR_PATH = "\033[91m"
COLOR_QUEUE = "\033[94m"
COLOR_NORM = "\033[0m"

directions: Directions = [UP, DOWN, LEFT, RIGHT]


class Position:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.el = 0

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return (self.x_coord == other.x_coord) and (self.y_coord == other.y_coord)
        return False

    def __str__(self) -> str:
        return f"x:{self.x_coord}, y:{self.y_coord}"

    def __hash__(self) -> int:
        return hash((self.x_coord, self.y_coord))

    def __iter__(self):
        return iter(self.x_coord, self.y_coord)

    def set_el(self, el: int):
        self.el = el


class Dimensions:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class IAgent(ABC):

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def set_grid(self, grid: IGrid):
        pass

    @abstractmethod
    def visited(self) -> set[Position]:
        pass

    @abstractmethod
    def position(self) -> Position:
        pass

    @abstractmethod
    def to_explore(self) -> deque[Position]:
        pass

    @abstractmethod
    def optimal_path(self) -> list[Position]:
        pass

    @abstractmethod
    def neighbors(self) -> list[Position]:
        pass

    @abstractmethod
    def seen(self) -> set[Position]:
        pass


class IGrid(ABC):

    @abstractmethod
    def start(self) -> Position:
        pass

    @abstractmethod
    def goal(self) -> Position:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def set_finished(self):
        pass

    @abstractmethod
    def walls(self) -> list[Position]:
        pass

    @abstractmethod
    def add_agent(self, agent: IAgent):
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def move_agents(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def get_el(self, pos: Position) -> int:
        pass

    @abstractmethod
    def set_el(self, pos: Position, el: int):
        pass

    @abstractmethod
    def set_els(self, pos1: Position, pos2: Position, el: int):
        pass

    @abstractmethod
    def is_valid(self, pos: Position) -> bool:
        pass
