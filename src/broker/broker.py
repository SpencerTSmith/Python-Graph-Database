import grpc
from concurrent import futures
import time
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generated import graph_service_pb2
from src.generated import graph_service_pb2_grpc
from src.algorithms import path_finding

class BrokerServicer(graph_service_pb2_grpc.GraphServiceServicer):
    def __init__(self, server_addresses):
        self.server_stubs = {}
        for i, address in enumerate(server_addresses):
            channel = grpc.insecure_channel(address)
            stub = graph_service_pb2_grpc.GraphServiceStub(channel)
            self.server_stubs[i] = stub
        self.num_servers = len(server_addresses)
        logger.info(f"Broker connected to {self.num_servers} servers at {server_addresses}")

    def get_responsible_server(self, vertex):
        server_index = sum(ord(c) for c in str(vertex)) % self.num_servers
        try:
            return self.server_stubs[server_index]
        except grpc.RpcError as e:
            logger.error(f"Failed to connect to server {server_index}: {e}")
            raise

    def AddVertex(self, request, context):
        logger.debug(f"Processing AddVertex request for vertex {request.vertex}")
        try:
            return self.get_responsible_server(request.vertex).AddVertex(request)
        except Exception as e:
            logger.error(f"Error in AddVertex: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.OperationResponse(success=False, message=str(e))

    def RemoveVertex(self, request, context):
        logger.debug(f"Processing RemoveVertex request for vertex {request.vertex}")
        try:
            responsible_server = self.get_responsible_server(request.vertex)
            response = responsible_server.RemoveVertex(request)
            
            # Remove the vertex from all other servers as well
            for stub in self.server_stubs.values():
                if stub != responsible_server:
                    stub.RemoveVertex(request)
            
            return response
        except Exception as e:
            logger.error(f"Error in RemoveVertex: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.OperationResponse(success=False, message=str(e))

    def HasVertex(self, request, context):
        logger.debug(f"Processing HasVertex request for vertex {request.vertex}")
        try:
            responsible_server = self.get_responsible_server(request.vertex)
            return responsible_server.HasVertex(request)
        except Exception as e:
            logger.error(f"Error in HasVertex: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.BooleanResponse(value=False)

    def GetAllVertices(self, request, context):
        logger.debug("Processing GetAllVertices request")
        all_vertices = set()
        for stub in self.server_stubs.values():
            try:
                response = stub.GetAllVertices(request)
                all_vertices.update(response.vertices)
            except grpc.RpcError as e:
                logger.error(f"Error getting vertices from a server: {e}")
        logger.info(f"GetAllVertices result - {len(all_vertices)} vertices")
        return graph_service_pb2.VertexListResponse(vertices=list(all_vertices))
    
    def AddEdge(self, request, context):
        logger.debug(f"Processing AddEdge request for edge ({request.vertex1}, {request.vertex2})")
        server1 = self.get_responsible_server(request.vertex1)
        server2 = self.get_responsible_server(request.vertex2)
        
        try:
            response1 = server1.AddEdge(request)
            if server1 != server2:
                response2 = server2.AddEdge(request)
                success = response1.success and response2.success
                message = "Edge added successfully" if success else "Failed to add edge on one or both servers"
            else:
                success = response1.success
                message = response1.message
            
            return graph_service_pb2.OperationResponse(success=success, message=message)
        except Exception as e:
            logger.error(f"Error in AddEdge: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.OperationResponse(success=False, message=str(e))

    def RemoveEdge(self, request, context):
        logger.debug(f"Processing RemoveEdge request for edge ({request.vertex1}, {request.vertex2})")
        server1 = self.get_responsible_server(request.vertex1)
        server2 = self.get_responsible_server(request.vertex2)
        
        try:
            response1 = server1.RemoveEdge(request)
            if server1 != server2:
                response2 = server2.RemoveEdge(request)
                success = response1.success and response2.success
                message = "Edge removed successfully" if success else "Failed to remove edge on one or both servers"
            else:
                success = response1.success
                message = response1.message
            
            return graph_service_pb2.OperationResponse(success=success, message=message)
        except Exception as e:
            logger.error(f"Error in RemoveEdge: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.OperationResponse(success=False, message=str(e))

    def HasEdge(self, request, context):
        logger.debug(f"Processing HasEdge request for edge ({request.vertex1}, {request.vertex2})")
        server1 = self.get_responsible_server(request.vertex1)
        server2 = self.get_responsible_server(request.vertex2)
        
        try:
            response1 = server1.HasEdge(request)
            if server1 != server2:
                response2 = server2.HasEdge(request)
                has_edge = response1.value or response2.value
            else:
                has_edge = response1.value
            
            return graph_service_pb2.BooleanResponse(value=has_edge)
        except Exception as e:
            logger.error(f"Error in HasEdge: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.BooleanResponse(value=False)

    def GetNeighbors(self, request, context):
        logger.debug(f"Processing GetNeighbors request for vertex {request.vertex}")
        all_neighbors = set()
        
        for stub in self.server_stubs.values():
            try:
                response = stub.GetNeighbors(request)
                all_neighbors.update(response.vertices)
            except grpc.RpcError as e:
                logger.error(f"Error getting neighbors from a server: {e}")
        
        # Remove the "EXTERNAL" placeholder if present
        all_neighbors.discard("EXTERNAL")
        
        return graph_service_pb2.VertexListResponse(vertices=list(all_neighbors))
    
    # This uses our parellel processing but it pulls in all vertices from every server before doing so
    def GetShortestPath(self, request, context):
        logger.debug(f"Processing GetShortestPath request from {request.start} to {request.end}")
        try:
            # Collect the entire graph from all servers
            graph = {}
            for stub in self.server_stubs.values():
                vertices_response = stub.GetAllVertices(graph_service_pb2.EmptyRequest())
                for vertex in vertices_response.vertices:
                    neighbors_response = stub.GetNeighbors(graph_service_pb2.VertexRequest(vertex=vertex))
                    graph[vertex] = set(neighbors_response.vertices) - {"EXTERNAL"}

            # Use the parallel_shortest_path function from path_finding
            start_time = time.time()
            path = path_finding.parallel_shortest_path(graph, request.start, request.end)
            end_time = time.time()

            if path:
                return graph_service_pb2.PathResponse(path=path, time=end_time - start_time)
            else:
                return graph_service_pb2.PathResponse(path=[], time=end_time - start_time)
        except Exception as e:
            logger.error(f"Error in GetShortestPath: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return graph_service_pb2.PathResponse(path=[], time=-1)


    def ExecuteCommands(self, request, context):
        logger.debug(f"Processing ExecuteCommands request with {len(request.commands)} commands")
        results = []
        start_time = time.time()
        for command in request.commands:
            try:
                if command.operation == "get-neighbors":
                    response = self.GetNeighbors(graph_service_pb2.VertexRequest(vertex=command.parameters[0]), context)
                    results.append(graph_service_pb2.CommandResult(operation=command.operation, result=str(response.vertices)))
                elif command.operation == "has-edge":
                    response = self.HasEdge(graph_service_pb2.EdgeRequest(vertex1=command.parameters[0], vertex2=command.parameters[1]), context)
                    results.append(graph_service_pb2.CommandResult(operation=command.operation, result=str(response.value)))
                elif command.operation == "add-edge":
                    response = self.AddEdge(graph_service_pb2.EdgeRequest(vertex1=command.parameters[0], vertex2=command.parameters[1]), context)
                    results.append(graph_service_pb2.CommandResult(operation=command.operation, result=response.message))
                elif command.operation == "remove-edge":
                    response = self.RemoveEdge(graph_service_pb2.EdgeRequest(vertex1=command.parameters[0], vertex2=command.parameters[1]), context)
                    results.append(graph_service_pb2.CommandResult(operation=command.operation, result=response.message))
                else:
                    # For operations that don't need the distributed approach, use the original method
                    responsible_server = self.get_responsible_server(command.parameters[0])
                    response = responsible_server.ExecuteCommands(graph_service_pb2.CommandsRequest(commands=[command]))
                    results.extend(response.results)
            except Exception as e:
                logger.error(f"Error executing command {command.operation}: {str(e)}")
                results.append(graph_service_pb2.CommandResult(operation=command.operation, result=f"Error: {str(e)}"))

        total_time = time.time() - start_time
        logger.debug(f"ExecuteCommands completed in {total_time:.6f} seconds")
        return graph_service_pb2.CommandsResponse(results=results, total_time=total_time)

def serve(broker_port=50050, server_addresses=None):
    if server_addresses is None:
        raise ValueError("server_addresses must be provided")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    graph_service_pb2_grpc.add_GraphServiceServicer_to_server(BrokerServicer(server_addresses), server)
    server.add_insecure_port(f'[::]:{broker_port}')
    server.start()
    logger.info(f"Broker started, listening on port {broker_port}")
    logger.info(f"Connected to servers: {server_addresses}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()