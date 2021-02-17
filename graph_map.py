# Tools:
import networkx as nx
import matplotlib.pyplot as plt
import uuid
from math import sqrt

# Configuration:
import conf

####################################
#           POINT GRAPH
####################################

# Base Graph:
class MapGraph (object):
    def __init__ (self):
        self.M = nx.Graph()
        self._map_list = []

    # Adding nodes in the graph AND connections between nodes:
    # ( nodes <=> class "Tile" )
    def create (self, _map):
        self.M, self._map_list = generate_graph_map (_map)

    # Verify is Graph contains value:
    def __contains__ (self, item):
        row, col = item
        try:
            if self._map_list[row][col] == None:
                return False
            else:
                return True
        except:
            return False

    # Print graph:
    def printContent (self, show = True):
        pos = dict([(item, item.get_coord()) for item in self.M])
        nx.draw(self.M, pos, node_color = 'g', node_size = 0.2, edge_color = 'g', width = 0.5)
        if show:
            plt.show()

    # Finding shortest path between two points:
    def find_path (self, pos_1, pos_2):
        tile_1 = self._map_list[pos_1[0]][pos_1[1]]
        tile_2 = self._map_list[pos_2[0]][pos_2[1]]
        return nx.shortest_path(self.M, tile_1, tile_2, weight = 'weight')

    def printContentPath (self, path, show = True):
        pos = dict([(item, item.get_coord()) for item in self.M])
        G = self.M.subgraph(path)

        nx.draw(G, pos, width = 2, edge_color = '#FD25D7', node_color = '#FD25D7', node_size = 0.2)
        if show:
            plt.show()

# Base Node:
class Tile (tuple):
    def __init__ (self, pos):
        super().__init__()
        row, col = pos
        self.row = row
        self.col = col
        self._id = uuid.uuid4()

    def get_coord (self):
        return (self.row, self.col)

    def __str__ (self):
        return '{}:{}'.format(self.row, self.col)


####################################
#           RUN
####################################

def generate_graph_map ( _map ):

    G = nx.Graph()
    _map_list = [[None] * conf.baseSize[1] for i in range(conf.baseSize[0])]

    for row in range(conf.baseSize[0]):
        for col in range(conf.baseSize[1]):
            _map_list[row][col] = Tile((row, col))

            # Adding connections:
            if col != 0:
                if not verify(_map_list[row][col], _map_list[row][col - 1], _map):
                    G.add_edge(_map_list[row][col], _map_list[row][col - 1], weight = 1 / sqrt(2))
            if col != conf.baseSize[1] - 1 and row != 0:
                if not verify(_map_list[row][col], _map_list[row - 1][col + 1], _map):
                    G.add_edge(_map_list[row][col], _map_list[row - 1][col + 1], weight = 1)
            if row != 0 and col != 0:
                if not verify(_map_list[row][col], _map_list[row - 1][col - 1], _map):
                    G.add_edge(_map_list[row][col], _map_list[row - 1][col - 1], weight = 1)
            if row != 0:
                if not verify(_map_list[row][col], _map_list[row - 1][col], _map):
                    G.add_edge(_map_list[row][col], _map_list[row - 1][col], weight = 1 / sqrt(2))

    return G, _map_list


def verify (pos_1, pos_2, _map):

    """
    pos_1 == Y
    pos_2 == 0

    Detect not allowed diagonal mouvement
    0 X   Y X
    X Y   X 0
    OP_1  OP_2

    X 0   X Y
    Y X   0 X
    OP_3 OP_4

    Note: In our case only OP_1 AND OP_3 is going to be found
    """

    # All other options
    if _map[pos_1.row, pos_1.col] or _map[pos_2.row, pos_2.col]:
        return True

    else:
        # OP_1 --> True
        if pos_1.row - 1 == pos_2.row and pos_1.col - 1 == pos_2.col:
             return _map[pos_1.row, pos_1.col - 1] or _map[pos_2.row, pos_2.col + 1]

        # OP_3 --> True
        elif pos_1.row - 1 == pos_2.row and pos_1.col + 1 == pos_2.col:
            return  _map[pos_1.row, pos_1.col + 1] or _map[pos_2.row, pos_2.col - 1]

        # If none of the above conditions have been accomplished then return false
        else:
            return False
