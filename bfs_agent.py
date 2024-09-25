from collections import deque
from domain import IAgent, IGrid, Position, directions
from utils import translate


def new_bfs_agent()->IAgent:
    return BfsAgent()

class BfsAgent(IAgent):

    def __init__(self) -> None:
        self._visited: set[Position] = set()
        self.queue: deque[Position] = deque()
        self.parents: dict[Position, Position]= {}
        self.shortest_path: list[Position] = []

    def position(self) -> Position:
        return self._position

    def set_grid(self, grid: IGrid):
        self.grid = grid
        self._position = grid.start()
        self.goal = grid.goal()

    def _mark_visited(self, pos: Position):
        self._visited.add(pos)

    def _is_visited(self, pos: Position):
        return pos in self._visited
    
    def _in_queue(self, pos: Position) -> bool:
        return pos in self.queue

    def _enqueue_cell(self, pos: Position):
        self.queue.append(pos)

    def visited(self) -> set[Position]:
        return self._visited

    def next(self):
        self._add_neighbors()
        self._position = self.queue.popleft()
        self._mark_visited(self._position)
        if self._position == self.grid.goal():
            self._shortest_path()
            self.grid.set_finished()

    def to_explore(self) -> deque[Position]:
        return self.queue
    
    def neighbors(self) -> list[Position]:
        neighbors = []
        for direction in directions:
            neighbor: Position = translate(self._position, direction)
            neighbors.append(neighbor)
        return neighbors

    
    def _add_neighbors(self)->None:
        for direction in directions:
            neighbor_pos: Position = translate(self._position, direction)
            if (not self._is_visited(neighbor_pos) and not self._in_queue(neighbor_pos)) and (self._is_valid_pos(neighbor_pos)):
                self._enqueue_cell(neighbor_pos)
                self.parents[neighbor_pos] = self._position

    def _is_valid_pos(self, position: Position)->bool:
        valid_x = 0 <= position.x_coord <= (self.grid.width() - 1)
        valid_y = 0 <= position.y_coord <= (self.grid.height() -1)
        not_wall = position not in self.grid.walls()
        return valid_x and valid_y and not_wall
    
    def _shortest_path(self):
            finished = False
            while not finished:
                self.shortest_path.append(self.parents[self._position])
                self._position = self.parents[self._position]
                if self.position == self.grid.start():
                    finished = True
   