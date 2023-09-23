from Square import *
from Entity import *
from MapItems import *
from display import *
import json



class QuestMap:
    def __init__(self,doors=[],rocks=[],entities=[],aggregatedRooms=[],informations=[]):
        self.doors = doors
        self.rocks = rocks
        self.entities = entities
        self.informations = informations
        self.aggregatedRooms = aggregatedRooms
        self.rooms = getRoomsAfterAggregation(aggregatedRooms)


    @classmethod
    def loadFile(cls,fileName=None):
        if fileName == None:
            fileName = "current"
        file = open("data/maps/"+fileName+".json","r")
        jsonstr = file.read()
        file.close()

        return cls.fromDict(json.loads(jsonstr))

    @classmethod
    def fromDict(cls,dict):
        doors = []
        for door in dict["doors"]:
            doors += [Door.fromDict(door)]
        rocks = []
        for rock in dict["rocks"]:
            rocks += [Rock.fromDict(rock)]
        entities = []
        for entity in dict["entities"]:
            entities += [Entity.fromDict(entity)]
        aggregatedRooms = []
        for aggregatedRoom in dict["aggregatedRooms"]:
            aggregatedRooms += [listToTupleRec(aggregatedRoom)]
        informations = []
        for infos in dict["informations"]:
            informations += [Informations.fromDict(infos)]
        return cls(doors,rocks,entities,aggregatedRooms,informations)

    def toJSON(self):
        doors = []
        for door in self.doors:
            doors += [door.toJSON()]
        rocks = []
        for rock in self.rocks:
            rocks += [rock.toJSON()]
        entities = []
        for entity in self.entities:
            entities += [entity.toJSON()]
        informations = []
        for infos in self.informations:
            informations += [infos.toJSON()]
        return {"doors":doors,"rocks":rocks,"entities":entities,"aggregatedRooms":self.aggregatedRooms,"informations":informations}

    def saveToFile(self,fileName = None):
        if fileName == None:
            fileName = "current"
        file = open("data/maps/"+fileName+".json","w")
        file.writelines([json.dumps(self.toJSON(),indent=2)])
        file.close()

    def loadGraph(self,questGraph):
        self.doors = []
        self.rocks = []
        self.entities = []
        self.informations = []
        for connector in questGraph.connectors:
            if connector.type == "Rock" and connector.open == False:
                for square in connector.squares:
                    self.rocks += [Rock(square)]
            if connector.type == "Door" and connector.open == True:
                self.doors += [Door(connector.frontSquare,connector.backSquare)]

        self.aggregatedRooms = []
        self.rooms = getRoomsAfterAggregation(self.aggregatedRooms)

    def fuseRooms(self,room1,room2):
        newRoom = roomDicToTuple(aggregateRooms(tupleToRoomDic(room1),tupleToRoomDic(room2)))
        self.rooms += [newRoom]
        self.rooms.remove(room1)
        self.rooms.remove(room2)
        self.aggregatedRooms += [[room1,room2]]

    def clearAggregatedRooms(self):
        self.aggregatedRooms = []
        self.rooms = getRooms()

    def display(self,surface,shift,squareSize):
        displayBoard(surface,shift,squareSize,self.rooms)
        for rock in self.rocks:
            rock.display(surface,shift,squareSize)
        for door in self.doors:
            door.display(surface,shift,squareSize)
        for index,entity in enumerate(self.entities):
            entity.display(surface,shift,squareSize,index)
        for index,infos in enumerate(self.informations):
            infos.display(surface,shift,squareSize,index)

    def itemAt(self,square):
        for item in self.rocks+self.entities+self.informations:
            if item.square.equal(square):
                return item
        return None

    def removeItemAT(self,item,square):

        for itemsList in [self.rocks,self.entities,self.informations]:
            if item in itemsList:
                itemsList.remove(item)
                return
        print("could not find item to remove, bruh")


    def doorAt(self,frontSquare,backSquare): #retourne la porte entre frontSquare et backSquare, None si il n'y en a pas
        for door in self.doors:
            if ((door.frontSquare.equal(frontSquare) and door.backSquare.equal(backSquare)) or
                (door.frontSquare.equal(backSquare) and door.backSquare.equal(frontSquare))):
                return door
        return None



def getRoomsAfterAggregation(aggregatedRooms=[]):
    rooms = getRooms()
    newRooms = rooms
    for aggregatedRoom in aggregatedRooms:
        room1Tuple = aggregatedRoom[0]
        room2Tuple = aggregatedRoom[1]
        room1Dic = tupleToRoomDic(room1Tuple)
        room2Dic = tupleToRoomDic(room2Tuple)
        newRoom = roomDicToTuple(aggregateRooms(room1Dic,room2Dic))

        newRooms += [newRoom]
        newRooms.remove(room1Tuple)
        newRooms.remove(room2Tuple)
    return newRooms



def aggregateRooms(room1,room2):
    x1,y1,w1,h1 = room1["coordinates"]
    x2,y2,w2,h2 = room2["coordinates"]
    x3 = min(x1,x2)
    y3 = min(y1,y2)
    w3 = max(x1+w1,x2+w2)-x3
    h3 = max(y1+h1,y2+h2)-y3

    cR1,cG1,cB1 = room1["color"]
    cR2,cG2,cB2 = room2["color"]
    #c3 = ((cR1+cR2)//2,(cG1+cG2)//2,(cB1+cB2)//2)

    room3 = {"coordinates":(x3,y3,w3,h3),"color":room1["color"]}
    return room3



def listToTupleRec(l):
    return tuple(listToTupleRec(x) for x in l) if type(l) is list else l
