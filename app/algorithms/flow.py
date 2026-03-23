from collections import defaultdict, deque

class HRFlowNetwork:
    def __init__(self):
        # We use a dictionary of dictionaries to represent the graph: u -> v -> capacity
        self.graph = defaultdict(dict)

    def add_edge(self, u: str, v: str, capacity: int):
        """Adds a directed edge from u to v with a specific capacity."""
        self.graph[u][v] = capacity
        # We must initialize the reverse edge with 0 capacity for the residual graph
        if u not in self.graph[v]:
            self.graph[v][u] = 0

    def bfs(self, source: str, sink: str, parent: dict) -> bool:
        """Breadth-First Search to find an augmenting path from source to sink."""
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v, cap in self.graph[u].items():
                # If the node isn't visited and there is available capacity > 0
                if v not in visited and cap > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def ford_fulkerson(self, source: str, sink: str) -> dict:
        """Runs the Ford-Fulkerson algorithm to find the absolute maximum flow."""
        parent = {}
        max_flow = 0

        # While there is a valid path from Source to Sink with available capacity
        while self.bfs(source, sink, parent):
            # Find the bottleneck (minimum capacity) along the path we just found
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Update the residual graph (subtract capacity going forward, add to reverse edges)
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return {
            "maximum_interviews_assigned": max_flow
        }