import grpc
import sys
import os
import argparse
from cmd import Cmd

# Add the parent directory to the Python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generated import graph_service_pb2
from src.generated import graph_service_pb2_grpc

def handle_error(operation):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except grpc.RpcError as e:
                print(f"RPC failed: {e.code()}")
                print(f"Details: {e.details()}")
                return None
        return wrapper
    return decorator

class GraphClient:
    def __init__(self, host='localhost', port=50052):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = graph_service_pb2_grpc.GraphServiceStub(self.channel)

    @handle_error("add_vertex")
    def add_vertex(self, vertex):
        request = graph_service_pb2.AddVertexRequest(vertex=vertex)
        response = self.stub.AddVertex(request)
        return response.success, response.message

    @handle_error("remove_vertex")
    def remove_vertex(self, vertex):
        request = graph_service_pb2.VertexRequest(vertex=vertex)
        response = self.stub.RemoveVertex(request)
        return response.success, response.message
    
    @handle_error("has_vertex")
    def has_vertex(self, vertex):
        request = graph_service_pb2.VertexRequest(vertex=vertex)
        response = self.stub.HasVertex(request)
        return response.value

    @handle_error("get_all_vertices")
    def get_all_vertices(self):
        request = graph_service_pb2.EmptyRequest()
        response = self.stub.GetAllVertices(request)
        return response.vertices

    @handle_error("add_edge")
    def add_edge(self, vertex1, vertex2):
        request = graph_service_pb2.AddEdgeRequest(vertex1=vertex1, vertex2=vertex2)
        response = self.stub.AddEdge(request)
        return response.success, response.message

    @handle_error("remove_edge")
    def remove_edge(self, vertex1, vertex2):
        request = graph_service_pb2.EdgeRequest(vertex1=vertex1, vertex2=vertex2)
        response = self.stub.RemoveEdge(request)
        return response.success, response.message

    @handle_error("has_edge")
    def has_edge(self, vertex1, vertex2):
        request = graph_service_pb2.EdgeRequest(vertex1=vertex1, vertex2=vertex2)
        response = self.stub.HasEdge(request)
        return response.value

    @handle_error("get_neighbors")
    def get_neighbors(self, vertex):
        request = graph_service_pb2.VertexRequest(vertex=vertex)
        response = self.stub.GetNeighbors(request)
        return response.vertices

    @handle_error("get_shortest_path")
    def get_shortest_path(self, start, end):
        request = graph_service_pb2.PathRequest(start=start, end=end)
        response = self.stub.GetShortestPath(request)
        return response.path, response.time

    @handle_error("execute_commands")
    def execute_commands(self, commands):
        command_requests = [
            graph_service_pb2.Command(operation=cmd[0], parameters=cmd[1:])
            for cmd in commands
        ]
        request = graph_service_pb2.CommandsRequest(commands=command_requests)
        response = self.stub.ExecuteCommands(request)
        return [(result.operation, result.result) for result in response.results], response.total_time

class GraphClientCLI(Cmd):
    prompt = 'graph> '
    intro = "Welcome to the Graph Client CLI. Type 'help' to list commands."

    def __init__(self, client):
        super().__init__()
        self.client = client

    def do_add_vertex(self, arg):
        """Add a vertex: add_vertex <vertex>"""
        vertex = arg.strip()
        if vertex:
            success, message = self.client.add_vertex(vertex)
            print(f"Success: {success}, Message: {message}")
        else:
            print("Please provide a vertex.")

    def do_remove_vertex(self, arg):
        """Remove a vertex: remove_vertex <vertex>"""
        vertex = arg.strip()
        if vertex:
            success, message = self.client.remove_vertex(vertex)
            print(f"Success: {success}, Message: {message}")
        else:
            print("Please provide a vertex.")

    def do_has_vertex(self, arg):
        """Check if a vertex exists: has_vertex <vertex>"""
        vertex = arg.strip()
        if vertex:
            result = self.client.has_vertex(vertex)
            print(f"Vertex exists: {result}")
        else:
            print("Please provide a vertex.")

    def do_get_all_vertices(self, arg):
        """Get all vertices"""
        vertices = self.client.get_all_vertices()
        print("Vertices:", vertices)

    def do_add_edge(self, arg):
        """Add an edge: add_edge <vertex1> <vertex2>"""
        args = arg.split()
        if len(args) == 2:
            success, message = self.client.add_edge(args[0], args[1])
            print(f"Success: {success}, Message: {message}")
        else:
            print("Please provide two vertices.")

    def do_remove_edge(self, arg):
        """Remove an edge: remove_edge <vertex1> <vertex2>"""
        args = arg.split()
        if len(args) == 2:
            success, message = self.client.remove_edge(args[0], args[1])
            print(f"Success: {success}, Message: {message}")
        else:
            print("Please provide two vertices.")

    def do_has_edge(self, arg):
        """Check if an edge exists: has_edge <vertex1> <vertex2>"""
        args = arg.split()
        if len(args) == 2:
            result = self.client.has_edge(args[0], args[1])
            print(f"Edge exists: {result}")
        else:
            print("Please provide two vertices.")

    def do_get_neighbors(self, arg):
        """Get neighbors of a vertex: get_neighbors <vertex>"""
        vertex = arg.strip()
        if vertex:
            neighbors = self.client.get_neighbors(vertex)
            print(f"Neighbors of {vertex}:", neighbors)
        else:
            print("Please provide a vertex.")

    def do_get_shortest_path(self, arg):
        """Get shortest path between two vertices: get_shortest_path <start> <end>"""
        args = arg.split()
        if len(args) == 2:
            path, time = self.client.get_shortest_path(args[0], args[1])
            print(f"Shortest path: {path}")
            print(f"Time taken: {time:.6f} seconds")
        else:
            print("Please provide start and end vertices.")

    def do_execute_commands(self, arg):
        """Execute multiple commands: execute_commands <command1> ; <command2> ; ..."""
        commands = [cmd.strip().split() for cmd in arg.split(';') if cmd.strip()]
        if commands:
            results, total_time = self.client.execute_commands(commands)
            for operation, result in results:
                print(f"{operation}: {result}")
            print(f"Total time: {total_time:.6f} seconds")
        else:
            print("Please provide commands separated by semicolons.")

    def do_quit(self, arg):
        """Quit the CLI"""
        print("Goodbye!")
        return True

    def do_exit(self, arg):
        """Exit the CLI"""
        return self.do_quit(arg)

def main(host='localhost', port=50052):
    client = GraphClient(host=host, port=port)
    cli = GraphClientCLI(client)
    cli.cmdloop()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Graph Client")
    parser.add_argument("--host", default="localhost", help="Broker host")
    parser.add_argument("--port", type=int, default=50052, help="Broker port")
    args = parser.parse_args()
    main(host=args.host, port=args.port)