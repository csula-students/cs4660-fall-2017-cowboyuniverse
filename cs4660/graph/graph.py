from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    nodeEdgeWeight = []
    f = open(file_path)
    content = f.readlines()
    size = content[:1][0].split('\n')[0]
    size = int(size)

    i = 0
    while i < size:
        graph.add_node(Node(i))
        i += 1

    for line in content[1:]:
        nodeEdgeWeight.append(line.split('\n'))
        for i in nodeEdgeWeight:
            arr = i[0].split(':')

        from_node = int(arr[0])
        to_node = int(arr[1])
        weight = int(arr[2])
        edge = Edge(Node(from_node), Node(to_node), weight)

        if type(graph) is ObjectOriented:
            graph.edges.append(edge)

        if type(graph) is AdjacencyList:
            graph.adjacency_list[Node(from_node)].append(edge)

        if type(graph) is AdjacencyMatrix:
            graph.adjacency_matrix[from_node][to_node] = weight

    return graph

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

class AdjacencyList(object):

    def __init__(self):
        self.adjacency_list = {}

    # O(n + m) n is vertex and m is edges, iterating the loop
    def neighbors(self, node):
        list = []
        items = self.adjacency_list[node]
        neighborhood = []
        for i in items:
            neighborhood.append(i.to_node)
        return neighborhood

    # O(n + m) n is vertex and m is edges, iterating the loop
    def adjacent(self, node_1, node_2):
        nodeOneNeighbors = self.neighbors(node_1)
        for node  in nodeOneNeighbors:
            if node == node_2:
                return True
        return False

    # only doing a seek which is return O(1)
    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        else:
            self.adjacency_list[node] = []
            return True

    # O(n^2) iteration of two loops and b/c its removing
    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for edges in self.adjacency_list.values():
                for edge in edges:
                    if edge.to_node == node:
                        self.remove_edge(edge)
            return True
        else:
            return False


    # only doing a seek which is return O(1)
    def add_edge(self, edge):
        if edge in self.adjacency_list[edge.from_node]:
            return False
        else:
            self.adjacency_list[edge.from_node].append(edge)
            return True

    # removing from the adjacency_list cost is O(n)
    def remove_edge(self, edge):
        if edge not in self.adjacency_list[edge.from_node]:
            return False
        else:
            self.adjacency_list[edge.from_node].remove(edge)
            return True

class AdjacencyMatrix(object):
    def __init__(self):
        self.adjacency_matrix = []
        self.nodes = {}


    # only doing a seek which is return O(1)
    def adjacent(self, node_1, node_2):
        if node_1 and node_2 not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[node_1]][self.nodes[node_2]] != 0:
            return True
        else:
            return False

    # O(n^2) loop of k and v loop and appending
    def neighbors(self, node):
        listOfNeighbors = []
        for k, v in self.nodes.items():
            if self.adjacency_matrix[ self.nodes[node]][v] != 0:
                listOfNeighbors.append(k)
        return listOfNeighbors

    # O(n^2) loop of adjacecy_matrix and appending
    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes[node] = len(self.nodes)
        for nodes in self.adjacency_matrix:
            nodes.append(0)
        self.adjacency_matrix.append([0] * len(self.nodes))
        return True

    # O(n^2)
    def remove_node(self, node):
        if node not in self.nodes:
            return False
        current_node = self.__get_node_index(node)
        for nodes in self.adjacency_matrix:
            nodes[current_node] = 0
        return True

    # only doing a seek which is return O(1)
    def add_edge(self, edge):
        if edge.from_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] != 0:
            return False
        self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] = edge.weight
        return True

    # only doing a seek which is return O(1)
    def remove_edge(self, edge):
        if edge.from_node and edge.to_node not in self.nodes:
            return False
        if self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] == 0:
            return False
        self.adjacency_matrix[self.nodes[edge.from_node]][self.nodes[edge.to_node]] = 0
        return True

    # only doing a seek which is return O(1)
    def __get_node_index(self, node):
        return self.nodes[node]


class ObjectOriented(object):
    def __init__(self):
        self.edges = []
        self.nodes = []

    # only doing a seek which is return O(1)
    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1:
                if edge.to_node == node_2:
                    return True
                else:
                    False
        return False

    # O(n) because it's creating a list of neighbors
    def neighbors(self, node):
        listOfNeighbors = []
        for edge in self.edges:
            if edge.from_node == node:
                listOfNeighbors.append(edge.to_node)
        return listOfNeighbors

    # O(n) because it's appending
    def add_node(self, node):
        for node_element in self.nodes:
            if node == node_element:
                return False
        self.nodes.append(node)
        return True

    # O(n^2) doing a loop and removing and doing another remove
    def remove_node(self, node):
        if node not in self.nodes:
            return False
        else:
            self.nodes.remove(node)
            for edge in self.edges:
                if self.adjacent(edge.from_node, node):
                    self.remove_edge(edge)
                if self.adjacent(edge.to_node, node):
                    self.remove_edge(edge)
            return True

    # O(n) doing an append
    def add_edge(self, edge):
        if edge in self.edges:
            return False
        if edge not in self.edges:
            self.edges.append(edge)
            return True

    # O(n) doing a remove
    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        if edge not in self.edges:
            return False



# ----------------NOTES ----------------------
# python -m unittest test.test_graph.TestObjectOriented
# python -m unittest test.test_graph.TestAdjacencyList
# python -m unittest test.test_graph.TestAdjacencyMatrix
# python -m unittest discover

    # adding a new node "f"
    # g = { "e": ["c"],
    #      "f": [] }

# resizing array
# a = [1, 2, 3]
# b = []
# for i in range(6):
#     b.append((([0] * i) + a[i:i+1] + ([0] * (len(a) - 1 - i)))[:len(a)])


"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""
