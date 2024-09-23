import logging
from typing import Dict, Set, Optional
from multiprocessing import Lock

# Set up logging:
# %(asctime)s: The time when the log message was created
# %(name)s: The name of the logger
# %(levelname)s: The level of the log message (INFO, WARNING, etc.)
# %(message)s: The actual log message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Graph:
    def __init__(self, shared_dict=None):
        if shared_dict is None:
            self._vertices = {}
        else:
            self._vertices = shared_dict
        self._external_vertices = set()
        self._lock = Lock()

    def add_external_vertex(self, vertex):
        if not hasattr(self, '_external_vertices'): # checking if the Graph instance (self) has an attribute named '_external_vertices'
            self._external_vertices = set()
        self._external_vertices.add(vertex)
        self._vertices[vertex] = set()

    def add_edge(self, v1: str, v2: str) -> bool:
        with self._lock:
            if v1 not in self._vertices:
                self._external_vertices.add(v1)
                self._vertices[v1] = set()
            if v2 not in self._vertices:
                self._external_vertices.add(v2)
                self._vertices[v2] = set()
            self._vertices[v1].add(v2)
            # Comment out or remove this line to make the graph directional
            # self._vertices[v2].add(v1)
            return True

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        with self._lock:
            neighbors = self._vertices.get(v, set()).copy()
            if v in self._external_vertices:
                neighbors.add("EXTERNAL")
            return neighbors

    def add_vertex(self, v: str) -> bool:
        with self._lock:
            if v not in self._vertices:
                self._vertices[v] = set()
                logger.debug(f"Added vertex {v}")
                return True
            logger.debug(f"Vertex {v} already exists")
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
                # Comment out or remove this line to make the graph directional
                # self._vertices[v2].discard(v1)
                return True
            return False

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
            all_vertices = set(self._vertices.keys()) | self._external_vertices #union of _vertices and _external_vertices
            logger.debug(f"Total vertices: {len(all_vertices)}")
            return all_vertices