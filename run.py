# Configuracion:
import conf

# Others:
from tile_gen import *
from room_gen import *
from planar_graph import get_faces

def run ( debugger = False ):

    P_Graph = PointGraph()
    P_Graph.create()

    try:
        connect = get_faces( P_Graph.P, True )
    except:
        P_Graph.printContent()
        raise ValueError ('A PointGraph() node isn\'t well writteen')

    P_Graph.printContent(False)

    # Format "connect" into "_connect" :
    # From : [[(7, 3), (3, 1, ... ],[ ... ]] --> To : [[ 7, 3, 1 ], [...]]
    _connect = list()
    for item in connect:
        item = [wall[0] for wall in item]
        _connect.append(item)

    R_Graph = RoomGraph()
    R_Graph.create(_connect)
    R_Graph.connectRooms()

    R_Graph.printContent()

    doors = R_Graph.add_doors()

    return (P_Graph, R_Graph, doors)
            # Points, Rooms

# Test:
if __name__ == '__main__':
    run( True )
