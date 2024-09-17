import multiprocessing as mp
from multiprocessing.managers import DictProxy
from typing import List, Optional, Dict, Set
from queue import Empty

def worker_bfs(graph: Dict[str, Set[str]], start: str, end: str, 
               task_queue: mp.Queue, result_queue: mp.Queue, 
               visited: DictProxy, found: mp.Value):
    while not found.value:
        try:
            current_path = task_queue.get(timeout=0.1)
            current_node = current_path[-1]

            if current_node == end:
                if not found.value:
                    found.value = True
                    result_queue.put(current_path)
                return

            if current_node not in visited:
                visited[current_node] = True
                for neighbor in graph.get(current_node, set()):
                    if neighbor not in visited:
                        new_path = current_path + [neighbor]
                        task_queue.put(new_path)
        except Empty:
            return

def parallel_bfs(graph: Dict[str, Set[str]], start: str, end: str, num_processes: int = 4) -> Optional[List[str]]:
    manager = mp.Manager()
    task_queue = manager.Queue()
    result_queue = manager.Queue()
    visited = manager.dict()
    found = manager.Value('b', False)

    task_queue.put([start])

    processes = []
    for _ in range(num_processes):
        p = mp.Process(target=worker_bfs, args=(graph, start, end, task_queue, result_queue, visited, found))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if not result_queue.empty():
        return result_queue.get()
    return None

def parallel_shortest_path(graph: Dict[str, Set[str]], start: str, end: str) -> Optional[List[str]]:
    return parallel_bfs(graph, start, end)

# Regular BFS for comparison (optional)
def bfs_shortest_path(graph: Dict[str, Set[str]], start: str, end: str) -> Optional[List[str]]:
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

    return None  # No path found