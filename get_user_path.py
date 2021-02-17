# Tools:
import networkx as nx
import random as rd
import numpy as np

# Configuration:
import conf

# Others:
from graph_map import *

"""
This function has as objective to get the user path through the level.
The only condition is that this path needs to be as long as possible.
"""
def get_user_path_1 (M_Graph, R_Graph, doors):

    no_prescindible_doors = set()

    # Transform ""doors"" raw data into usefull data:
    doors = [door.get_coord() for door in doors]

    # Filter rooms that can potentially be a ""room_init"" and a ""room end"":
    rooms = [room.center for room in R_Graph.R.nodes() if room.size <= conf.room_path_size]

    # Select rooms:
    room_init = rd.choice(rooms)
    rooms.remove(room_init)
    room_end = rd.choice(rooms)

    while True:

        # Get shortest path from ""M_Graph"":
        path = M_Graph.find_path(room_init, room_end)

        # Get all doors involved in the path:
        doors_involved = [tile.get_coord() for tile in path if tile.get_coord() in doors]

        # Get the first door that can be eliminated without compromising the integrity of ""M_graph""
        for door in doors_involved:
            if door not in no_prescindible_doors:
                current_door = door
                break

        # If we haven't found a prescindible door
        else:
            M_Graph.printContent(False)
            M_Graph.printContentPath(path)
            return doors

        # Verify if ""M_Graph"" is one component:
        M = M_Graph.M.copy()
        M.remove_node(M_Graph._map_list[current_door[0]][current_door[1]])
        if nx.number_connected_components(M) != 1:
            no_prescindible_doors.add(current_door)

        # If the nummber of components is still 1 continue normal procedure:
        else:
            # Update ""M_Graph"" for next iteration:
            M_Graph.M.remove_node(M_Graph._map_list[current_door[0]][current_door[1]])

        del(M)


"""
This method of solving the same problem as above uses ""R_Graph"" instead of ""M_Graph""
Note: After some iteration this method has shown to be more succesfull
"""
def get_user_path_2 (M_Graph, R_Graph, _map, allow_obstacles):

    # Filter rooms that can potentially be a ""room_init"" and a ""room end"":
    rooms = [room for room in R_Graph.R.nodes() if room.size <= conf.room_path_size]

    # Select rooms:
    room_init = rd.choice(rooms)
    rooms.remove(room_init)
    room_end = rd.choice(rooms)

    # Add weight to ""R_Graph"":
    for room_1, room_2 in R_Graph.R.edges():
        weight = len(M_Graph.find_path(room_1.center, room_2.center))
        R_Graph.R.add_edge(room_1, room_2, weight = weight)

    paths = nx.all_simple_paths(R_Graph.R, room_init, room_end)

    # Classify all paths:
    classify_paths = dict()
    for path in paths:
        total_weight = 0
        for i in range(len(path) - 1):
            total_weight += R_Graph.R[path[i]][path[i+1]]['weight']

        # Appending values:
        if total_weight not in classify_paths:
            classify_paths[total_weight] = [path]
        else:
            classify_paths[total_weight].append(path)


    # Update ""R_Graph"":
    route = max(classify_paths.keys())
    route = classify_paths[route][0]


    # Create the ""new_Graph"" to update ""R_Graph""
    new_Graph = nx.Graph()
    for i in range(len(route) - 1):
        new_Graph.add_edge(route[i], route[i + 1], points = R_Graph.R[route[i]][route[i + 1]]['points'])

    # Get ""room"" nodes from ""R_Graph"" that have not been included in the final ""route"" _map_list
    other_rooms = [room for room in R_Graph.R.nodes() if room not in route]
    for room in other_rooms:
        for nei in R_Graph.R.neighbors(room):
            if nei != room_init and nei != room_end:
                new_Graph.add_edge(room, nei, points = R_Graph.R[room][nei]['points'])
                break

    R_Graph.R = new_Graph


    # Updating ""_map"":
    #    Adding obstacles to "_map_complete_without_doors":
    _map_complete_without_doors = _map.copy()

    if allow_obstacles:
        obstacles = R_Graph.get_obtacles( room_init, room_end )
        for obstacle in obstacles:

            """
            Equilant in numpy ""_map""
            2 --> stainless_box OR rusted_box
            3 --> lamp
            4 --> eyeBox
            5 --> pipeline
            """

            # If the size of the obstacle is 1 the obstacle can be: A lamp, a rusted box or a stainless box
            if obstacle.size == 1:
                value = np.random.choice(np.arange(2, 5), p=[0.40, 0.45, 0.15])
                _map_complete_without_doors[obstacle.row: obstacle.row + obstacle.size, obstacle.col: obstacle.col + obstacle.size] = value

            # If the size of the obstacle is 2 or greater the obstacle can be: a rusted box or a stainless box
            elif obstacle.size == 2:
                for i in range(obstacle.size):
                    for x in range(obstacle.size):
                        value = np.random.choice((2, 3, 4), p=[0.70, 0.20, 0.10])
                        _map_complete_without_doors[obstacle.row + i, obstacle.col + x] = value

            # If the size of the obstacle is 3 or greater the obstacle can be: a pipeline
            elif obstacle.size == 3:
                if np.random.choice(np.arange(0, 2), p=[0.65, 0.35]) == 0:
                    _map_complete_without_doors[obstacle.row: obstacle.row + obstacle.size, obstacle.col: obstacle.col + obstacle.size] = 10
                    _map_complete_without_doors[obstacle.row + 1, obstacle.col + 1] = 5

                else:
                    for i in range(obstacle.size):
                        for x in range(obstacle.size):
                            value = np.random.choice((2, 3, 4), p=[0.75, 0.10, 0.15])
                            _map_complete_without_doors[obstacle.row + i, obstacle.col + x] = value

    # Add init and end plataform:
    for room in [room_init, room_end]:
        _map_complete_without_doors[room.center[0] - 1: room.center[0] + 2, room.center[1] - 1: room.center[1] + 2] = 10
        _map_complete_without_doors[room.center[0] - 1: room.center[0] + 2, room.center[1]] = 0
        _map_complete_without_doors[room.center[0], room.center[1] - 1: room.center[1] + 2] = 0



    #    Adding final door to ""_map_complete""
    doors = R_Graph.add_doors()
    _map_complete = _map_complete_without_doors.copy()
    for door in doors:
        _map_complete[door.row, door.col] = 0

    M_Graph = MapGraph()
    M_Graph.create( _map_complete )

    # Add init and end plataform:
    for room in [room_init, room_end]:
        _map_complete_without_doors[room.center[0], room.center[1]] = -1

    return M_Graph, R_Graph, doors, _map_complete_without_doors, room_init, room_end
