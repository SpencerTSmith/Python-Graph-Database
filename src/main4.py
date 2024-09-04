#use command python -m src.main4
from src.core.graph import Graph
from src.core.operations import GraphOperations
from typing import Tuple
import os
import time
import threading
# import networkx as nx
# import matplotlib.pyplot as plt

# TODO(spencer): Seems to be an issue because the portioning is done by character and not lines... leads to some missed edges and an error
def read_file_portion(graph: Graph, filename: str, start: int, end: int):
    with open(filename, 'r') as file:
        file.seek(start)
        
        # If we're not at the beginning of the file, discard the first (potentially partial) line
        if start > 0:
            file.readline()
        
        while file.tell() < end:
            line = file.readline().strip()
            if not line:
                continue  # Skip empty lines
            
            parts = line.split()
            if len(parts) != 2:
                continue  # Skip lines that don't have exactly two vertices
            
            v1, v2 = parts
            graph.add_vertex(v1)
            graph.add_vertex(v2)
            graph.add_edge(v1, v2)

def read_graph_from_file_t(filename: str) -> Tuple[Graph, float]:
    start_time = time.time()

    num_threads = 4

    graph = Graph()
    # Split the graph file into portions and give to threads
    graph_file_size = os.path.getsize(filename)
    file_portion_size = graph_file_size // num_threads

    threads = []
    for i in range(num_threads):
        portion_start = i * file_portion_size
        portion_end = ((i + 1) * file_portion_size) if i < num_threads - 1 else graph_file_size
        thread = threading.Thread(target=read_file_portion, args=(graph, filename, portion_start, portion_end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    stop_time = time.time()
    return graph, stop_time - start_time

def read_worker(graph: Graph, line: str):
    v1, v2 = line.strip().split()
    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_edge(v1, v2)

def read_graph_from_file(filename: str) -> Tuple[Graph, float]:
    start_time = time.time()

    graph = Graph()
    with open(filename, 'r') as f:
        for line in f:
            v1, v2 = line.strip().split()
            graph.add_vertex(v1)
            graph.add_vertex(v2)
            graph.add_edge(v1, v2)
    stop_time = time.time()
    return graph, stop_time - start_time

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(current_dir, '..', 'data', 'large_graph.txt')
    command_path = os.path.join(current_dir, '..', 'data', 'sample_commands.txt')
    output_path = os.path.join(current_dir, '..', 'data', 'sample_output.txt')

    graph, create_time = read_graph_from_file_t(graph_path)

    ops = GraphOperations(graph)

    ops.execute_commands(command_path, output_path)
    print(f'Created graph in : {create_time:.6f}\n')

if __name__ == "__main__":
    main()
