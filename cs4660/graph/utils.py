from graph.graph import Node, Edge
from graph import graph as graf

class Tile(object):
    """Node represents basic unit of graph"""

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other_node):
        return self.__hash__() > other_node.__hash__()

    def __lt__(self, other_node):
        return self.__hash__() < other_node.__hash__()

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)


def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph
    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph
    nodes = []
    lines = None
    f = open(file_path)
    i = 0
    for line in f:
        lines = f.readlines()
        if line[i] == '+':
            continue
        if line['-']:
            continue
    f.close()

    x_axis = 1
    y_axis = 0
    for i in lines:
        k = -1
        for j in range(1, len(i) - 2):
            k += 1
            if lines[x_axis][y_axis] == "#":
                continue
            else:
                tile = Tile(k, x_axis - 1, lines[x_axis][y_axis] + "" + lines[x_axis][y_axis + 1])
                graph.add_node(graf.Node(tile))

                print(graf.Node(tile))

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    path = ""

    for edge in edges:

        tile1 = edge.from_node.data
        tile2 = edge.to_node.data


        if (tile2.y - tile1.y) > 0:
            path += "S"
        elif (tile2.x - tile1.x) > 0:
            path += "E"
        elif (tile2.y - tile1.y) < 0:
            path += "N"
        elif (tile2.x - tile1.x) < 0:
            path += "W"
    return path

