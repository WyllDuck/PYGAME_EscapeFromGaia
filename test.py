# Tools:
import networkx as nx
import matplotlib.pyplot as plt

# Configuration:
baseSize = (10, 10)

# Point / node:
class Point (object):
    def __init__ (self, row, col):
        self.row = row
        self.col = col

    def get_set (self):
        _set = set()
        _set.add(str(self.row) + ':row')
        _set.add(str(self.col) + ':col')
        return _set

    def get_coord (self):
        return (self.row, self.col)

    def __str__ (self):
        return '{}:{}'.format(self.row, self.col)


listPoints = [  Point(0,0),
                Point(0, baseSize[1] - 1),
                Point( baseSize[0] - 1, baseSize[1] - 1),
                Point( baseSize[0] - 1, 0),
                Point(5,0),
                Point(0,5),
                Point(5,5),
                Point(5,3),
                Point(9,3),
                Point(5,9)]

listConnections = [ (0, 5),
                    (5, 1),
                    (1, 9),
                    (9, 2),
                    (2, 8),
                    (8, 3),
                    (3, 4),
                    (4, 0),
                    (5, 6),
                    (6, 7),
                    (6, 9),
                    (8, 7),
                    (7, 4)]
A = nx.Graph()

def main ():
    global A
    for node_1, node_2 in listConnections:
        A.add_edge(listPoints[node_1], listPoints[node_2])

if __name__ == '__main__':
    main()
