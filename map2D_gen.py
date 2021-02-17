# Tools:
import numpy as np
import networkx as nx

# Configuration:
import conf

def map_painter(P_Graph):

	_map = np.zeros((conf.baseSize[0], conf.baseSize[1]))

	for node_1 in P_Graph.P:
		row_1 = node_1.row
		col_1 = node_1.col

		for node_2 in P_Graph.P.neighbors( node_1 ):
			row_2 = node_2.row
			col_2 = node_2.col

			# Vertical wall:
			if col_1 == col_2:
				if row_2 > row_1:
					_map[row_1 : row_2 + 1, col_1 : col_2 + 1] = 1

				else:
					_map[row_2 : row_1 + 1, col_1 : col_2 + 1] = 1

			# Horizontal wall:
			if row_1 == row_2:
				if col_2 > col_1:
					_map[row_1 : row_2 + 1, col_1 : col_2 + 1] = 1

				else:
					_map[row_1 : row_2 + 1, col_2 : col_1 + 1] = 1

	return _map
