import argparse
import sys
import os
import logging
import json
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server.server import serve as start_server
from src.client.client import main as start_client
from src.broker.broker import serve as start_broker
from data.data_loader import load_graph_data, partition_graph

def get_server_addresses(num_servers, base_port=50051):
    return [f'localhost:{base_port + i*2}' for i in range(num_servers)]


def set_to_list(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj

def load_or_create_partitions(data_file, num_servers):
    partition_file = Path(f"partitioned_data_{num_servers}.json")
    
    if partition_file.exists():
        try:
            with open(partition_file, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded existing partition file: {partition_file}")
            return data
        except json.JSONDecodeError:
            logger.warning(f"Corrupted partition file detected. Deleting {partition_file}")
            os.remove(partition_file)
        except Exception as e:
            logger.error(f"Error loading partition file: {e}")
    
    logger.info("Creating new partitioned data")
    graph_data = load_graph_data(data_file)
    logger.info(f"Loaded graph data with {len(graph_data)} vertices")
    
    partitioned_data = partition_graph(graph_data, num_servers)
    logger.info(f"Partitioned data into {len(partitioned_data)} parts")
    
    # Convert sets to lists and ensure keys are strings
    serializable_data = {str(k): set_to_list(v) for k, v in partitioned_data.items()}
    
    try:
        with open(partition_file, 'w') as f:
            json.dump(serializable_data, f)
        logger.info(f"Successfully wrote partitioned data to {partition_file}")
    except Exception as e:
        logger.error(f"Failed to write partition file: {e}")
    
    return serializable_data

def main():
    parser = argparse.ArgumentParser(description="Graph Database Application")
    parser.add_argument("mode", choices=["server", "broker", "client"], help="Run as server, broker, or client")
    parser.add_argument("num_servers", type=int, nargs='?', default=3, help="Number of servers")
    parser.add_argument("--server-id", type=int, help="Server ID (required for server mode)")
    parser.add_argument("--host", default="localhost", help="Server/Broker host (for client mode)")
    parser.add_argument("--broker-port", type=int, default=50050, help="Broker port")
    parser.add_argument("--data-file", default="data/num_large_graph.txt", help="Path to the graph data file")
    
    args = parser.parse_args()

    server_addresses = get_server_addresses(args.num_servers)

    # Load or create partitioned data
    partitioned_data = load_or_create_partitions(args.data_file, args.num_servers)
    
    logger.info(f"Partitioned data keys: {list(partitioned_data.keys())}")
    for key, value in partitioned_data.items():
        logger.info(f"Partition {key}: {len(value)} vertices")

    if args.mode == "server":
        if args.server_id is None:
            logger.error("Server ID is required for server mode. Use --server-id")
            return
        if args.server_id >= args.num_servers:
            logger.error(f"Server ID {args.server_id} is not valid for {args.num_servers} servers")
            return

        server_id_str = str(args.server_id)
        if server_id_str not in partitioned_data:
            logger.error(f"No data found for server ID {args.server_id}. Available partitions: {list(partitioned_data.keys())}")
            return

        port = int(server_addresses[args.server_id].split(':')[1])
        logger.info(f"Starting server {args.server_id} on port {port}")
        start_server(port=port, initial_data=partitioned_data[server_id_str])

    elif args.mode == "broker":
        logger.info(f"Starting broker on port {args.broker_port}, connecting to servers at {server_addresses}")
        start_broker(broker_port=args.broker_port, server_addresses=server_addresses)

    elif args.mode == "client":
        logger.info(f"Starting client, connecting to broker at {args.host}:{args.broker_port}")
        start_client(host=args.host, port=args.broker_port)

if __name__ == "__main__":
    main()