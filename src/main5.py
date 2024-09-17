import os
import time
import multiprocessing as mp
from multiprocessing import Manager
from src.core.graph import Graph
from src.core.operations import GraphOperations
from typing import Tuple

def read_file_portion(shared_dict, lock, filename, start, end):
    local_dict = {}
    with open(filename, 'r') as file:
        file.seek(start)
        if start > 0:
            file.readline()
        while file.tell() < end:
            line = file.readline().strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            v1, v2 = parts
            if v1 not in local_dict:
                local_dict[v1] = set()
            if v2 not in local_dict:
                local_dict[v2] = set()
            local_dict[v1].add(v2)
    
    with lock:
        for v, edges in local_dict.items():
            if v not in shared_dict:
                shared_dict[v] = edges
            else:
                shared_dict[v].update(edges)

def read_graph_from_file_mp(filename: str) -> Tuple[Graph, float]:
    start_time = time.time()

    num_processes = mp.cpu_count()
    manager = Manager()
    shared_dict = manager.dict()
    lock = manager.Lock()

    graph_file_size = os.path.getsize(filename)
    file_portion_size = graph_file_size // num_processes

    with mp.Pool(num_processes) as pool:
        args = [(shared_dict, lock, filename, i * file_portion_size, 
                 (i + 1) * file_portion_size if i < num_processes - 1 else graph_file_size) 
                for i in range(num_processes)]
        pool.starmap(read_file_portion, args)

    graph = Graph(shared_dict)
    stop_time = time.time()
    return graph, stop_time - start_time

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(current_dir, '..', 'data', '1Large_graph.txt')
    command_path = os.path.join(current_dir, '..', 'data', 'sample_commands.txt')
    output_path = os.path.join(current_dir, '..', 'data', 'sample_output.txt')

    graph, create_time = read_graph_from_file_mp(graph_path)

    ops = GraphOperations(graph)

    ops.execute_commands(command_path, output_path)
    print(f'Created graph in : {create_time:.6f}\n')

if __name__ == "__main__":
    mp.freeze_support()  # Needed for Windows
    main()