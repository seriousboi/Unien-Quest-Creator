from constAndStyle import *
from QuestGraph import *
from random import seed,randrange, random



#heterogeneous connective constructive generator
def genHtCC(questGraph):
    global nbMaxDoors,nbRooms,nbHallways,nbRockConnectors,nbDoorConnectors
    config  = [False]*questGraph.nbConnectors

    startRoomIndex = randrange(nbRooms)
    currentArea = questGraph.areas[startRoomIndex]
    visited = [currentArea]

    nbPlacedDoors = 0
    while nbPlacedDoors < nbMaxDoors:

        weights = getWeightsHtCC(questGraph,currentArea,config,visited)
        choiceIndex = choiceFromWeights(weights)
        connector = currentArea.edges[choiceIndex]

        if connector.type == "Door" and config[connector.id] == False:
            nbPlacedDoors += 1
        config[connector.id] = True

        currentArea = connector.getOppositeVertex(currentArea)
        if currentArea not in visited:
            visited += [currentArea]

    #post processing
    removeUselessRocks(questGraph,config,visited)

    return config,visited



def getWeightsHtCC(questGraph,area,config,visited):
    weights = [1]*area.degree

    visitedPenalty = 0.2
    #reducing the probability of coming back to an area already visited
    for choiceIndex,connector in enumerate(area.edges):
        if connector.start in visited and connector.end in visited:
            weights[choiceIndex] = weights[choiceIndex]*visitedPenalty

    #preventing rooms from having more than one door leading to a hallway
    for choiceIndex,connector in enumerate(area.edges):

        #checking if using this connector would create a door between a room and a hallway
        if connector.start.type != connector.end.type and config[connector.id] == False:

            #checking if the room already has a door leading to a hallway
            if connector.start.type == "Room":
                room = connector.start
            elif connector.end.type == "Room":
                room = connector.end

            #we make en exception for the big central room, it can have 2 doors to hallways
            nbDoorsToHallways = getNbDoorsToHallways(questGraph,room,config)
            if nbDoorsToHallways >= 1 and room.id != 0:
                weights[choiceIndex] = 0
            elif nbDoorsToHallways >= 2 and room.id == 0:
                weights[choiceIndex] = 0

    normalize(weights)
    return weights


def removeUselessRocks(questGraph,config,visited):
    for index,connector in enumerate(questGraph.connectors):
        if connector.type == "Rock" and config[index] == False:
            connector.start
            connector.end
            if (connector.start not in visited) and (connector.end not in visited):
                config[index] = True


def choiceFromWeights(weights):
    rand = random()
    slice = 0
    for choiceIndex,weight in enumerate(weights):
        slice += weight
        if rand < slice:
            return choiceIndex



def normalize(weights):
    total = sum(weights)
    for index in range(len(weights)):
        weights[index] = weights[index]/total
    return weights



def getNbDoorsToHallways(questGraph,room,config):
    nbDoorsToHallways = 0
    for door in room.edges:
        neighborArea = door.getOppositeVertex(room)
        if (neighborArea.type == "Hallway") and config[door.id]:
            nbDoorsToHallways += 1
    return nbDoorsToHallways
