from constAndStyle import *
from QuestGraph import *
from random import randrange



#heterogeneous connective constructive generator
def genHtCC(questGraph):
    global nbMaxDoors,nbRooms,nbHallways,nbRockConnectors,nbDoorConnectors
    config  = [False]*questGraph.nbConnectors

    startRoomIndex = randrange(nbRooms)
    currentArea = questGraph.areas[startRoomIndex]

    nbPlacedDoors = 0
    while nbPlacedDoors < nbMaxDoors:

        move = randrange(currentArea.degree)
        connector = currentArea.edges[move]

        if connector.type == "Door" and config[connector.id] == False:
            nbPlacedDoors += 1
        config[connector.id] = True

        currentArea = connector.getOppositeVertex(currentArea)

    return config
