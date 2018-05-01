# Tools:
from math import pi, atan
import itertools
import numpy as np

# Configuration:
from conf import debugger_planar


# Note: 'coord' variable adjust result to just return the simple cycles of the graph. In other words to eliminate the external face.
def Faces(edges,embedding, coord = None):
    """
    edges: is an undirected graph as a set of undirected edges
    embedding: is a combinatorial embedding dictionary. Format: v1:[v2,v3], v2:[v1], v3:[v1] clockwise ordering of neighbors at each vertex.)

    >>> edges = [(1, 2), (1, 2), (2, 3), (2, 4), (3, 5), (3, 7), (4, 6), (4, 9), (5, 6), (6, 8), (7, 8), (8, 11), (9, 10), (10, 11)]
    >>> emb = {1: [2, 3], 2: [4, 3, 1], 3: [1, 2, 5, 7], 4: [9, 6, 2], 5: [3, 6], 6: [8, 5, 4], 7: [3, 8], 8: [6, 11, 7], 9: [4, 10], 10: [9, 11], 11: [10, 8]}
    >>> f = Faces(edges, emb)
    >>> f
    [[(7, 3), (3, 1), (1, 2), (2, 4), (4, 9), (9, 10), (10, 11), (11, 8), (8, 7)], [(3, 2), (2, 1), (1, 3)], [(6, 4), (4, 2), (2, 3), (3, 5), (5, 6)], [(8, 11), (11, 10), (10, 9), (9, 4), (4, 6), (6, 8)], [(3, 7), (7, 8), (8, 6), (6, 5), (5, 3)]]

    """
    # Establish set of possible edges
    edgeset = set()
    for edge in edges: # edges is an undirected graph as a set of undirected edges
        edge = list(edge)
        edgeset |= set([(edge[0],edge[1]),(edge[1],edge[0])])

    # Storage for face paths
    faces = []
    path  = []
    for edge in edgeset:
        path.append(edge)
        edgeset -= set([edge])
        break  # (Only one iteration)

    # Trace faces
    while (len(edgeset) > 0):
        neighbors = embedding[path[-1][-1]]
        next_node = neighbors[(neighbors.index(path[-1][-2])+1)%(len(neighbors))]
        tup = (path[-1][-1],next_node)
        if tup == path[0]:
            faces.append(path)
            path = []
            for edge in edgeset:
                path.append(edge)
                edgeset -= set([edge])
                break  # (Only one iteration)
        else:
            path.append(tup)
            edgeset -= set([tup])
    if (len(path) != 0): faces.append(path)


    # Note: 'coord' variable adjust result to just return the simple cycles of the graph. In other words to eliminate the external face.
    if coord:
        for i in range(len(faces)):
            if es_cara_exterior(faces[i], coord.keys(), coord):
                del(faces[i])
                break

    # Debugger:
    if debugger_planar:
        count = 1
        for cycle in faces:
            print('CYCLE_{}:\n'.format(count))
            for node_1, node_2 in cycle:
                print('({}) --> ({})'.format(str(node_1), str(node_2)))

            count += 1
            print('\n\nNEXT_CYCLE\n')

    return faces


def get_coord ( graph ):
    coord = dict()
    for node in graph:
        coord[node] = node.get_coord()
    return coord


# Note: 'simple_cycles' variable adjust result to just return the simple cycles of the graph. In other words to eliminate the external face.
def get_faces( graph, simple_cycles = False ):
    """

        >>> f = get_faces( networkx.Graph() )
        internal step: embedding = combinatorial_embedding( graph )
        >>> embedding = {1: [2, 3], 2: [4, 3, 1], 3: [1, 2, 5, 7], 4: [9, 6, 2], 5: [3, 6], 6: [8, 5, 4], 7: [3, 8], 8: [6, 11, 7], 9: [4, 10], 10: [9, 11], 11: [10, 8]}
        >>> f
        [[(7, 3), (3, 1), (1, 2), (2, 4), (4, 9), (9, 10), (10, 11), (11, 8), (8, 7)], [(3, 2), (2, 1), (1, 3)], [(6, 4), (4, 2), (2, 3), (3, 5), (5, 6)], [(8, 11), (11, 10), (10, 9), (9, 4), (4, 6), (6, 8)], [(3, 7), (7, 8), (8, 6), (6, 5), (5, 3)]]

    """

    # Getting combinatorial embedinng from our "Planar Graph" from NetworkX
    embedding = combinatorial_embedding( graph )

    edges = []
    for node in embedding:
        adjacent = [(node, neighbor) for neighbor in embedding[node]]
        edges.extend(adjacent)

    # Should I detect the external cycle?
    # Yes
    if simple_cycles:
        coord = get_coord( graph )
        return Faces(edges, embedding, coord)

    # No
    else:
        return Faces(edges, embedding)


def es_cara_exterior(cara, vertexs, coordenades):
    """
    cara        llista dels vèrtexs de la cara.
    coordenades diccionari (vèrtex, coordenades).

    >>> coords = {1: (0, 3), 2: (1, 3), 4: (3, 3), 6: (3, 2), 5: (2, 2), 3: (1, 2)}
    >>> cara = [(3, 2), (2, 1), (1, 3)]
    >>> es_cara_exterior(cara, coords.keys(), coords)
    False
    >>> cara = [(6, 4), (4, 2), (2, 3), (3, 5), (5, 6)]
    >>> es_cara_exterior(cara, coords.keys(), coords)
    False
    >>> cara = [(1, 2), (2, 4), (4, 6), (6, 5), (5, 3), (3, 1)]
    >>> es_cara_exterior(cara, coords.keys(), coords)
    True

    """
    trobat = False
    for aresta in cara:
        triangles = [(coordenades[aresta[0]], coordenades[aresta[1]], coordenades[v]) for v in vertexs if v not in aresta]
        arees = [area_triangle(*t) for t in triangles]
        arees_pos = [a for a in arees if a != 0]
        signes = [signe(arees_pos[0]) != signe(a) for a in arees_pos]
        # Tots els punts que no estan alineats estan al mateix semiespai
        trobat = any(signes)
        if trobat:
            break
    return not trobat


def area_triangle(v0, v1, v2):
    """Retorna l'àrea amb signe del triangle

    >>> area_triangle((0, 0), (1, 0), (1, 1))
    0.5
    >>> area_triangle((0, 0), (1, 1), (1, 0))
    -0.5
    """
    mat = np.array([[v0[0], v1[0], v2[0]], [v0[1], v1[1], v2[1]], [1, 1, 1]])
    det = np.linalg.det(mat)
    return det / 2


def signe(v):
    if v < 0:
        s = -1
    elif v > 0:
        s = 1
    else:
        s = 0
    return s


def combinatorial_embedding ( G ):

    """
    combinatorial_embedding: is a combinatorial embedding dictionary. Format: v1:[v2,v3], v2:[v1], v3:[v1] clockwise ordering of neighbors at each vertex.)
    """

    comb = dict()
    for node in G:
        angles = list((get_angle(node, item)[0], item) for item in G.neighbors( node ))

        # Debugger:
        if debugger_planar:
            print('comb_embedding node: {}\n'.format(str(node)))
            for item in angles:
                print('angles: {} / node: {} / id: {}'.format(item[0], str(item[1]), item[1]._id))

            print('\n\nNEXT_NODE\n')

        # Note: .sort() and .reverse() orders node in clockwise order
        angles.sort()
        angles.reverse()

        # Note: We are keeping only de nodes in clockwise order
        angles = [item for key, item in angles]

        comb[node] = angles

    return comb


def get_angle (node_1, node_2):
    # Lenght of triangle sides:
    opp = ( node_2.row - node_1.row )
    adj = ( node_2.col - node_1.col )

    # Handle indeterminations of "tan" function:
    try:
        angle = atan( abs( opp / adj ) )

        # left / bottom:
        if adj < 0 and opp >= 0:
            angle = angle + pi

        # right / bottom:
        elif adj > 0 and opp >= 0:
            angle = abs(angle - pi/2) + 1.5 * pi

        # left / top:
        elif adj < 0 and opp < 0:
            angle = abs(angle - pi/2) + 0.5 * pi

        # right / top:
        elif adj > 0 and opp < 0:
            pass

    except:
        if adj == 0 and opp >= 0:
            angle = pi * 1.5
        elif adj == 0 and opp < 0:
            angle = pi * .5

    return (angle * (360/(2*pi)), angle)
