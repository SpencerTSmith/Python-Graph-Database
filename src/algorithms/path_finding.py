from typing import List, Optional, Dict, Set

def bfs_shortest_path(graph: Dict[str, Set[str]], start: str, end: str) -> Optional[List[str]]:
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

    return None  # No path found

def dijkstra_shortest_path(graph: Dict[str, Dict[str, float]], start: str, end: str) -> Optional[List[str]]:
    # This is a placeholder for Dijkstra's algorithm
    # maybe implement the full algorithm here
    # For now, we'll just call BFS
    return bfs_shortest_path({k: set(v.keys()) for k, v in graph.items()}, start, end)
