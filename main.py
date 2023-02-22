from constAndStyle import *
from QuestGraph import *
from mapEditor import *
from generators import *
from pygame import *



def main():
    global mapLength,mapWidth
    squareSize = 50
    shift = [0,0]

    #test
    testqg = QuestGraph()
    config,visited = genHtCC(testqg)
    testqg.applyConfiguration(config,visited)
    #test

    vars = {
    "squareSize":squareSize,"shift":shift,
    "running":True,
    "testqg":testqg
    }

    pygame.init()
    window = pygame.display.set_mode((squareSize*(mapLength+8),squareSize*(mapWidth)))
    pygame.display.set_caption("Union Quest Creator")
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.QUIT])

    mainInterface.run(window,vars)



main()
