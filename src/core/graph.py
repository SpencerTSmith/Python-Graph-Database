from typing import Dict, Set, Optional
import threading

class Graph:
    def __init__(self):
        self._vertices: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    def add_vertex(self, v: str) -> bool:
        with self._lock:
            if v not in self._vertices:
                self._vertices[v] = set()
                return True
            return False

    def add_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 in self._vertices and v2 in self._vertices:
                self._vertices[v1].add(v2)
                #self._vertices[v2].add(v1)  # remove first comment symbol for undirected graph
                return True
            return False

    def remove_vertex(self, v: str) -> bool:
        with self._lock:
            if v in self._vertices:
                del self._vertices[v]
                for vertex in self._vertices:
                    self._vertices[vertex].discard(v)
                return True
            return False

    def remove_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 in self._vertices and v2 in self._vertices:
                self._vertices[v1].discard(v2)
                self._vertices[v2].discard(v1)
                return True
            return False


    def __eq__(self, other) ->bool:
        if not isinstance(other, Graph):
            return False

        if len(self._vertices) != len(other._vertices):
            return False

        for vertex in self._vertices.items():
            if vertex not in other._vertices:
                return False
            if self._vertices[vertex] != other._vertices[vertex]:
                return False
        return True
        


    def has_vertex(self, v: str) -> bool:
        with self._lock:
            return v in self._vertices

    def has_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            return v1 in self._vertices and v2 in self._vertices[v1]

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        with self._lock:
            return self._vertices.get(v)

    def get_all_vertices(self) -> Set[str]:
        with self._lock:
            return set(self._vertices.keys())
