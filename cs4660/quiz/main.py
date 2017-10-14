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

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"


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




def dfs(graph, start, end):
    path = []
    visited = set()
    stack = [(path, start, visited)]
    # print(stack)
    while len(stack) > 0:
        q = stack.pop()
        dq = deque(q)
        path = dq.popleft()
        node = dq.popleft()
        visited = dq.popleft()
        # print(node)

        # for item in node:
        #     print(item)
        #
        # for item in empty_room['neighbors'][0]:
        #     print(item)
        #
        # for item in empty_room['location']:
        #     print(item)
        #
        # for item in get_state(node['id']):
        #     print(item)

        # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
        # print(get_state(empty_room['id']))

        if get_state(start['id'])  == get_state(end['id']):
            print (get_state(start['id']) )
            return path

        # if node['neighbors'][0]['id'] == end['neighbors'][0]['id']:
        #     print(node['neighbors'][0]['id'])
        #     path = node['neighbors'][0]['id']

        for neighborNode in graph.neighbors(node['neighbors'])[::-1]:
            if neighborNode in visited:
                continue
            stack.append((path + [graph.distance(node, neighborNode)], neighborNode, visited))
    return path






if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')
    # print(empty_room)
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    # print(get_state(empty_room['id']))

    graph = AdjacencyMatrix()
    dfs(graph,empty_room, dark_room)



# {'location': {'x': 0.41050677394431695, 'name': 'Empty Room', 'y': 0.3128340566729299}, 'neighbors': [{'location': {'x': 0.41395402442946244, 'name': 'Dire Tombs', 'y': 0.05581702965734227}, 'neighbors': [], 'id': '44dfaae131fa9d0a541c3eb790b57b00'}, {'location': {'x': 0.034009476916210486, 'name': 'Hall Way', 'y': 0.4557497412525217}, 'neighbors': [], 'id': '547c87c401822417fe069546143de4bb'}, {'location': {'x': 0.9663475335965225, 'name': 'Hall Way', 'y': 0.5341404874731764}, 'neighbors': [], 'id': '0d1d67f3e6bf24e4c2acff975025a497'}, {'location': {'x': 0.14817408641021726, 'name': 'Empty Room', 'y': 0.7622836109520683}, 'neighbors': [], 'id': 'ef296fb452b14eb1cf579fa69d0fe7da'}, {'location': {'x': 0.06790011592868717, 'name': 'Empty Room', 'y': 0.2715183032482974}, 'neighbors': [], 'id': 'bc59dd94f397de7cc7eeca02752d7a15'}, {'location': {'x': 0.14817408641021726, 'name': 'Empty Room', 'y': 0.7622836109520683}, 'neighbors': [], 'id': 'ef296fb452b14eb1cf579fa69d0fe7da'}, {'location': {'x': 0.27200464110221384, 'name': 'Room with cage', 'y': 0.8878513114930595}, 'neighbors': [], 'id': '2b04cd8a31bfd09aa663787fbb150265'}, {'location': {'x': 0.8918202638919476, 'name': 'Empty Room', 'y': 0.97217634152161}, 'neighbors': [], 'id': 'dcb4565202e804f1f27120dabb32bd87'}], 'id': '7f3dc077574c013d98b2de8f735058b4'}


