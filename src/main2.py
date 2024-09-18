#use command python -m src.main2
from src.core.graph import Graph
from core.operations2 import GraphOperations
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

def visualize_graph(graph: Graph, path: list = []):
    G = nx.Graph()
    for vertex in graph.get_all_vertices():
        G.add_node(vertex)
        neighbors = graph.get_neighbors(vertex)
        if neighbors:
            for neighbor in neighbors:
                G.add_edge(vertex, neighbor)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r', node_size=500)

    plt.title("Graph Visualization")
    plt.axis('off')
    plt.show()

def main():
    # Get the absolute path to the sample_graph.txt file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'sample_graph2.txt')

    # Read graph from file
    graph = read_graph_from_file(file_path)
    
    # Create GraphOperations instance
    ops = GraphOperations(graph)

    # Visualize the entire graph
    visualize_graph(graph)

    # Get start and end vertices from user
    start = input("Enter start vertex: ")
    end = input("Enter end vertex: ")

    # Find shortest path
    path, time_taken = ops.get_shortest_path(start, end)

    # Print results
    if path:
        print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
        # Visualize the graph with the shortest path highlighted
        visualize_graph(graph, path)
    else:
        print(f"No path found from {start} to {end}")
    print(f"Time taken: {time_taken:.6f} seconds")

if __name__ == "__main__":
    main()
