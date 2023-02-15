from constAndStyle import *
from interface import *
from pygame import *



def main():
    global mapLength,mapWidth
    squareSize = 50
    shift = [0,0]

    vars = {
    "squareSize":squareSize,"shift":shift,
    "running":True}

    pygame.init()
    window = pygame.display.set_mode((squareSize*(mapLength+8),squareSize*(mapWidth)))
    pygame.display.set_caption("Union Quest Creator")
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.QUIT])

    mainInterface.run(window,vars)



main()
