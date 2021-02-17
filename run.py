# Tools:
import random as rd

# Configuracion:
import conf

# Others:
from tile_gen import *
from room_gen import *
from graph_map import *
from planar_graph import get_faces
from map2D_gen import map_painter
from get_user_path import get_user_path_2

def run ( debugger = False, allow_obstacles = True ):

    P_Graph = PointGraph()
    P_Graph.create()

    try:
        connect = get_faces( P_Graph.P, True )
    except:
        P_Graph.printContent()
        raise ValueError ('A PointGraph() node isn\'t well writteen')

    # Format "connect" into "_connect" :
    # From : [[(7, 3), (3, 1, ... ],[ ... ]] --> To : [[ 7, 3, 1 ], [...]]
    _connect = list()
    for item in connect:
        item = [wall[0] for wall in item]
        _connect.append(item)

    R_Graph = RoomGraph()
    R_Graph.create(_connect)
    R_Graph.connectRooms()

    # Creating the numpy array "_map":
    _map = map_painter( P_Graph )

    # Change "_map" to take into account "doors":
    # Note: This info will be sent to "M_Graph" replacing "_map"
    doors = R_Graph.add_doors()
    _map_doors = _map.copy()
    for door in doors:
        _map_doors[door.row, door.col] = 0

    M_Graph = MapGraph()
    M_Graph.create( _map_doors )

    M_Graph, R_Graph, doors, _map, room_init, room_end = get_user_path_2 (M_Graph, R_Graph, _map, allow_obstacles)

    # This is a test:
    if debugger:
        path = M_Graph.find_path(room_init.center, room_end.center)

        P_Graph.printContent(False)
        R_Graph.printContent(False)
        M_Graph.printContent(False)
        M_Graph.printContentPath(path)

    return (P_Graph, R_Graph, M_Graph, doors, _map, room_init, room_end)
            # Points, Rooms, Map, doors, _map

# Test:
if __name__ == '__main__':
    run(True, True)
