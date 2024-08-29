from src.core.graph import Graph
from src.algorithms import path_finding
from typing import Tuple, List, Optional
import time

class GraphOperations:
    def __init__(self, graph: Graph):
        self.graph = graph

    def add_vertex(self, v: str) -> bool:
        return self.graph.add_vertex(v)

    def add_edge(self, v1: str, v2: str) -> bool:
        return self.graph.add_edge(v1, v2)

    def remove_vertex(self, v: str) -> bool:
        return self.graph.remove_vertex(v)

    def remove_edge(self, v1: str, v2: str) -> bool:
        return self.graph.remove_edge(v1, v2)

    def has_vertex(self, v: str) -> bool:
        return self.graph.has_vertex(v)

    def has_edge(self, v1: str, v2: str) -> bool:
        return self.graph.has_edge(v1, v2)

    def get_neighbors(self, v: str) -> Optional[List[str]]:
        neighbors = self.graph.get_neighbors(v)
        return list(neighbors) if neighbors is not None else None

    def get_all_vertices(self) -> List[str]:
        return list(self.graph.get_all_vertices())

    def get_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        start_time = time.time()
        # Convert our graph structure to the format expected by the path_finding module
        graph_dict = {v: self.graph.get_neighbors(v) for v in self.graph.get_all_vertices()}
        path = path_finding.bfs_shortest_path(graph_dict, start, end)
        end_time = time.time()
        return path, end_time - start_time