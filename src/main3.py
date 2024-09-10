#use command python -m src.main3
from src.core.graph import Graph
from src.core.operations2 import GraphOperations
import os
import networkx as nx
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from src.utils.logging_utils import log_operation, log_result, log_error
import threading
import time

def read_graph_from_file(filename: str, num_threads: int = 4) -> Graph:
    graph = Graph()
    ops = GraphOperations(graph)
    log_operation("read_graph_from_file", filename)
    
    lock = threading.Lock()
    
    def process_line(line):
        try:
            v1, v2 = line.strip().split()
            with lock:
                ops.add_vertex(v1)
                ops.add_vertex(v2)
                ops.add_edge(v1, v2)
        except ValueError:
            log_error("read_graph_from_file", f"Invalid line format: {line.strip()}")
        except Exception as e:
            log_error("read_graph_from_file", f"Error processing line: {str(e)}")

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(process_line, lines)
        
        log_result("read_graph_from_file", f"Graph created with {len(ops.get_all_vertices())} vertices")
        return graph
    except Exception as e:
        log_error("read_graph_from_file", f"Error reading file: {str(e)}")
        raise

def visualize_graph(graph: Graph, path: list = None):
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

def print_menu():
    print("\nAvailable commands:")
    print("1. add_vertex <vertex>")
    print("2. add_edge <vertex1> <vertex2>")
    print("3. remove_vertex <vertex>")
    print("4. remove_edge <vertex1> <vertex2>")
    print("5. has_vertex <vertex>")
    print("6. has_edge <vertex1> <vertex2>")
    print("7. get_neighbors <vertex>")
    print("8. get_all_vertices")
    print("9. get_shortest_path <start> <end>")
    print("10. visualize")
    print("11. quit")

def execute_command(ops: GraphOperations, command: str):
    parts = command.split()
    if not parts:
        print("Invalid command")
        return

    cmd = parts[0].lower()
    args = parts[1:]

    try:
        if cmd == "add_vertex" and len(args) == 1:
            result = ops.parallel_operation(ops.add_vertex, args[0])
            print(f"Add vertex result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "add_edge" and len(args) == 2:
            result = ops.parallel_operation(ops.add_edge, args[0], args[1])
            print(f"Add edge result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "remove_vertex" and len(args) == 1:
            result = ops.parallel_operation(ops.remove_vertex, args[0])
            print(f"Remove vertex result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "remove_edge" and len(args) == 2:
            result = ops.parallel_operation(ops.remove_edge, args[0], args[1])
            print(f"Remove edge result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "has_vertex" and len(args) == 1:
            result = ops.parallel_operation(ops.has_vertex, args[0])
            print(f"Has vertex result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "has_edge" and len(args) == 2:
            result = ops.parallel_operation(ops.has_edge, args[0], args[1])
            print(f"Has edge result: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "get_neighbors" and len(args) == 1:
            result = ops.parallel_operation(ops.get_neighbors, args[0])
            print(f"Neighbors: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "get_all_vertices" and len(args) == 0:
            result = ops.parallel_operation(ops.get_all_vertices)
            print(f"All vertices: {result}")
            print(f"Unix completion time: {time.time()}")
        elif cmd == "get_shortest_path" and len(args) == 2:
            path, time_taken = ops.get_shortest_path(args[0], args[1])
            if path:
                print(f"Shortest path from {args[0]} to {args[1]}: {' -> '.join(path)}")
                print(f"Time taken: {time_taken:.6f} seconds")
                print(f"Unix completion time: {time.time()}")
            else:
                print(f"No path found from {args[0]} to {args[1]}")
                print(f"Unix completion time: {time.time()}")
        elif cmd == "visualize" and len(args) == 0:
            visualize_graph(ops.graph)
        else:
            print("Invalid command or wrong number of arguments")
            log_error("User input invalid command: ", cmd)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        log_error("Error occured when inputting command: ", cmd)

def main():
    # Get the absolute path to the sample_graph.txt file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')

    # Read graph from file
    graph = read_graph_from_file(file_path, num_threads=8)
    
    # Create GraphOperations instance
    ops = GraphOperations(graph)

    # Initial graph visualization
    print("Initial graph:")
    visualize_graph(graph)

    # Interactive command loop
    while True:
        print_menu()
        command = input("Enter a command (or 'quit' to exit): ")
        
        if command.lower() == 'quit':
            break
        
        execute_command(ops, command)

    print("Thank you for using the Graph Operations program!")

if __name__ == "__main__":
    main()
    