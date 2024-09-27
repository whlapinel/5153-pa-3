from collections import deque
from domain import IAgent, Position, IGrid, directions
import heapq
from utils import translate


def new_ufs_agent() -> IAgent:
    return UfsAgent()


class UfsAgent(IAgent):
    def __init__(self) -> None:
        self._visited: set[Position] = set()
        """For tracking positions already visited"""
        self._prty_queue = []
        """Priority queue that uses relative elevation of a position to determine cost"""
        self._pri_set: set = set()
        """For tracking positions already added to the queue"""
        self._cost = 0
        """Cumulative cost tracker"""
        self._neighbors: list[Position] = []
        """Current neighbors"""
        self._path: list[Position] = []
        """Path traveled"""
        self._counter = 0
        """For acting as a tie-breaker for the priority queue, ensuring it uses insertion order when costs are equal"""
        self._seen: set[Position] = set()

    def next(self):
        if len(self._prty_queue) > 0:
            self._cost, _, self._current = heapq.heappop(self._prty_queue)
            self._visited.add(self._current)
        if self._current == self._grid.goal():
            self._grid.set_finished()
        else:
            self._add_neighbors()

    def set_grid(self, grid: IGrid):
        self._grid = grid
        self._current: Position = grid.start()

    def visited(self) -> set[Position]:
        return self._visited

    def position(self) -> Position:
        return self._current

    def to_explore(self):
        positions_queue = deque(position for _, _, position in self._prty_queue)
        return positions_queue

    def neighbors(self) -> list[Position]:
        return self._neighbors

    def _push_to_queue(self, neighbor: Position):
        self._pri_set.add(neighbor)
        neighbor_el = self._grid.get_el(neighbor)
        cumulative_cost = self._cost + neighbor_el
        self._counter += 1
        heapq.heappush(self._prty_queue, (cumulative_cost, self._counter, neighbor))

    def seen(self) -> set[Position]:
        return self._seen

    def _add_neighbors(self):
        print(f"add neighbors called:")
        self._neighbors.clear()
        for direction in directions:
            neighbor = translate(self._current, direction)
            self._seen.add(neighbor)
            self._neighbors.append(neighbor)
            is_visited = neighbor in self._visited
            is_valid = self._grid.is_valid(neighbor)
            in_set = neighbor in self._pri_set
            if (not is_visited) and is_valid and (not in_set):
                self._push_to_queue(neighbor)
