# Configuration:
import conf

def type_detector ( pos, _map ):

    row, col = pos

####################################
#           EDGES
####################################

    if row == 0 and col == 0:
        
        # 
        #   X X
        #   X 0
        
        return 15

    elif row == 0 and col == conf.baseSize[1] - 1:

        # 
        # X X 
        # 0 X 

        return 16

    elif row == conf.baseSize[0] - 1 and col == conf.baseSize[1] - 1:

        # 0 X
        # X X 
        # 

        return 17

    elif row == conf.baseSize[0] - 1 and col == 0:

        #   X 0
        #   X X
        #  

        return 18



####################################
#           EXTERNAL WALL
####################################

    # Horizontal Wall Top
    if row == 0 and col != 0 and col != conf.baseSize[1] - 1:
        if _map[ row , col + 1] and _map[ row , col - 1] and _map[row + 1, col]:
            
            # 
            # X X X
            # 0 X 0

            return 7
        
        elif _map[ row , col + 1] and _map[ row , col - 1]:

            # 
            # X X X
            # 0 0 0

            return 8


    # Vertical Wall Left
    elif col == 0 and row != 0 and row != conf.baseSize[0] - 1:
        if _map[ row + 1 , col] and _map[ row - 1 , col] and _map[row, col + 1]:
            
            #   X 0
            #   X X
            #   X 0

            return 9
        
        elif _map[ row + 1 , col] and _map[ row - 1 , col]:

            #   X 0
            #   X 0
            #   X 0

            return 10

    # Horizontal Wall Bottom
    elif row == conf.baseSize[0] - 1 and col != 0 and col !=  conf.baseSize[1] - 1:
        if _map[ row , col + 1] and _map[ row , col - 1] and _map[row - 1, col]:
            
            # 0 X 0
            # X X X
            # 

            return 11
        
        if _map[ row , col + 1] and _map[ row , col - 1]:

            # 0 0 0
            # X X X
            # 

            return 12

    # Vertical Wall Right
    elif col == conf.baseSize[1] - 1 and row != 0 and row != conf.baseSize[0] - 1:
        if _map[ row + 1 , col] and _map[ row - 1 , col] and _map[row, col - 1]:
            
            # 0 X 
            # X X 
            # 0 X 

            return 13
        
        elif _map[ row + 1 , col] and _map[ row - 1 , col]:

            # 0 X 
            # 0 X 
            # 0 X 

            return 14


####################################
#           INTERNAL WALL
####################################

    # We draw the wall:
    elif _map[ row + 1, col ] and _map[ row - 1, col ]:
        if _map[ row , col + 1] and _map[ row , col - 1]:

            # 0 X 0
            # X X X
            # 0 X 0

            return 0

        elif _map[ row , col + 1]:

            # 0 X 0
            # 0 X X
            # 0 X 0

            return 1

        elif _map[ row , col - 1]:

            # 0 X 0
            # X X 0
            # 0 X 0

            return 2

        else:

            # 0 X 0
            # 0 X 0
            # 0 X 0

            return 3
    elif _map[ row, col + 1] and _map[ row, col - 1]:
        if _map[ row + 1, col ] == 1:
        
            # 0 0 0
            # X X X
            # 0 X 0

            return 4
            
        elif _map[ row - 1, col ] == 1:

            # 0 X 0
            # X X X
            # 0 0 0
            
            return 5
            
        else:

            # 0 0 0
            # X X X
            # 0 0 0
            
            return 6