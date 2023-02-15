from constAndStyle import *
from structures import *
from display import displayGraph



class Vertex():
    def __init__(self,id,edges,degree):
        self.id = id
        self.edges = edges
        self.degree = degree



class Edge():
    def __init__(self,id,start,end):
        self.id = id
        self.start = start
        self.end = end



class Area(Vertex):
    def __init__(self,id,edges,degree,type,center):
        super().__init__(id,edges,degree)
        self.type = type
        self.center = center



class Connector(Edge):
    def __init__(self,id,start,end,type,squares):
        super().__init__(id,start,end)
        self.type = type

        if type == "Rock":
            self.open = True
            self.squares = squares
        elif type == "Door":
            self.open = False
            self.frontSquare = squares[0]
            self.backSquare = squares[1]

    def flip(self):
        self.open = not self.open



class QuestGraph():
    def __init__(self):
        global nbRooms,nbHallways
        global rooms,hallways,rockConnectors,doorConnectors

        self.nbAreas = nbRooms + nbHallways
        self.nbConnectors = len(doorConnectors) + len(rockConnectors)

        areaIndex = 0
        self.areas = []
        for room in rooms:
            x = room["coordinates"][0]+room["coordinates"][2]/2
            y = room["coordinates"][1]+room["coordinates"][3]/2
            self.areas += [Area(areaIndex,[],0,"Room",(x,y))]
            areaIndex += 1
        for hallway in hallways:
            self.areas += [Area(areaIndex,[],0,"Hallway",hallway)]
            areaIndex += 1

        connectorIndex = 0
        self.connectors = []
        for doorConnector in doorConnectors:
            startId = doorConnector[0][0]
            endId = doorConnector[0][1]
            squares = []
            for coords in doorConnector[1]:
                squares += [Square(coords[0],coords[1])]
            connector = Connector(connectorIndex,startId,endId,"Door",squares)
            self.connectors += [connector]
            self.areas[startId].edges += [connector]
            self.areas[endId].edges += [connector]
            self.areas[startId].degree += 1
            self.areas[endId].degree += 1

            connectorIndex += 1
        for rockConnector in  rockConnectors:
            startId = rockConnector[0][0]
            endId = rockConnector[0][1]
            squares = []
            for coords in rockConnector[1]:
                squares += [Square(coords[0],coords[1])]
            connector = Connector(connectorIndex,startId,endId,"Rock",squares)
            self.connectors += [connector]
            self.areas[startId].edges += [connector]
            self.areas[endId].edges += [connector]
            self.areas[startId].degree += 1
            self.areas[endId].degree += 1

            connectorIndex += 1

    def display(self,surface,shift,squareSize):
        displayGraph(surface,shift,squareSize,self.nbAreas,self.nbConnectors,self.areas,self.connectors)
