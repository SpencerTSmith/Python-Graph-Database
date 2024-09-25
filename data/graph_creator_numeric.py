import random

def generate_large_graph_file(filename, num_vertices, num_edges):
    with open(filename, 'w') as f:
        edges_added = set()
        
        # Ensure the graph is connected
        for i in range(1, num_vertices):
            v1 = i - 1
            v2 = i
            f.write(f"{v1} {v2}\n")
            edges_added.add((v1, v2))
        
        # Add remaining random edges
        while len(edges_added) < num_edges:
            v1 = random.randint(0, num_vertices - 1)
            v2 = random.randint(0, num_vertices - 1)
            if v1 != v2 and (v1, v2) not in edges_added and (v2, v1) not in edges_added:
                f.write(f"{v1} {v2}\n")
                edges_added.add((v1, v2))

    print(f"Graph file '{filename}' created with {num_vertices} vertices and {num_edges} edges.")

# Usage
generate_large_graph_file("num_large_graph.txt", 1000, 100000)