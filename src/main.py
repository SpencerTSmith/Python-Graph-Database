#use command python -m src.main
from src.core.graph import Graph
from core.operations2 import GraphOperations
import os

def read_graph_from_file(filename: str) -> Graph:
    graph = Graph()
    with open(filename, 'r') as f:
        for line in f:
            v1, v2 = line.strip().split()
            graph.add_vertex(v1)
            graph.add_vertex(v2)
            graph.add_edge(v1, v2)
    return graph

def main():
    # Get the absolute path to the sample_graph.txt file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')

    # Read graph from file
    graph = read_graph_from_file(file_path)
    
    # Create GraphOperations instance
    ops = GraphOperations(graph)

    # Get start and end vertices from user
    start = input("Enter start vertex: ")
    end = input("Enter end vertex: ")

    # Find shortest path
    path, time_taken = ops.get_shortest_path(start, end)

    # Print results
    if path:
        print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
    else:
        print(f"No path found from {start} to {end}")
    print(f"Time taken: {time_taken:.6f} seconds")

if __name__ == "__main__":
    main()