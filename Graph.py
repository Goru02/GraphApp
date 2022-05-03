import queue as q
#
#
#
#   Currently unused class which holds graph search logic
#
#
#
class Graph:
    def __init__(self, heuristics, directed):
        self.directed = directed
        self.heuristics = heuristics
        self.adjancencies = {}
        for node in heuristics.keys():
            self.adjancencies[node] = []

    def addNode(self, node):
        self.nodes.append(node)
        self.adjancencies[node] = []

    def addEdge(self, node1, node2, weight):
        self.adjancencies[node1].append([node2, weight])
        if not self.directed:
            self.adjacencies[node2].append([node1, weight])

    def breadthFirstSearch(self, start, goal):
        visited = []

        queue = [(start, [start])]

        while queue:
            node, path = queue.pop(0)

            if node in visited:
                continue

            visited.append(node)

            if node == goal:
                return visited, path

            for adjNode, weight in self.adjancencies[node]:
                queue.append((adjNode, path+[adjNode]))

    def depthFirstSearch(self, start, goal):
        visited = []

        stack = [(start, [start])]

        while stack:
            node, path = stack.pop()

            if node in visited:
                continue

            visited.append(node)

            if node == goal:
                return visited, path

            for adjNode, weight in self.adjancencies[node]:
                stack.append((adjNode, path+[adjNode]))

    def uniformCostSearch(self, start, goal):
        visited = []

        queue = q.PriorityQueue()
        queue.put((0, start, [start]))

        while queue:
            cost, node, path = queue.get()

            if node in visited:
                continue

            visited.append(node)

            if node == goal:
                return visited, path

            for adjNode, weight in self.adjancencies[node]:
                queue.put((cost+weight, adjNode, path+[adjNode]))
    
    def iterativeDeepingSearch(self, start, goal, limit):
        for i in range(1, limit+1):
            print("level =", i)
            visited = []

            stack = [(start, [start], 1)]

            while stack:
                node, path, level = stack.pop()

                if node in visited or level > i:
                    continue

                visited.append(node)

                if node == goal:
                    return visited, path

                for adjNode, weight in self.adjancencies[node]:
                    stack.append((adjNode, path+[adjNode], level+1))
            print(visited)

    def greedySearch(self, start, goal):
        visited = []

        queue = q.PriorityQueue()
        queue.put((self.heuristics[start], start, [start]))

        while queue:
            heuristic, node, path = queue.get()

            if node in visited:
                continue

            visited.append(node)

            if node == goal:
                return visited, path

            for adjNode, weight in self.adjancencies[node]:
                queue.put((self.heuristics[adjNode], adjNode, path+[adjNode]))

    def aStarSearch(self, start, goal):
        visited = []

        queue = q.PriorityQueue()
        queue.put((self.heuristics[start], 0, start, [start]))

        while queue:
            total, cost, node, path = queue.get()

            if node in visited:
                continue

            visited.append(node)

            if node == goal:
                return visited, path

            for adjNode, weight in self.adjancencies[node]:
                queue.put((self.heuristics[adjNode]+cost+weight, cost+weight, adjNode, path+[adjNode]))


graph = Graph({
    's': 13, 'a': 12, 'b': 4, 'c': 7, 'd': 3, 'e': 8, 'f': 2, 'g': 0, 'h': 4, 'i': 9
    }, True)
graph.addEdge('s', 'a', 3)
graph.addEdge('a', 'c', 4)
graph.addEdge('a', 'd', 1)
graph.addEdge('s', 'b', 2)
graph.addEdge('b', 'e', 3)
graph.addEdge('b', 'f', 1)
graph.addEdge('e', 'h', 5)
graph.addEdge('f', 'i', 2)
graph.addEdge('f', 'g', 3)

print("Breadth First:")
print(graph.breadthFirstSearch('s', 'g'))
print("_______________________________________")
print("Depth First:")
print(graph.depthFirstSearch('s', 'g'))
print("_______________________________________")
print("Uniform Cost")
print(graph.uniformCostSearch('s', 'g'))
print("_______________________________________")
print("Iterative Deepening")
print(graph.iterativeDeepingSearch('s', 'g', 4))
print("_______________________________________")
print("Greedy Search")
print(graph.greedySearch('s', 'g'))
print("_______________________________________")
print("A* Search")
print(graph.aStarSearch('s', 'g'))
print("_______________________________________")