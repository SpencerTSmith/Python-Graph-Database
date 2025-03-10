from src.core.graph import Graph
from src.algorithms import path_finding

from src.utils.time_tracking import TimeTracking
from src.utils.logging_utils import log_operation, log_result, log_error

from typing import Tuple, List, Optional, Set
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
    HAS_PATH = "has-path"
    GET_HOOD = "get-neighborhood"
    GET_SSSP = "get-shortest-path"
    GET_VRTS = "get-all-vertices"
    GET_EDGS = "get-all-edges"

class GraphOperations:
    def __init__(self, graph: Graph):
        self._graph = graph
        self.lamport_clock=TimeTracking()

    def add_vertex(self, v: str) -> bool: 
        #log_result(f"add_vertex {v}", (f"{result} completed at {time.time()}"))
        start_time=time.time()
        result = self._graph.add_vertex(v)
        
        end_time= time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("add vertex", start_time,end_time,lamport_time)
        return result

    def add_external_vertex(self, vertex):
        self._graph._external_vertices.add(vertex)

    def add_edge(self, v1: str, v2: str) -> bool:
        #log_result(f"add_edge {v1} -> {v2}", (f"{result} completed at {time.time()}"))
        start_time=time.time()
        result = self._graph.add_edge(v1, v2)
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("add edge", start_time,end_time,lamport_time)
        return result

    def remove_vertex(self, v: str) -> bool:
        #log_result(f"remove_vertex {v}", (f"{result} completed at {time.time()}"))
        
        start_time=time.time()
        result = self._graph.remove_vertex(v)
        
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("remove vertex", start_time,end_time,lamport_time)
        return result

    def remove_edge(self, v1: str, v2: str) -> bool:
        #log_result(f"remove_edge {v1} {v2}", (f"{result} completed at {time.time()}"))
        start_time=time.time()
        
        result = self._graph.remove_edge(v1, v2)
        
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("remove edge", start_time,end_time,lamport_time)
        return result

    def has_vertex(self, v: str) -> bool:
        #log_result(f"has_vertex {v}", (f"{result} completed at {time.time()}"))
        start_time=time.time()
        
        result = self._graph.has_vertex(v)
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("has vertex", start_time,end_time,lamport_time)
        return result

    def has_edge(self, v1: str, v2: str) -> bool:
        #log_result(f"has_edge {v1} {v2}", (f"{result} completed at {time.time()}"))
        start_time=time.time()
        
        result = self._graph.has_edge(v1, v2)
        
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("has edge", start_time,end_time,lamport_time)
        return result

    def has_path(self, vertices: List[str]) -> bool: 
        log_operation("has path", vertices)
        for i in range(len(vertices) - 1):
            if not self.has_edge(vertices[i], vertices[i + 1]):
                result = False
                log_result(f"has_path {vertices}", (f"{result} completed at {time.time()}"))
                return result
        result = True
        log_result(f"has_path {vertices}", (f"{result} completed at {time.time()}"))
        return result

    def get_neighbors(self, v: str) -> Optional[Set[str]]:
        start_time=time.time()
        
        result = self._graph.get_neighbors(v)
        #log_result(f"get_neighbors {v}", (f"{neighbors} completed at {time.time()}"))
        
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("get_neighbors", start_time,end_time,lamport_time)

        return result if result is not None else None

    def get_all_vertices(self) -> List[str]:
        start_time=time.time()
        result = list(self._graph.get_all_vertices())
        
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times(" get all vertices",start_time,end_time,lamport_time)

        return result

    def get_all_edges(self) -> List[Tuple[str, str]]:
        start_time=time.time()
        log_operation("get_all_edges")
        all = []
        for vert, edges in list(self._graph._vertices.items()):
            for edge in edges:
                all.append((vert, edge))
        log_result(f"get_all_edges", (f"{all} completed at {time.time()}"))
        end_time=time.time()
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times(" get all vertices",start_time,end_time,lamport_time)
        return all

    def get_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:

        log_operation("get_shortest_path", start, end)
        start_time = time.time()
        #graph_dict = {v: self._graph.get_neighbors(v) for v in self._graph.get_all_vertices()}
        #path= path_finding.bfs_shortest_path(graph_dict, start, end)

        #future = self.executor.submit(path_finder)
        #path = future.result()
        
        path = path_finding.parallel_shortest_path(self._graph._vertices, start, end)

        end_time = time.time()
        log_result(f"get_shortest_path {start} {end}", (f"{path} in {end_time - start_time: .6f} seconds completed at ", time.time()))
        
        lamport_time=self.lamport_clock.get_lamport_times()
        self.lamport_clock._log_times("get shortest path", start_time,end_time,lamport_time)
        return path, end_time -start_time

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
                        #log_result(f"add_vertex {tokens[1]}", (f"{result} completed at {time.time()}"))
                    case Commands.ADD_EDGE:
                        result = self.add_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.ADD_EDGE} {tokens[1]} {tokens[2]} : {'success' if result else 'fail'}\n")
                        #log_result(f"add_edge {tokens[1]} {tokens[2]}", (f"{result} completed at {time.time()}"))
                    case Commands.REM_VERT:
                        result = self.remove_vertex(tokens[1])
                        output.write(f"{Commands.REM_VERT} {tokens[1]} : {'success' if result else 'fail'}\n")
                        #log_result(f"remove_vertex {tokens[1]}", (f"{result} completed at {time.time()}"))
                    case Commands.REM_EDGE:
                        result = self.remove_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.REM_EDGE} {tokens[1]} {tokens[2]} : {'success' if result else 'fail'}\n")
                        #log_result(f"remove_edge {tokens[1]} {tokens[2]}", (f"{result} completed at {time.time()}"))
                    case Commands.HAS_VERT:
                        result = self.has_vertex(tokens[1])
                        output.write(f"{Commands.HAS_VERT} {tokens[1]} : {str(result)}\n")
                        #log_result(f"has_vertex {tokens[1]}", (f"{result} completed at {time.time()}"))
                    case Commands.HAS_EDGE:
                        result = self.has_edge(tokens[1], tokens[2])
                        output.write(f"{Commands.HAS_EDGE} {tokens[1]} {tokens[2]} : {str(result)}\n")
                        #log_result(f"has_edge {tokens[1]} {tokens[2]}", (f"{result} completed at {time.time()}"))
                    case Commands.HAS_PATH:
                        result = self.has_path(tokens[1:])
                        output.write(f"{Commands.HAS_PATH} {tokens[1:]} : {str(result)}\n")
                        #log_result(f"has_path {tokens[1:]}", (f"{result} completed at {time.time()}"))
                    case Commands.GET_HOOD:
                        neighborhood = self.get_neighbors(tokens[1])
                        output.write(f"{Commands.GET_HOOD} {tokens[1]} : {str(neighborhood)}\n")
                        #log_result(f"get_neighbors {tokens[1]}", (f"{result} completed at {time.time()}"))
                    case Commands.GET_SSSP:
                        path, sp_time = self.get_shortest_path(tokens[1], tokens[2])
                        output.write(f"{Commands.GET_SSSP} {tokens[1]} {tokens[2]} : {str(path)} in {sp_time:.6f} seconds\n")
                        #log_result(f"get_shortest_path {tokens[1]} {tokens[2]}", (f"{result} in {sp_time: .6f} seconds completed at ", time.time()))
                    case Commands.GET_VRTS:
                        verts = self.get_all_vertices()
                        output.write(f"{Commands.GET_VRTS} : {verts}\n")
                        #log_result(f"get_all_vertices", (f"{result} completed at {time.time()}"))
                    case Commands.GET_EDGS:
                        edges = self.get_all_edges()
                        output.write(f"{Commands.GET_EDGS} : {edges}\n")
                        #log_result(f"get_all_edges", (f"{result} completed at {time.time()}"))

            output.write("\nGraph after commands:\n")
            pprint(self._graph._vertices, stream=output)
            stop_time = time.time()
            output.write(f"Executed all commands in: {stop_time - start_time:.6f}\n")
            log_result("all commands executed", f"executed in {stop_time -start_time:.6f} at {time.time()}")
