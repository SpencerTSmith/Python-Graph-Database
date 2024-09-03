import random
import string

def generate_large_graph_file(filename, num_vertices, num_edges):
    def generate_vertex_name(index):
        # Generate vertex names like A, B, C, ..., Z, AA, AB, AC, ...
        if index < 26:
            return chr(65 + index)
        else:
            return chr(65 + (index // 26) - 1) + chr(65 + (index % 26))

    vertices = [generate_vertex_name(i) for i in range(num_vertices)]
    
    with open(filename, 'w') as f:
        edges_added = set()
        
        # Ensure the graph is connected
        for i in range(1, num_vertices):
            v1 = vertices[i-1]
            v2 = vertices[i]
            f.write(f"{v1} {v2}\n")
            edges_added.add((v1, v2))
        
        # Add remaining random edges
        while len(edges_added) < num_edges:
            v1 = random.choice(vertices)
            v2 = random.choice(vertices)
            if v1 != v2 and (v1, v2) not in edges_added and (v2, v1) not in edges_added:
                f.write(f"{v1} {v2}\n")
                edges_added.add((v1, v2))

    print(f"Graph file '{filename}' created with {num_vertices} vertices and {num_edges} edges.")

# Usage
generate_large_graph_file("large_graph.txt", 1000, 100000)