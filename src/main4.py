#use command python -m src.main4
from src.core.graph import Graph
from src.core.operations import GraphOperations
import os
import networkx as nx
import matplotlib.pyplot as plt

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')
    command_path = os.path.join(current_dir, '..', 'data', 'sample_commands.txt')
    output_path = os.path.join(current_dir, '..', 'data', 'sample_output.txt')

    graph = read_graph_from_file(graph_path)

    ops = GraphOperations(graph)

    ops.execute_commands(command_path, output_path)








if __name__ == "__main__":
    main()
