import grpc
from concurrent import futures
import time
import sys
import os
import logging
from src.core.operations import Commands

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
    def __init__(self, initial_data):
        self.graph = Graph()
        self.operations = GraphOperations(self.graph)
        self.load_initial_data(initial_data)
        logger.info(f"Loaded initial data: {len(initial_data)} vertices")

    def load_initial_data(self, data):
        vertex_count = 0
        for vertex, edges in data.items():
            self.operations.add_vertex(vertex)
            vertex_count += 1
            for edge in edges:
                self.operations.add_edge(vertex, edge)
        logger.info(f"Loaded {vertex_count} vertices")
    
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
        if not self.operations.has_vertex(request.vertex1):
            # This is an external vertex, add it as a placeholder
            self.operations.add_vertex(request.vertex1)
        if not self.operations.has_vertex(request.vertex2):
            # This is an external vertex, add it as a placeholder
            self.operations.add_vertex(request.vertex2)
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

    def GetShortestPath(self, request, context):
        logger.info(f"Received GetShortestPath request from {request.start} to {request.end}")
        path, time = self.operations.get_shortest_path(request.start, request.end)
        logger.info(f"GetShortestPath result - Path: {path}, Time: {time}")
        return graph_service_pb2.PathResponse(path=path if path else [], time=time)
    
    def ExecuteCommands(self, request, context):
        logger.info(f"Received ExecuteCommands request with {len(request.commands)} commands")
        results = []
        start_time = time.time()
        
        for command in request.commands:
            result = self.execute_single_command(command)
            results.append(graph_service_pb2.CommandResult(operation=command.operation, result=result))
        
        total_time = time.time() - start_time
        logger.info(f"ExecuteCommands completed in {total_time:.6f} seconds")
        return graph_service_pb2.CommandsResponse(results=results, total_time=total_time)

    def execute_single_command(self, command):
        operation = command.operation
        params = command.parameters

        try:
            if operation == Commands.ADD_VERT:
                success = self.operations.add_vertex(params[0])
                return f"{'success' if success else 'fail'}"
            
            elif operation == Commands.ADD_EDGE:
                success = self.operations.add_edge(params[0], params[1])
                return f"{'success' if success else 'fail'}"
            
            elif operation == Commands.REM_VERT:
                success = self.operations.remove_vertex(params[0])
                return f"{'success' if success else 'fail'}"
            
            elif operation == Commands.REM_EDGE:
                success = self.operations.remove_edge(params[0], params[1])
                return f"{'success' if success else 'fail'}"
            
            elif operation == Commands.HAS_VERT:
                result = self.operations.has_vertex(params[0])
                return str(result)
            
            elif operation == Commands.HAS_EDGE:
                result = self.operations.has_edge(params[0], params[1])
                return str(result)
            
            elif operation == Commands.GET_HOOD:
                neighborhood = self.operations.get_neighbors(params[0])
                return str(neighborhood)
            
            elif operation == Commands.GET_SSSP:
                path, sp_time = self.operations.get_shortest_path(params[0], params[1])
                return f"{str(path)} in {sp_time:.6f} seconds"
            
            else:
                return "unknown command"

        except IndexError:
            return "invalid parameters"
        except Exception as e:
            logger.error(f"Error executing command {operation}: {str(e)}")
            return f"error: {str(e)}"

def serve(port=50051, initial_data=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    graph_service_pb2_grpc.add_GraphServiceServicer_to_server(GraphServicer(initial_data), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Server started, listening on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()