import argparse
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.server.server import serve as start_server
from src.client.client import main as start_client
from src.broker.broker import serve as start_broker

def main():
    parser = argparse.ArgumentParser(description="Graph Database Application")
    parser.add_argument("mode", choices=["server", "broker", "client"], help="Run as server, broker, or client")
    parser.add_argument("--host", default="localhost", help="Server/Broker host (for client mode)")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--broker-port", type=int, default=50052, help="Broker port")
    parser.add_argument("--server-address", default="localhost:50051", help="Server address (for broker mode)")
    
    args = parser.parse_args()

    if args.mode == "server":
        print(f"Starting server on port {args.port}")
        start_server(port=args.port)
    elif args.mode == "broker":
        print(f"Starting broker on port {args.broker_port}, connecting to server at {args.server_address}")
        start_broker(broker_port=args.broker_port, server_address=args.server_address)
    elif args.mode == "client":
        client_port = args.broker_port  # Connect to the broker by default
        print(f"Starting client, connecting to {args.host}:{client_port}")
        start_client(host=args.host, port=client_port)

if __name__ == "__main__":
    main()