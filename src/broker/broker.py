import grpc
from concurrent import futures
import time
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generated import graph_service_pb2
from src.generated import graph_service_pb2_grpc
from src.algorithms import path_finding

class BrokerServicer(graph_service_pb2_grpc.GraphServiceServicer):
    def __init__(self, server_address):
        self.server_channel = grpc.insecure_channel(server_address)
        self.server_stub = graph_service_pb2_grpc.GraphServiceStub(self.server_channel)
        logger.info(f"Broker connected to server at {server_address}")

    def GetShortestPath(self, request, context):
        logger.info(f"Received request for shortest path from {request.start} to {request.end}")
        
        # Get all vertices from the server
        vertices_response = self.server_stub.GetAllVertices(graph_service_pb2.EmptyRequest())
        vertices = vertices_response.vertices
        logger.info(f"Retrieved {len(vertices)} vertices from server")

        # Build the graph structure
        graph = {v: set() for v in vertices}
        for v in vertices:
            neighbors_response = self.server_stub.GetNeighbors(graph_service_pb2.VertexRequest(vertex=v))
            graph[v] = set(neighbors_response.vertices)
        logger.info("Built graph structure")

        # Use the path_finding algorithm
        start_time = time.time()
        path = path_finding.parallel_shortest_path(graph, request.start, request.end)
        end_time = time.time()
        
        logger.info(f"Found shortest path: {path}")
        logger.info(f"Path finding took {end_time - start_time:.6f} seconds")

        return graph_service_pb2.PathResponse(path=path if path else [], time=end_time - start_time)

    def AddVertex(self, request, context):
        logger.info(f"Forwarding AddVertex request for vertex {request.vertex}")
        return self.server_stub.AddVertex(request)

    def RemoveVertex(self, request, context):
        logger.info(f"Forwarding RemoveVertex request for vertex {request.vertex}")
        return self.server_stub.RemoveVertex(request)

    def HasVertex(self, request, context):
        logger.info(f"Forwarding HasVertex request for vertex {request.vertex}")
        return self.server_stub.HasVertex(request)

    def GetAllVertices(self, request, context):
        logger.info("Forwarding GetAllVertices request")
        return self.server_stub.GetAllVertices(request)

    def AddEdge(self, request, context):
        logger.info(f"Forwarding AddEdge request for edge ({request.vertex1}, {request.vertex2})")
        return self.server_stub.AddEdge(request)

    def RemoveEdge(self, request, context):
        logger.info(f"Forwarding RemoveEdge request for edge ({request.vertex1}, {request.vertex2})")
        return self.server_stub.RemoveEdge(request)

    def HasEdge(self, request, context):
        logger.info(f"Forwarding HasEdge request for edge ({request.vertex1}, {request.vertex2})")
        return self.server_stub.HasEdge(request)

    def GetNeighbors(self, request, context):
        logger.info(f"Forwarding GetNeighbors request for vertex {request.vertex}")
        return self.server_stub.GetNeighbors(request)

def serve(broker_port=50052, server_address='localhost:50051'):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    graph_service_pb2_grpc.add_GraphServiceServicer_to_server(BrokerServicer(server_address), server)
    server.add_insecure_port(f'[::]:{broker_port}')
    server.start()
    logger.info(f"Broker started, listening on port {broker_port}")
    server.wait_for_termination()

if __name__ == '__main__':
    broker_port = 50052  # Choose a different port for the broker
    server_address = 'localhost:50051'  # Address of the main server
    serve(broker_port, server_address)