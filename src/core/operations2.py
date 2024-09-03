import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Set, Tuple
from src.core.graph import Graph
from src.algorithms import path_finding
from src.utils.logging_utils import log_operation, log_result, log_error
import time

class GraphOperations:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=4)  # Adjust the number of workers as needed

    def add_vertex(self, v: str) -> bool:
        log_operation("add_vertex", v)
        with self.lock:
            result = self.graph.add_vertex(v)
        log_result("add_vertex", result)
        return result

    def add_edge(self, v1: str, v2: str) -> bool:
        log_operation("add_edge", v1, v2)
        with self.lock:
            result = self.graph.add_edge(v1, v2)
        log_result("add_edge", result)
        return result

    def remove_vertex(self, v: str) -> bool:
        log_operation("remove_vertex", v)
        with self.lock:
            result = self.graph.remove_vertex(v)
        log_result("remove_vertex", result)
        return result

    def remove_edge(self, v1: str, v2: str) -> bool:
        log_operation("remove_edge", v1, v2)
        with self.lock:
            result = self.graph.remove_edge(v1, v2)
        log_result("remove_edge", result)
        return result

    def has_vertex(self, v: str) -> bool:
        log_operation("has_vertex", v)
        with self.lock:
            result = self.graph.has_vertex(v)
        log_result("has_vertex", result)
        return result

    def has_edge(self, v1: str, v2: str) -> bool:
        log_operation("has_edge", v1, v2)
        with self.lock:
            result = self.graph.has_edge(v1, v2)
        log_result("has_edge", result)
        return result

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        log_operation("get_neighbors", v)
        with self.lock:
            result = self.graph.get_neighbors(v)
        log_result("get_neighbors", result)
        return result

    def get_all_vertices(self) -> Set[str]:
        log_operation("get_all_vertices")
        with self.lock:
            result = self.graph.get_all_vertices()
        log_result("get_all_vertices", result)
        return result

    def get_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        log_operation("get_shortest_path", start, end)
        start_time = time.time()
        
        def path_finder():
            graph_dict = {v: self.graph.get_neighbors(v) for v in self.graph.get_all_vertices()}
            return path_finding.bfs_shortest_path(graph_dict, start, end)

        future = self.executor.submit(path_finder)
        path = future.result()
        
        end_time = time.time()
        time_taken = end_time - start_time
        log_result("get_shortest_path", (path, time_taken))
        return path, time_taken

    def parallel_operation(self, operation, *args):
        """Execute an operation in parallel"""
        future = self.executor.submit(operation, *args)
        return future.result()

    def __del__(self):
        self.executor.shutdown()