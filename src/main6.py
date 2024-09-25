# covers c and e

import argparse
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.server.server import serve as start_server
from src.client.client import main as start_client

def main():
    parser = argparse.ArgumentParser(description="Graph Database Application")
    parser.add_argument("mode", choices=["server", "client"], help="Run as server or client")
    parser.add_argument("--host", default="localhost", help="Server host (for client mode)")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    
    args = parser.parse_args()

    if args.mode == "server":
        print(f"Starting server on port {args.port}")
        start_server()
    elif args.mode == "client":
        print(f"Starting client, connecting to {args.host}:{args.port}")
        start_client(host=args.host, port=args.port)

if __name__ == "__main__":
    main()