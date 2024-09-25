from domain import IAgent, Position, IGrid, directions
from collections import deque
from utils import translate


def new_dfs_agent()->IAgent:
    return DfsAgent()

class DfsAgent(IAgent):
    def __init__(self) -> None:
        self._visited: set[Position] = set()
        self._stack: deque[Position] = deque()
        self._path: list[Position] = []

    def set_grid(self, grid: IGrid):
        self.grid = grid
        self._position = grid.start()

    def position(self) -> Position:
        return self._position
    
    def visited(self) -> set[Position]:
        return self._visited
    
    def to_explore(self) -> deque[Position]:
        return self._stack

    def _mark_visited(self):
        self._visited.add(self._position)
    
    def _push_stack(self, pos: Position):
        self._stack.append(pos)
    
    def _pop_stack(self):
        self._position = self._stack.pop()
        self._path.append(self._position)
  
    def next(self):
        if len(self._stack) > 0:
            self._pop_stack()
        if self._position == self.grid.goal():
            self.grid.set_finished()
        self._mark_visited()
        self._add_neighbors()
    
    def neighbors(self) -> list[Position]:
        neighbors = []
        for direction in directions:
            neighbor: Position = translate(self._position, direction)
            neighbors.append(neighbor)
        return neighbors
    
    def _in_stack(self, pos: Position)->bool:
        return pos in self._stack
        
    def _add_neighbors(self)->None:
        for direction in directions:
            nghbr: Position = translate(self._position, direction)
            is_visited = self._is_visited(nghbr)
            is_valid = self._is_valid_pos(nghbr)
            in_stack = self._in_stack(nghbr)
            if ((not is_visited) and is_valid and (not in_stack)):
                self._push_stack(nghbr)

    def _is_visited(self, pos: Position):
        return pos in self._visited
    
    def _is_valid_pos(self, position: Position)->bool:
        valid_x = 0 <= position.x_coord <= (self.grid.width() - 1)
        valid_y = 0 <= position.y_coord <= (self.grid.height() -1)
        not_wall = position not in self.grid.walls()
        return valid_x and valid_y and not_wall

