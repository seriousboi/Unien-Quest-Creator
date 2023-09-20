from Square import *
from Entity import *
from MapItems import *
from display import *
import json



class QuestMap:
    def __init__(self,doors=[],rocks=[],entities=[],aggregatedRooms=[[3,4]]):
        self.doors = doors
        self.rocks = rocks
        self.entities = entities
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
        return cls(doors,rocks,entities)

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
        return {"doors":doors,"rocks":rocks,"entities":entities}

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
        for connector in questGraph.connectors:
            if connector.type == "Rock" and connector.open == False:
                for square in connector.squares:
                    self.rocks += [Rock(square)]
            if connector.type == "Door" and connector.open == True:
                self.doors += [Door(connector.frontSquare,connector.backSquare)]

        self.aggregatedRooms = []
        self.rooms = getRoomsAfterAggregation(self.aggregatedRooms)

    def display(self,surface,shift,squareSize):
        displayBoard(surface,shift,squareSize,self.rooms)
        for rock in self.rocks:
            rock.display(surface,shift,squareSize)
        for door in self.doors:
            door.display(surface,shift,squareSize)
        for entity in self.entities:
            entity.display(surface,shift,squareSize)

    def itemAt(self,square):
        for rock in self.rocks:
            if rock.square.equal(square):
                return rock
        for entity in self.entities:
            if entity.square.equal(square):
                return entity
        return None

    def removeItemAT(self,item,square):
        if item in self.rocks:
            self.rocks.remove(item)
        elif item in self.entities:
            self.entities.remove(item)
        else:
            print("could not find item to remove, bruh")


    def doorAt(self,frontSquare,backSquare): #retourne la porte entre frontSquare et backSquare, None si il n'y en a pas
        for door in self.doors:
            if ((door.frontSquare.equal(frontSquare) and door.backSquare.equal(backSquare)) or
                (door.frontSquare.equal(backSquare) and door.backSquare.equal(frontSquare))):
                return door
        return None



def getRoomsAfterAggregation(aggregatedRooms):
    rooms = getRooms()
    newRooms = rooms
    for aggregatedRoom in aggregatedRooms:
        roomIndex1 = aggregatedRoom[0]
        roomIndex2 = aggregatedRoom[1]
        room1Tuple = rooms[roomIndex1]
        room2Tuple = rooms[roomIndex2]
        room1Dic = tupleToRoomDic(room1Tuple)
        room2Dic = tupleToRoomDic(room2Tuple)
        newRoom = roomDicToTuple(aggregateRooms(room1Dic,room2Dic))

        newRooms += [newRoom]
        newRooms.remove(room1Tuple)
        newRooms.remove(room2Tuple)
    return newRooms
