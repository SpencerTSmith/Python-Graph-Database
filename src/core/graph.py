import logging
from typing import Dict, Set, Optional
import time
from src.utils.logging_utils import log_operation, log_result, log_error
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
            if v1 in self._vertices and v2 in self._vertices:
                self._vertices[v1].add(v2)
                #self._vertices[v2].add(v1)  # remove first comment symbol for undirected graph
                log_result(f"add_edge {v1} -> {v2}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"add_edge {v1} -> {v2}", (f"{False} edge could not be added {time.time()}"))
            return False

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        with self._lock:
            neighbors = self._vertices.get(v, set()).copy()
            if v in self._external_vertices:
                neighbors.add("EXTERNAL")
            log_result(f"get_neighbors {v}", (f"{neighbors} completed at {time.time()}"))
            return neighbors

    def add_vertex(self, v: str) -> bool:
        with self._lock:
            if v not in self._vertices:
                self._vertices[v] = set()
                log_result(f"add_vertex {v}", (f"{True} completed at {time.time()}"))
                return True
            log_result(f"add_vertex {v}", (f"{False} Vertex already in graph {time.time()}"))
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
                # Comment out or remove this line to make the graph directional
                # self._vertices[v2].discard(v1)
                return True
            log_result(f"remove_edge {v1} {v2}", (f"{False} edge could not be removed {time.time()}"))
            return False

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

    def get_all_vertices(self) -> Set[str]:
        with self._lock:
            log_result(f"get_all_vertices", (f"{self._vertices.keys()} completed at {time.time()}"))
            all_vertices = set(self._vertices.keys()) | self._external_vertices #union of _vertices and _external_vertices
            logger.debug(f"Total vertices: {len(all_vertices)}")
            return all_vertices
