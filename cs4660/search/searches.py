from collections import defaultdict
from collections import deque
# from graph.graph.utils import convert_edge_to_grid_actions
#
from queue import PriorityQueue
import queue as Q

def bfs(graph, initial_node, dest_node):
    path = []
    visited = set()
    queue = [(path,  initial_node, visited)]
    while len(queue)>0:
        q = queue.pop(0)
        dq = deque(q)
        path = dq.popleft()
        node = dq.popleft()
        visited = dq.popleft()
        # print (type(path))
        # print (type(node))
        visited.add(node)
        for neighborNode in graph.neighbors(node):
            if neighborNode == dest_node:
                # print (path + [graph.distance(node, neighborNode)])
                return path + [graph.distance(node, neighborNode)]
            elif neighborNode not in visited:
                queue.append((path + [graph.distance(node,neighborNode)], neighborNode, visited ))
    return path


def dfs(graph, initial_node, dest_node):
    path = []
    visited = set()
    stack = [(path, initial_node, visited)]
    while stack:
        q = stack.pop()
        dq = deque(q)
        path = dq.popleft()
        node = dq.popleft()
        visited = dq.popleft()
        if node == dest_node:
            return path
        visited.add(node)
        for neighborNode in graph.neighbors(node)[::-1]:
            if neighborNode in visited:
                continue
            stack.append(( path + [graph.distance(node, neighborNode)],neighborNode, visited))
    return path



# time complexit :  O((|E| + |V|) log (|V|)
def dijkstra_search(graph,initial_node, dest_node):
    frontier = Q.PriorityQueue()
    final_path = []
    came_from_nodes = []
    going_to_nodes= []
    visited = set()
    path = {}
    distances = defaultdict(lambda: float("inf"))
    path[initial_node] = None
    visted_node = None
    infinity = 99999
    queue = [initial_node]
    frontier = distances
    frontier[initial_node] = 0
    for node in graph.neighbors(initial_node):
        graph.neighbors(node)
        (frontier[node]) = infinity
        for nd in graph.neighbors(node):
            frontier[nd] = infinity

    # print(queue)
    while queue:
        min_dist = 12
        for q in queue:
            # for node, dist in distances.items():
            if frontier[q] < min_dist:
                min_dist = frontier[q]
                visted_node = q
                visited.add(visted_node)

        for q in queue:
            if q == visted_node:
                queue.pop(queue.index(visted_node))

        for node in graph.neighbors(visted_node):
            weight = graph.distance(visted_node, node).weight
            new_weight = min_dist + weight
            if new_weight < frontier[node]:
                frontier[node] = new_weight
                path[node] = visted_node
            queue.append(node)

    path_list = [dest_node]
    while path[dest_node]:
        path_list.append(path[dest_node])
        dest_node = path[dest_node]
    path_list.reverse()
    for from_node in path_list[:-1]:
        came_from_nodes.append(from_node)

    for going_to in path_list[1:]:
        going_to_nodes.append(going_to)

    for v, w in zip(came_from_nodes, going_to_nodes):
        final_path.append(graph.distance(v, w))
    return final_path



# http://www.redblobgames.com/pathfinding/a-star/implementation.html
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, initial_node, dest_node):
    frontier = PriorityQueue()
    frontier.put(initial_node, 0)
    came_from = {}
    cost_so_far = {}
    going_to_nodes = []
    came_from_nodes = []
    final_path = []
    came_from[initial_node] = None
    cost_so_far[initial_node] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == dest_node:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.distance(current, next).weight
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(dest_node, next)
                frontier.put(next, priority)
                came_from[next] = current

    path_list = [dest_node]
    while came_from[dest_node]:
        path_list.append(came_from[dest_node])
        dest_node = came_from[dest_node]
    path_list.reverse()
    for from_node in path_list[:-1]:
        came_from_nodes.append(from_node)
    for going_to in path_list[1:]:
        going_to_nodes.append(going_to)
    for v, w in zip(came_from_nodes, going_to_nodes):
        final_path.append(graph.distance(v, w))
    return final_path




