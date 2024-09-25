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
from src.core.graph import Graph
from src.core.operations import GraphOperations

class GraphServicer(graph_service_pb2_grpc.GraphServiceServicer):
    def __init__(self):
        self.graph = Graph()
        self.operations = GraphOperations(self.graph)
        logger.info("Graph initialized")

    def AddVertex(self, request, context):
        logger.info(f"Received AddVertex request for vertex {request.vertex}")
        success = self.operations.add_vertex(request.vertex)
        message = "Vertex added successfully" if success else "Failed to add vertex"
        logger.info(f"AddVertex result - {message}")
        return graph_service_pb2.OperationResponse(success=success, message=message)

    def RemoveVertex(self, request, context):
        logger.info(f"Received RemoveVertex request for vertex {request.vertex}")
        success = self.operations.remove_vertex(request.vertex)
        message = "Vertex removed successfully" if success else "Failed to remove vertex"
        logger.info(f"RemoveVertex result - {message}")
        return graph_service_pb2.OperationResponse(success=success, message=message)

    def HasVertex(self, request, context):
        logger.info(f"Received HasVertex request for vertex {request.vertex}")
        has_vertex = self.operations.has_vertex(request.vertex)
        logger.info(f"HasVertex result - {has_vertex}")
        return graph_service_pb2.BooleanResponse(value=has_vertex)

    def GetAllVertices(self, request, context):
        logger.info("Received GetAllVertices request")
        vertices = self.operations.get_all_vertices()
        logger.info(f"GetAllVertices result - {len(vertices)} vertices")
        return graph_service_pb2.VertexListResponse(vertices=vertices)

    def AddEdge(self, request, context):
        logger.info(f"Received AddEdge request for edge ({request.vertex1}, {request.vertex2})")
        success = self.operations.add_edge(request.vertex1, request.vertex2)
        message = "Edge added successfully" if success else "Failed to add edge"
        logger.info(f"AddEdge result - {message}")
        return graph_service_pb2.OperationResponse(success=success, message=message)

    def RemoveEdge(self, request, context):
        logger.info(f"Received RemoveEdge request for edge ({request.vertex1}, {request.vertex2})")
        success = self.operations.remove_edge(request.vertex1, request.vertex2)
        message = "Edge removed successfully" if success else "Failed to remove edge"
        logger.info(f"RemoveEdge result - {message}")
        return graph_service_pb2.OperationResponse(success=success, message=message)

    def HasEdge(self, request, context):
        logger.info(f"Received HasEdge request for edge ({request.vertex1}, {request.vertex2})")
        has_edge = self.operations.has_edge(request.vertex1, request.vertex2)
        logger.info(f"HasEdge result - {has_edge}")
        return graph_service_pb2.BooleanResponse(value=has_edge)

    def GetNeighbors(self, request, context):
        logger.info(f"Received GetNeighbors request for vertex {request.vertex}")
        neighbors = self.operations.get_neighbors(request.vertex)
        logger.info(f"GetNeighbors result - {len(neighbors) if neighbors else 0} neighbors")
        return graph_service_pb2.VertexListResponse(vertices=list(neighbors) if neighbors else [])

def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    graph_service_pb2_grpc.add_GraphServiceServicer_to_server(GraphServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Server started, listening on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()