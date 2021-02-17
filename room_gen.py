# Tools:
import networkx as nx
import matplotlib.pyplot as plt
import uuid
import numpy as np

# Configuration:
import conf

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

            # Get door orientation:
            comun = wall_1.get_set() & wall_2.get_set()
            number_pos, orientation = comun.pop().split(':')
            del(comun)

            doors.append( DoorClass(new_row, new_col, orientation) )

        return doors

    # Get all obstacles of the map
    def get_obtacles(self, room_init, room_end, debugger = False ):
        data = list()
        for room in self.R.nodes():
            if room != room_init and room != room_end:
                add = room.add_obstacles(debugger)
                data += add

        return data


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

        self.size = (_max_row - _min_row) * (_max_col - _min_col)

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

    # Getting size internal space of the room:
    def get_size (self):
        row_1, col_1 = self.topleft.get_coord()
        row_2, col_2 = self.bottomright.get_coord()
        return (row_2 - row_1 - 1, col_2 - col_1 - 1)

    # Adding room obstacles
    def add_obstacles (self, debugger = False):

        data = list()
        count = 0

        _row, _col = self.get_size()
        prop = np.random.randint( *conf.percentage_boxes )
        left = int(_row * _col * prop / 100)

        # small
        matrix=np.zeros((_row - 2, _col - 2))
        # big
        _matrix=np.zeros((_row, _col))

        while True:
            count += 1

            row,col = np.where(matrix == 0)
            i = np.random.randint(len(row))
            row, col = (row[i], col[i])
            del(i)

            if left > 0:
                obstsize = np.random.randint(1,4)
            else:
                break

            # After 100 tries we will supose the program is having troubles adding obstacles
            if count >= 100:
                break

            if row + 1 + obstsize > _row - 1 or col + 1 + obstsize > _col - 1:
                continue

            candidate = _matrix[(row + 1) -1 : (row + 1) + obstsize + 1 , (col + 1) - 1 : (col + 1) + obstsize + 1] == 0
            candidate = candidate.tolist()

            """
            there will be 3 kinds of obstacles:
            1x1 (will be asigned as 3)
            2x2 (will be asigned as 4)
            3x3 (will be asigned as 5)
            """

            if verify(candidate):
                _matrix[(row + 1): (row + 1) + obstsize, (col + 1) : (col + 1) + obstsize] = obstsize + 2
                left -= (obstsize + 2) ** 2
                data.append(ObstacleClass((row + 2) + self.topleft.get_coord()[0], (col + 2) + self.topleft.get_coord()[1], obstsize))

            else:
                pass

            if left <= 0:
                break

        if debugger:
            print('\nROOM: {}\n'.format(self.topleft))
            print(_matrix)

        return data


####################################
#           DOOR and OBSTACLES
####################################

class DoorClass (object):
    def __init__ (self, row, col, orientation):
        self.row = row
        self.col = col
        self.orientation = orientation

    def get_coord (self):
        return (self.row, self.col)

class ObstacleClass (object):
    def __init__ (self, row, col, size):
        self.row = row
        self.col = col
        self.size = size


####################################
#           INTERN FUNCTION
####################################

def verify(candidate):
    for item in candidate:
        if all(item):
            continue
        else: return False
    return True
