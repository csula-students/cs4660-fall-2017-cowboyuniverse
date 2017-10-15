"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

from collections import deque
import json
import codecs
import queue as Q

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"


class Node(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))

class AdjacencyMatrix(object):
    def __init__(self):
        self.adjacency_matrix = []
        self.nodes = {}


    def adjacent(self, node_1, node_2):
        if node_1 and node_2 not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[node_1]][self.nodes[node_2]] != 0:
            return True
        else:
            return False

    def neighbors(self, node):
        listOfNeighbors = []
        for k, v in self.nodes.items():
            if self.adjacency_matrix[ self.nodes[node]][v] != 0:
                listOfNeighbors.append(k)
        return listOfNeighbors



    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes[node] = len(self.nodes)
        for nodes in self.adjacency_matrix:
            nodes.append(0)
        self.adjacency_matrix.append([0] * len(self.nodes))
        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False
        current_node = self.__get_node_index(node)
        for nodes in self.adjacency_matrix:
            nodes[current_node] = 0
        return True


    def add_edge(self, edge):
        if edge.from_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] != 0:
            return False
        self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] = edge.weight
        return True


    def remove_edge(self, edge):
        if edge.from_node and edge.to_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] == 0:
            return False
        self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] = 0
        return True


    def __get_node_index(self, node):
        return self.nodes[node]


    def distance(self, node_1, node_2):
        edgeWeight = self.adjacency_matrix[self.nodes[node_1]][self.nodes[node_2]]
        edge = Edge(node_1, node_2, edgeWeight)
        if edgeWeight == 0:
            return None
        return edge





def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)


def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)



def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response




def bfs(initial_node, dest_node):
    path = []
    visited = set()
    queue = [(path, initial_node, visited)]

    while len(queue)>0:
        q = queue.pop(0)
        dq = deque(q)
        path = dq.popleft()
        node = dq.popleft()
        visited = dq.popleft()
        # print (type(path))
        # print(type(node))
        # print(type(visited))

        for neighborNode in node['neighbors']:
            visited.add(neighborNode['id'])
            path = [(transition_state(neighborNode['id'], node['id']))]

        for visitNode in visited:
            for neighbor in get_state(visitNode)['neighbors']:
                json = transition_state(visitNode, neighbor['id'])
                weight = [json['event']['effect'] for weight in json['event']]
                path = [get_state(visitNode)['location']['name'] + '(' + visitNode + ')' + ': ' + neighbor['location'][
                    'name'] + '(' + neighbor['id'] + ')' + ':' + str(weight[0])]

                if dest_node['id'] == neighbor['id']:
                    print(path)
                    return path

                elif neighbor['id'] not in visited:
                    print(path)
                    queue.append((path, get_state(neighbor['id']), visited))



# http://www.redblobgames.com/pathfinding/a-star/introduction.html
def dijkstra(start, goal):
    graph = AdjacencyMatrix
    frontier = Q.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current


if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')

    bfs(empty_room, dark_room)
    dijkstra(empty_room, dark_room)



