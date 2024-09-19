from typing import Dict, Set, Optional
import threading
import time
from src.utils.logging_utils import log_operation, log_result, log_error

class Graph:
    def __init__(self):
        self._vertices: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    def add_vertex(self, v: str) -> bool:
        with self._lock:
            if v not in self._vertices:
                self._vertices[v] = set()
                log_result(f"add_vertex {v}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"add_vertex {v}", (f"{False} Vertex already in graph {time.time()}"))
            return False

    def add_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 in self._vertices and v2 in self._vertices:
                self._vertices[v1].add(v2)
                #self._vertices[v2].add(v1)  # remove first comment symbol for undirected graph
                log_result(f"add_edge {v1} -> {v2}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"add_edge {v1} -> {v2}", (f"{False} edge could not be added {time.time()}"))
            return False

    def remove_vertex(self, v: str) -> bool:
        with self._lock:
            if v in self._vertices:
                del self._vertices[v]
                for vertex in self._vertices:
                    self._vertices[vertex].discard(v)
                log_result(f"remove_vertex {v}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"remove_vertex {v}", (f"{False} vertex not found {time.time()}"))
            return False

    def remove_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 in self._vertices and v2 in self._vertices:
                self._vertices[v1].discard(v2)
                self._vertices[v2].discard(v1)
                log_result(f"remove_edge {v1} {v2}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"remove_edge {v1} {v2}", (f"{False} edge could not be removed {time.time()}"))
            return False


    def __eq__(self, other) ->bool:
        if not isinstance(other, Graph):
            return False

        if len(self._vertices) != len(other._vertices):
            return False

        for vertex in self._vertices:
            if vertex not in other._vertices:
                return False
            if self._vertices[vertex] != other._vertices[vertex]:
                return False
        return True
        


    def has_vertex(self, v: str) -> bool:
        with self._lock:
            if v in self._vertices:
                log_result(f"has_vertex {v}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"has_vertex {v}", (f"{False} vertex not found {time.time()}"))
            return False

    def has_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 in self._vertices and v2 in self._vertices[v1]:
               log_result(f"has_edge {v1} {v2}", (f"{True} completed at {time.time()}")) 
            log_result(f"has_edge {v1} {v2}", (f"{False} edge not found{time.time()}"))
            return False

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        with self._lock:
            log_result(f"get_neighbors {v}", (f"{self._vertices.get(v)} completed at {time.time()}"))
            return self._vertices.get(v)

    def get_all_vertices(self) -> Set[str]:
        with self._lock:
            log_result(f"get_all_vertices", (f"{self._vertices.keys()} completed at {time.time()}"))
            return set(self._vertices.keys())
