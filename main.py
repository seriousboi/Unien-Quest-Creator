from constAndStyle import *
from QuestGraph import *
from mapEditor import *
from generatorInterface import *
from generators import *
from pygame import *



def main():
    global mapLength,mapWidth
    squareSize = 50
    shift = [0,0]

    pygame.init()
    window = pygame.display.set_mode((squareSize*(mapLength+8),squareSize*(mapWidth)))
    pygame.display.set_caption("Union Quest Creator")
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.QUIT])

    currentGraph = None
    currentMap = QuestMap()

    state = "inEditor"
    while state != "quitting":
        variables = {
        "squareSize":squareSize,"shift":shift,
        "currentGraph":currentGraph,"currentMap":currentMap,
        "window":window}

        if state == "inEditor":
            mainInterface.run(window,variables,state)
            state = variables["state"]
            currentGraph = variables["currentGraph"]
            currentMap = variables["currentMap"]
        elif state == "inGenerator":
            generatorInterface.run(window,variables,state)
            state = variables["state"]
            currentGraph = variables["currentGraph"]
            currentMap = variables["currentMap"]


    pygame.display.quit()



main()
