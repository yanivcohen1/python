# https://www.youtube.com/watch?v=Urx87-NMm6c
graph = {
    'A': ['B', 'G'],
    'B': ['C', 'D', 'E'],
    'C': [],
    'D': [],
    'E': ['F'],
    'F': [],
    'G': ['H'],
    'H': ['I'],
    'I': [],
}

visiteds = set() # Set to keep track of visited nodes of graph.

def dfs(graph, node):
    visited = []
    stack = [] # stack insted of recursion

    visited.append(node)
    stack.append(node)

    while stack:
        s = stack.pop()
        print(s, end=" ")

        # reverse iterate through edge list so results match recursive version
        for n in reversed(graph[s]):
            if n not in visited:
                visited.append(n)
                stack.append(n)

def dfs_recursive(visited, graph, node):  #function for dfs
    if node not in visited:
        print (node, end=" ")
        visiteds.add(node)
        for neighbour in graph[node]:
            dfs_recursive(visiteds, graph, neighbour)

def main():
    dfs(graph, 'A')
    print("")
    dfs_recursive(visiteds, graph, 'A')


main()
