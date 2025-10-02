import heapq

class Edge:
    def __init__(self, v, capacity, cost, rev):
        self.v = v
        self.capacity = capacity
        self.cost = cost
        self.rev = rev

class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, capacity, cost):
        forward = Edge(v, capacity, cost, len(self.graph[v]))
        backward = Edge(u, 0, -cost, len(self.graph[u]))
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def min_cost_flow(self, s, t, maxf=float('inf')):
        n = self.n
        h = [0]*n  # potentials
        prevv = [0]*n
        preve = [0]*n
        flow = 0
        cost = 0

        while flow < maxf:
            dist = [float('inf')]*n
            dist[s] = 0
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if dist[u] < d:
                    continue
                for i, e in enumerate(self.graph[u]):
                    if e.capacity > 0 and dist[e.v] > dist[u] + e.cost + h[u] - h[e.v]:
                        dist[e.v] = dist[u] + e.cost + h[u] - h[e.v]
                        prevv[e.v] = u
                        preve[e.v] = i
                        heapq.heappush(pq, (dist[e.v], e.v))
            if dist[t] == float('inf'):
                break  # no more augmenting path

            # Update potentials
            for v in range(n):
                if dist[v] < float('inf'):
                    h[v] += dist[v]

            # Find min residual capacity along path
            d = maxf - flow
            v = t
            while v != s:
                d = min(d, self.graph[prevv[v]][preve[v]].capacity)
                v = prevv[v]

            # Apply flow
            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                e.capacity -= d
                self.graph[v][e.rev].capacity += d
                cost += e.cost * d
                v = prevv[v]
            flow += d

        return flow, cost

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    n = 4
    mcmf = MinCostMaxFlow(n)
    mcmf.add_edge(0, 1, 2, 1)
    mcmf.add_edge(0, 2, 1, 2)
    mcmf.add_edge(1, 2, 1, 1)
    mcmf.add_edge(1, 3, 1, 3)
    mcmf.add_edge(2, 3, 2, 1)

    flow, cost = mcmf.min_cost_flow(0, 3)
    print("Max Flow:", flow)   # Should be 3
    print("Min Cost:", cost)   # Should be 6 (guaranteed)
