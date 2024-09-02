# Threading Notes

## Python not good at multithreading for CPU bound things
GLI (Global Interpreter Lock) ensures that python threads are not actually running in parallel. For IO bound stuff this doesn't matter as threads that are waiting don't slow down the rest. 
Right now the only part of our program that is CPU bound is probably shortest path, and even that with small graphs is not meaningfully bound. The rest is just interacting with the file system.
I have added threaded loading of graph from file, but it is actually slower, overhead. Next step is probably testing it on a really, really big graph.
"samplegraph2.txt" is 8000 edges long and it is still too small to see any benefit from threading.

GLI is very unfortunate because now we need to do deal with communication overhead between processes.

## Will our graphs contain loops?
If so, we can't use BFS.


