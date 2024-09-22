#use command python -m tests.test_core
import unittest
import data as data
import src.algorithms.path_finding as path
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
        

        edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
        ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
        ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
        ("P", "T"), ("A", "D"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
        ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        graph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            graph.add_vertex(v)

        for v1, v2 in edges:
            graph.add_edge(v1, v2)
        

        outputGraph = read_graph_from_file(file_path)
        graphO = GraphOperations(graph)
        graphI = GraphOperations(outputGraph)
        self.assertEqual(graph, outputGraph)
        graph.add_vertex('Test')
        outputGraph.add_vertex('Test')
        self.assertEqual(graph, outputGraph)
        graph.add_edge('Test', 'A')
        outputGraph.add_edge('Test', 'A')
        self.assertEqual(graph, outputGraph)
        graph.remove_edge('Test', 'A')
        outputGraph.remove_edge('Test', 'A')
        self.assertEqual(graph, outputGraph)
        graph.remove_vertex('Test')
        outputGraph.remove_vertex('Test')
        self.assertEqual(graph, outputGraph)
        self.assertEqual(graphO.has_vertex('A'), graphI.has_vertex('A'))

        self.assertEqual(graphO.has_path(['A', 'B']), graphI.has_path(['A', 'B']))
        self.assertEqual(graph.add_vertex('A'), outputGraph.add_vertex('A'))
        self.assertEqual(graph.get_all_vertices(), outputGraph.get_all_vertices())
        self.assertEqual(graph.has_edge("A", "B"), outputGraph.has_edge("A", "B"))
        self.assertEqual(graph.add_edge("A", "B"), outputGraph.add_edge("A", "B"))
        self.assertEqual(graph.add_edge("A", "ABC"), outputGraph.add_edge("A", "ABC"))
        self.assertEqual(graphO.get_neighbors("A"), graphI.get_neighbors("A"))
        self.assertEqual(graph.remove_vertex('AB'), outputGraph.remove_vertex('AB'))
        self.assertEqual(graph.has_vertex('AB'), outputGraph.has_vertex('AB'))
        path0, time = graphO.get_shortest_path('A', "G")
        path1, time1 = graphI.get_shortest_path("A", "G")
        self.assertEqual(path0, path1)
        graphI.remove_edge('A', 'B')
        graphI.remove_edge('A', 'C')
        graphI.remove_edge('A', 'D')
        path0, time = graphO.get_shortest_path('A', "G")
        path1, time1 = graphI.get_shortest_path("A", "G")
        self.assertNotEqual(path0, path1)
        graphI.add_edge('A', 'B')
        graphI.add_edge('A', 'C')
        graphI.add_edge('A', 'D')
        graphO.execute_commands("data/sample_commands.txt", "data/sample_output1.txt")
        graphI.execute_commands("data/sample_commands.txt", "data/sample_output2.txt")
        self.maxDiff = None
        with open("data/sample_output1.txt", "r") as file1, open("data/sample_output2.txt", "r") as file2:
            output1 = file1.read()
            output2 = file2.read()
        self.assertNotEqual(output1, output2)

    def test_remove_edge(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        

        file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')
        

        edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
        ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
        ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
        ("P", "T"), ("A", "D"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
        ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        graph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            graph.add_vertex(v)

        for v1, v2 in edges:
            graph.add_edge(v1, v2)
        
        graph.remove_edge('A', 'B')

        edges = [
            ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
            ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
            ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
            ("P", "T"), ("A", "D"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
            ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        outGraph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            outGraph.add_vertex(v)

        for v1, v2 in edges:
            outGraph.add_edge(v1, v2)

        self.assertEqual(graph, outGraph)
    def test_remove_vertice(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        

        file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')
        

        edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
        ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
        ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
        ("P", "T"), ("A", "D"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
        ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        graph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            graph.add_vertex(v)

        for v1, v2 in edges:
            graph.add_edge(v1, v2)
        
        graph.remove_vertex('A')

        edges = [
            ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
            ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
            ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
            ("P", "T"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
            ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        outGraph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            outGraph.add_vertex(v)

        for v1, v2 in edges:
            outGraph.add_edge(v1, v2)

        self.assertEqual(graph, outGraph)

    def test_has_neighbors(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        

        file_path = os.path.join(current_dir, '..', 'data', 'sample_graph.txt')
        

        edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
        ("D", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L"), ("I", "M"),
        ("J", "N"), ("K", "O"), ("L", "P"), ("M", "Q"), ("N", "R"), ("O", "S"),
        ("P", "T"), ("A", "D"), ("B", "F"), ("C", "H"), ("D", "J"), ("E", "K"),
        ("F", "L"), ("G", "M"), ("H", "N"), ("I", "O"), ("J", "P"), ("K", "Q")
        ]


        graph = Graph()

        vertices = {v for edge in edges for v in edge}
        for v in vertices:
            graph.add_vertex(v)

        for v1, v2 in edges:
            graph.add_edge(v1, v2)

if __name__ == '__main__':
    unittest.main()


