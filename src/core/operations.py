from src.core.graph import Graph
from src.algorithms import path_finding
from typing import Tuple, List, Optional
import time
from enum import StrEnum


class Commands(StrEnum):
    ADD_VERT = "add-vertex"
    ADD_EDGE = "add-edge"
    REM_VERT = "remove-vertex"
    REM_EDGE = "remove-edge"
    HAS_VERT = "has-vertex"
    HAS_EDGE = "has-edge"
    GET_HOOD = "get-neighbors"
    GET_SSSP = "get-shortest-path"

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

        path = path_finding.bfs_shortest_path(self.graph._vertices, start, end)

        end_time = time.time()
        return path, end_time - start_time

    def execute_commands(self, command_file: str, output_file: str):
        with open(command_file, 'r') as commands, open(output_file, 'w') as output:
            for line in commands:
                tokens = line.strip().split(' ')

                match tokens[0]:
                    # NOTE(spencer): What do you all think? Is this readable? We may want to create a formatting function to make this prettier.
                    case Commands.ADD_VERT:
                        result = self.graph.add_vertex(tokens[1])
                        output.write(Commands.ADD_VERT + ' ' + tokens[1] + ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.ADD_EDGE:
                        result = self.graph.add_edge(tokens[1], tokens[2])
                        output.write(Commands.ADD_EDGE + ' ' + tokens[1] + ' ' + tokens[2] + ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.REM_VERT:
                        result = self.graph.remove_vertex(tokens[1])
                        output.write(Commands.REM_VERT + ' ' + tokens[1] + ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.REM_EDGE:
                        result = self.graph.remove_edge(tokens[1], tokens[2])
                        output.write(Commands.REM_EDGE + ' ' + tokens[1] + ' ' + tokens[2] + ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.HAS_VERT:
                        result = self.graph.has_vertex(tokens[1])
                        output.write(Commands.HAS_VERT + ' ' + tokens[1] +  ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.HAS_EDGE:
                        result = self.graph.has_edge(tokens[1], tokens[2])
                        output.write(Commands.HAS_EDGE + ' ' + tokens[1] + ' ' + tokens[2] + ' : ' + ( 'success' if result else 'fail' ) + '\n')
                    case Commands.GET_HOOD:
                        self.graph.get_neighbors(tokens[1])
                    case Commands.GET_SSSP:
                        self.get_shortest_path(tokens[1], tokens[2])







