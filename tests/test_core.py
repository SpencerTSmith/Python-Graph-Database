#use command python -m tests.test_core
import unittest
from src.core.graph import Graph
from src.core.operations import GraphOperations
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

class TestGraphOperations(unittest.TestCase):
    def test_graph(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        

        file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')
        

        graph = read_graph_from_file(file_path)
        

        outputGraph = read_graph_from_file(file_path)

        self.assertEqual(graph, outputGraph)

if __name__ == '__main__':
    unittest.main()

