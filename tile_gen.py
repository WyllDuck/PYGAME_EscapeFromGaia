# Tools:
import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import uuid
import pprint as pp

# Configuration:
import conf

####################################
#           POINT GRAPH
####################################

# Base Graph:
class PointGraph (object):
    def __init__ (self):
        self.P = nx.Graph()

    # Adding nodes in the graph AND connections between nodes:
    # ( nodes <=> class Point )
    def create (self):
        self.P = add_random_nodes()

    # Print graph:
    def printContent (self, show = True):
        pos = dict([(item, (item.row, item.col)) for item in self.P])
        nx.draw(self.P, pos, with_labels = True)
        if show:
            plt.show()


# Base Node:
class Point (object):
    def __init__ (self, row, col):
        self.row = row
        self.col = col
        self._id = uuid.uuid4()

    def get_set (self):
        _set = set()
        _set.add(str(self.row) + ':row')
        _set.add(str(self.col) + ':col')
        return _set

    def get_coord (self):
        return (self.row, self.col)

    def __str__ (self):
        return '{}:{}'.format(self.row, self.col)


####################################
#           RUN
####################################

def add_random_nodes ():

    P = nx.Graph()

    # Add INIT Points / nodes:
    listPoints = [  Point(0,0),
                    Point(0, conf.baseSize[1] - 1),
                    Point( conf.baseSize[0] - 1, conf.baseSize[1] - 1),
                    Point( conf.baseSize[0] - 1, 0)]

    listConnections = [ (0, 1),
                        (0, 3),
                        (2, 1),
                        (2, 3)]

    for connect in listConnections:
        P.add_edge(listPoints[connect[0]], listPoints[connect[1]])

    del(listPoints)
    del(listConnections)

    # Add random Points / nodes:
    counter = 1

    while conf.room_number > counter:

        # Select Points / nodes:
        random_node_1 = rd.choice(list(P.nodes()))
        random_node_2 = rd.choice(list(P.neighbors(random_node_1)))

        comun = random_node_1.get_set() & random_node_2.get_set()
        number_pos, type_pos = comun.pop().split(':')
        del(comun)

        # Debugger
        if conf.debugger:
            print('random_node_1: {}'.format(random_node_1))
            print('random_node_2: {}'.format(random_node_2))
            print('number_pos: {}'.format(number_pos))
            print('type_pos: {}'.format(type_pos))

        # Chose new Point / node:
        # Creating a new HORIZONTAL wall:
        if type_pos == 'col' and abs(random_node_1.row - random_node_2.row) > 2 * conf.border_limit:
            try:
                new_row = rd.randrange(random_node_1.row + conf.border_limit, random_node_2.row - conf.border_limit + 1)
            except:
                new_row = rd.randrange(random_node_2.row + conf.border_limit, random_node_1.row - conf.border_limit + 1)
            new_point_1 = Point(int(new_row), int(number_pos))

            # Find the TWO walls you can collide with and select ONE:
            collider = detect_collision(P, new_point_1, type_pos)
            collider_wall = rd.choice(collider)

            # Verifying that intersection points pass "border_limit" test:
            _max = max(point.row for point in collider_wall)
            _min = min(point.row for point in collider_wall)

            if _min + conf.border_limit < new_row and new_row < _max - conf.border_limit:
                # Create new_point_2:
                new_point_2 = Point(int(new_row), int(collider_wall[0].col))

            else:
                # Note: If there's only ONE wall program will crash
                if len(collider) > 1:
                    collider.remove(collider_wall)
                    collider_wall = rd.choice(collider)

                    # Verifying that intersection points pass "border_limit" test:
                    _max = max(point.row for point in collider_wall)
                    _min = min(point.row for point in collider_wall)

                    if _min + conf.border_limit < new_row and new_row < _max - conf.border_limit:
                        # Create new_point_2:
                        new_point_2 = Point(int(new_row), int(collider_wall[0].col))

                    else:
                        continue

                else:
                    continue

        # Creating a new VERTICAL wall:
        elif type_pos == 'row' and abs(random_node_1.col - random_node_2.col) > 2 * conf.border_limit:
            try:
                new_col = rd.randrange(random_node_1.col + conf.border_limit, random_node_2.col - conf.border_limit + 1)
            except:
                new_col = rd.randrange(random_node_2.col + conf.border_limit, random_node_1.col - conf.border_limit + 1)
            new_point_1 = Point(int(number_pos), int(new_col))

           # Find the TWO walls you can collide with and select ONE:
            collider = detect_collision(P, new_point_1, type_pos)
            collider_wall = rd.choice(collider)

            # Verifying that intersection points pass "border_limit" test:
            _max = max(point.col for point in collider_wall)
            _min = min(point.col for point in collider_wall)

            if _min + conf.border_limit < new_col and new_col < _max - conf.border_limit:
                # Create new_point_2:
                new_point_2 = Point(int(collider_wall[0].row), int(new_col))

            else:
                # Note: If there's only ONE wall program will crash
                if len(collider) > 1:
                    collider.remove(collider_wall)
                    collider_wall = rd.choice(collider)

                    # Verifying that intersection points pass "border_limit" test:
                    _max = max(point.col for point in collider_wall)
                    _min = min(point.col for point in collider_wall)

                    if _min + conf.border_limit < new_col and new_col < _max - conf.border_limit:
                        # Create new_point_2:
                        new_point_2 = Point(int(collider_wall[0].row), int(new_col))

                    else:
                        continue

                else:
                    continue

        else:
            continue

        # Add new connections new_point_1:
        P.remove_edge(random_node_1, random_node_2)
        P.add_edge(random_node_1, new_point_1)
        P.add_edge(random_node_2, new_point_1)

        # Debugger
        if conf.debugger:
            print('new_point_2: {}'.format(new_point_2))
            print('collider:')
            pp.pprint(collider)
            print('\n')

        # Add new connections collider_wall:
        if len(collider_wall) == 3:
            # We replace 'new_point_2' by it's equivalent from the 'collider_wall' list:
            for item in collider_wall:
                 if len(item.get_set() & new_point_2.get_set()) == 2:
                     collider_wall.remove(item)
                     new_point_2 = item
                     break

            P.add_edge(new_point_1, new_point_2)

            for item in collider_wall:
                P.add_edge(item, new_point_2)

        elif len(collider_wall) == 2:
            P.remove_edge(collider_wall[0], collider_wall[1])
            P.add_edge(new_point_1, new_point_2)
            for item in collider_wall:
                P.add_edge(item, new_point_2)

        # Add to counter the new room:
        counter += 1

        # Debugger PRO:
        if conf.debugger_pro:
            nx.draw(P, with_labels=True)
            plt.show()

    return P


def detect_collision (P, point, type_pos_point):

    # Debugger
    if conf.debugger:
        print('_______________ENTER________________')

    C = nx.Graph()
    for node_1 in P:
        for node_2 in P.neighbors(node_1):

            # Find all vertical wall or horizontal walls of P
            comun = node_1.get_set() & node_2.get_set()
            number_pos, type_pos = comun.pop().split(':')
            del(comun)
            del(number_pos)

            # Vertical wall:
            if type_pos_point == type_pos and type_pos == 'col':
                if point.row > node_1.row and point.row < node_2.row:
                    C.add_edge(node_1, node_2)
                elif point.row < node_1.row and point.row > node_2.row:
                    C.add_edge(node_1, node_2)
                elif point.row == node_1.row and point.row > node_2.row:
                    C.add_edge(node_1, node_2)
                elif point.row == node_1.row and point.row < node_2.row:
                    C.add_edge(node_1, node_2)
                elif point.row < node_1.row and point.row == node_2.row:
                    C.add_edge(node_1, node_2)
                elif point.row > node_1.row and point.row == node_2.row:
                    C.add_edge(node_1, node_2)
                else:
                    continue

            # Horizontal wall:
            elif type_pos_point == type_pos and type_pos == 'row':
                if point.col > node_1.col and point.col < node_2.col:
                    C.add_edge(node_1, node_2)
                elif point.col < node_1.col and point.col > node_2.col:
                    C.add_edge(node_1, node_2)
                elif point.col == node_1.col and point.col > node_2.col:
                    C.add_edge(node_1, node_2)
                elif point.col == node_1.col and point.col < node_2.col:
                    C.add_edge(node_1, node_2)
                elif point.col < node_1.col and point.col == node_2.col:
                    C.add_edge(node_1, node_2)
                elif point.col > node_1.col and point.col == node_2.col:
                    C.add_edge(node_1, node_2)
                else:
                    continue

    # Debugger
    if conf.debugger:
        print('new_point_1: {}'.format(point))
        if conf.debugger_pro:
            nx.draw(C, with_labels=True)
            plt.show()

    # Find the nearest walls you can collide with:
    # Vertical wall:
    if type_pos_point == 'col':

        # Tabulate wall by proximity:
        dict_point = dict()
        for node in C:
            new_index = node.col - point.col
            if new_index in dict_point:
                dict_point[new_index].append(node)
            else:
                dict_point[new_index] = [node]

        # Debugger
        if conf.debugger:
            print('dict_point:')
            pp.pprint(dict_point)
            print('\n')

        # Eliminate the wall where 'point' is located:
        del(dict_point[0])

        # Nearest wall right:
        try:
            index_1 = min(key for key, item in dict_point.items() if key > 0)
        # If there is'nt any wall:
        except:
            index_1 = None

        # Nearest wall left:
        try:
            index_2 = max(key for key, item in dict_point.items() if key < 0)
        # If there is'nt any wall:
        except:
            index_2 = None

        # Return list of points to "play" with:
        # RIGHT / LEFT
        if not index_1: return [dict_point[index_2]]
        elif not index_2: return [dict_point[index_1]]
        else: return [dict_point[index_1], dict_point[index_2]]


    # Horizontal wall:
    else:

        # Tabulate wall by proximity:
        dict_point = dict()
        for node in C:
            new_index = node.row - point.row
            if new_index in dict_point:
                dict_point[new_index].append(node)
            else:
                dict_point[new_index] = [node]

        # Eliminate the wall where 'point' is located:
        del(dict_point[0])

        # Debugger
        if conf.debugger:
            print('dict_point:')
            pp.pprint(dict_point)
            print('\n')

        # Nearest wall up:
        try:
            index_1 = max(key for key, item in dict_point.items() if key < 0)
        # If there is'nt any wall:
        except:
            index_1 = None

        # Nearest wall down:
        try:
            index_2 = min(key for key, item in dict_point.items() if key > 0)
        # If there is'nt any wall:
        except:
            index_2 = None

        # Return list of points to "play" with:
        # UP / DOWN
        if not index_1: return [dict_point[index_2]]
        elif not index_2: return [dict_point[index_1]]
        else: return [dict_point[index_1], dict_point[index_2]]


if __name__ == '__main__':
    P_Graph = PointGraph()
    P_Graph.create()
    P_Graph.printContent()
