# Tools:
import networkx as nx
import matplotlib.pyplot as plt
import uuid

####################################
#           ROOM GRAPH
####################################

#Base Graph:
class RoomGraph (object):
    def __init__ (self):
        self.R = nx.Graph()

    # Adding nodes in the Graph:
    # ( nodes <=> class Room )
    def create (self, _connect):
        for item in _connect:
            self.R.add_node(Room(item))

    # Adding connections between nodes:
    def connectRooms (self):
        _next = list(self.R.nodes())
        for room_1 in _next:
            for room_2 in _next:
                if room_2 == room_1:
                    continue
                elif len(room_2.master_points & room_1.master_points) == 2:
                    self.R.add_edge(room_1, room_2, points = tuple(room_2.master_points & room_1.master_points))
                else:
                    pass

    # Print graph:
    def printContent (self, show = True):
        pos = dict([(item, item.center) for item in self.R])
        nx.draw(self.R, pos, with_labels = True, node_color='b')
        if show:
            plt.show()

    # Adding Doors to Game:
    def add_doors (self):
        doors = list()
        for node_1, node_2 in self.R.edges():
            wall_1, wall_2 = self.R[node_1][node_2]['points']

            new_row = int(( wall_1.row + wall_2.row ) * .5)
            new_col = int(( wall_1.col + wall_2.col ) * .5)

            doors.append( DoorClass(new_row, new_col) )

        return doors

#Base Node:
class Room (object):
    def __init__ (self, pos):
        self.master_points = set(pos)
        self._id = uuid.uuid4()
        self.get_center()

    def __str__ (self):
        return '{}:{}'.format(self.center[0], self.center[1])

    def get_center (self):
        _min_row = min( item.row for item in self.master_points )
        _max_row = max( item.row for item in self.master_points )
        _min_col = min( item.col for item in self.master_points )
        _max_col = max( item.col for item in self.master_points )

        for node in self.master_points:
            # Top Left Point:
            if node.row == _min_row and node.col == _min_col:
                self.topleft = node

            # Top Right Point:
            elif node.row == _min_row and node.col == _max_col:
                self.topright = node

            # Bottom Left Point:
            elif node.row == _max_row and node.col == _min_col:
                self.bottomleft = node

            # Bottom Right Point:
            elif node.row == _max_row and node.col == _max_col:
                self.bottomright = node

            else:
                continue

        self.center = (_min_row + _max_row) // 2, (_min_col + _max_col) // 2

        return self.center


####################################
#           DOOR
####################################

class DoorClass (object):
    def __init__ (self, row, col):
        self.row = row
        self.col = col
