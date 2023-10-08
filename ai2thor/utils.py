from collections import deque
from typing import Tuple

def get_neighbors(positions_tuple: Tuple[Tuple[float, float, float]]):
    grid_size = 0.25
    neighbors = dict()
    for position in positions_tuple:
        position_neighbors = set()
        for p in positions_tuple:
            if position != p and (
                (
                    abs(position[0] - p[0]) < 1.5 * grid_size
                    and abs(position[2] - p[2]) < 0.5 * grid_size
                )
                or (
                    abs(position[0] - p[0]) < 0.5 * grid_size
                    and abs(position[2] - p[2]) < 1.5 * grid_size
                )
            ):
                position_neighbors.add(p)
        neighbors[position] = position_neighbors
    
    return neighbors

def closest_grid_point(world_point: Tuple[float, float, float], positions_tuple: Tuple[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Return the grid point that is closest to a world coordinate.

    Expects world_point=(x_pos, y_pos, z_pos). Note y_pos is ignored in the calculation.
    """
    def distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]):
        # ignore the y_pos
        return ((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5

    min_dist = float("inf")
    closest_point = None
    assert len(positions_tuple) > 0
    for p in positions_tuple:
        dist = distance(p, world_point)
        if dist < min_dist:
            min_dist = dist
            closest_point = p
    return closest_point


def shortest_path(start: Tuple[float, float, float], end: Tuple[float, float, float], neighbors: dict, positions_tuple: Tuple[Tuple[float, float, float]]):
    """Expects the start=(x_pos, y_pos, z_pos) and end=(x_pos, y_pos, z_pos).

    Note y_pos is ignored in the calculation.
    """
    start = closest_grid_point(start, positions_tuple)
    end = closest_grid_point(end, positions_tuple)
    print(start, end)

    if start == end:
        return [start]

    q = deque()
    q.append([start])

    visited = set()

    while q:
        path = q.popleft()
        pos = path[-1]

        if pos in visited:
            continue

        visited.add(pos)
        for neighbor in neighbors[pos]:
            if neighbor == end:
                return path + [neighbor]
            q.append(path + [neighbor])

    raise Exception("Invalid state. Must be a bug!")