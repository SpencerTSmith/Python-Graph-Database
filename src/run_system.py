# did not finish this yet

import subprocess
import sys
import time
import os

def run_command(command, background=True):
    if background:
        if os.name == 'nt':  # For Windows
            return subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # For Unix-like systems
            return subprocess.Popen(command, shell=True)
    else:
        subprocess.run(command, shell=True)

def main():
    num_servers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    data_file = sys.argv[2] if len(sys.argv) > 2 else "graph_data.txt"

    processes = []

    # Start servers
    for i in range(num_servers):
        command = f"python -m src.main server --num-servers {num_servers} --server-id {i} --data-file {data_file}"
        processes.append(run_command(command))
        time.sleep(1)  # Give each server a second to start up

    # Start broker
    broker_command = f"python -m src.main broker --num-servers {num_servers} --data-file {data_file}"
    processes.append(run_command(broker_command))
    time.sleep(1)  # Give the broker a second to start up

    # Start client (in foreground)
    client_command = f"python -m src.main client --num-servers {num_servers}"
    run_command(client_command, background=False)

    # After client exits, terminate all background processes
    for process in processes:
        process.terminate()

if __name__ == "__main__":
    main()