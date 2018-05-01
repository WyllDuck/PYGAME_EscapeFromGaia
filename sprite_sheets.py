"""Funcions per crear llistes o matrius d'imatges a partir d'un sprite
sheet.

"""

import pygame


def crea_llista_imatges(spritesheet, nims):
    """Retorna una llista de subsurfaces obtinguda a partir de l'sprite
    sheet de `nims` imatges.

    """
    mides = ( spritesheet.get_width() // nims,
              spritesheet.get_height() )
    llista = []
    for columna in range(nims):
        tros = pygame.Rect( (mides[0] * columna, 0), mides )
        llista.append(spritesheet.subsurface(tros))
    return llista


def crea_matriu_imatges(spritesheet, nfils, ncols):
    """Retorna una matriu de subsurfaces obtinguda a partir de l'sprite
    sheet de `nfils`x`ncols` imatges.

    """
    mides = ( spritesheet.get_width() // ncols,
              spritesheet.get_height() // nfils )
    matriu = [[] for i in range(nfils)]
    for fila in range(nfils):
        for columna in range(ncols):
            tros = pygame.Rect( (mides[0] * columna, mides[1] * fila), mides )
            matriu[fila].append(spritesheet.subsurface(tros))
    return matriu
