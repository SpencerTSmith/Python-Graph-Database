def load_graph_data(filename):
    graph_data = {}
    with open(filename, 'r') as file:
        for line in file:
            v1, v2 = line.strip().split()
            if v1 not in graph_data:
                graph_data[v1] = set()
            graph_data[v1].add(v2)
            if v2 not in graph_data:
                graph_data[v2] = set()
            #graph_data[v2].add(v1)  # Add reverse edge for undirected graph
    return graph_data

def partition_graph(graph_data, num_partitions):
    partitioned_data = {str(i): {} for i in range(num_partitions)}
    for i, (vertex, edges) in enumerate(graph_data.items()):
        partition = str(i % num_partitions)
        partitioned_data[partition][vertex] = edges
    return partitioned_data