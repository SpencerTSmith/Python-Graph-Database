from src.core.graph import Graph
from src.algorithms import path_finding
from typing import Tuple, List, Optional
import time
from enum import StrEnum
from pprint import pprint

class Commands(StrEnum):
    ADD_VERT = "add-vertex"
    ADD_EDGE = "add-edge"
    REM_VERT = "remove-vertex"
    REM_EDGE = "remove-edge"
    HAS_VERT = "has-vertex"
    HAS_EDGE = "has-edge"
    GET_HOOD = "get-neighborhood"
    GET_SSSP = "get-shortest-path"

class GraphOperations:
    def __init__(self, graph: Graph):
        self._graph = graph

    def add_vertex(self, v: str) -> bool:
        return self._graph.add_vertex(v)

    def add_edge(self, v1: str, v2: str) -> bool:
        return self._graph.add_edge(v1, v2)

    def remove_vertex(self, v: str) -> bool:
        return self._graph.remove_vertex(v)

    def remove_edge(self, v1: str, v2: str) -> bool:
        return self._graph.remove_edge(v1, v2)

    def has_vertex(self, v: str) -> bool:
        return self._graph.has_vertex(v)

    def has_edge(self, v1: str, v2: str) -> bool:
        return self._graph.has_edge(v1, v2)

    def get_neighbors(self, v: str) -> Optional[List[str]]:
        neighbors = self._graph.get_neighbors(v)
        return list(neighbors) if neighbors is not None else None

    def get_all_vertices(self) -> List[str]:
        return list(self._graph.get_all_vertices())

    def get_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        start_time = time.time()

        path = path_finding.parallel_shortest_path(self._graph._vertices, start, end)

        end_time = time.time()
        return path, end_time - start_time

    # Optional: Add a method for regular BFS for comparison
    def get_shortest_path_bfs(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        start_time = time.time()

        path = path_finding.bfs_shortest_path(self._graph._vertices, start, end)

        end_time = time.time()
        return path, end_time - start_time
    
    # TODO(spencer): Needs nicer error checking and handling probably
    def execute_commands(self, command_file: str, output_file: str):
        start_time = time.time()
        with open(command_file, 'r') as commands, open(output_file, 'w') as output:
            output.write('Graph before commands:\n')
            # pretty print looks better than str()
            pprint(self._graph._vertices, stream=output)

            for line in commands:
                tokens = line.strip().split(' ')

                match tokens[0]:
                    case Commands.ADD_VERT:
                        result = self.add_vertex(tokens[1])
                        output.write(f"{Commands.ADD_VERT} {tokens[1]} : {'success' if result else 'fail'}\n")
                    case Commands.ADD_EDGE:
                        result = self.add_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.ADD_EDGE} {tokens[1]} {tokens[2]} : {'success' if result else 'fail'}\n")
                    case Commands.REM_VERT:
                        result = self.remove_vertex(tokens[1])
                        output.write(f"{Commands.REM_VERT} {tokens[1]} : {'success' if result else 'fail'}\n")
                    case Commands.REM_EDGE:
                        result = self.remove_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.REM_EDGE} {tokens[1]} {tokens[2]} : {'success' if result else 'fail'}\n")
                    case Commands.HAS_VERT:
                        result = self.has_vertex(tokens[1])
                        output.write(f"{Commands.HAS_VERT} {tokens[1]} : {str(result)}\n")
                    case Commands.HAS_EDGE:
                        result = self.has_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.HAS_EDGE} {tokens[1]} {tokens[2]} : {str(result)}\n")
                    case Commands.GET_HOOD:
                        neighborhood = self.get_neighbors(tokens[1])
                        output.write(f"{Commands.GET_HOOD} {tokens[1]} : {str(neighborhood)}\n")
                    case Commands.GET_SSSP:
                        path, sp_time = self.get_shortest_path(tokens[1], tokens[2])
                        output.write(f"{Commands.GET_SSSP} {tokens[1]} {tokens[2]} : {str(path)} in {sp_time:.6f} seconds\n")

            output.write("\nGraph after commands:\n")
            pprint(self._graph._vertices, stream=output)
            stop_time = time.time()
            output.write(f"Executed all commands in: {stop_time - start_time:.6f}\n")