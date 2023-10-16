from Square import *
from Entity import *
from MapItems import *
from display import *
import json



class QuestMap:
    def __init__(self,doors=[],rocks=[],entities=[],aggregatedRooms=[],annotations=[],traps=[],treasures=[]):
        self.doors = doors
        self.rocks = rocks
        self.entities = entities
        self.annotations = annotations
        self.traps = traps
        self.treasures = treasures
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
        listsToFill = {"doors":[],"rocks":[],"traps":[],"treasures":[],"entities":[],"aggregatedRooms":[],"annotations":[]}
        construtorsToUse = {"doors":Door.fromDict,"rocks":Rock.fromDict,"traps":Trap.fromDict,"treasures":Treasure.fromDict,"entities":Entity.fromDict,"aggregatedRooms":listToTupleRec,"annotations":Informations.fromDict}

        for key in listsToFill:
            for thing in dict[key]:
                listsToFill[key] += [construtorsToUse[key](thing)]

        return cls(listsToFill["doors"],listsToFill["rocks"],listsToFill["entities"],listsToFill["aggregatedRooms"],listsToFill["annotations"],listsToFill["traps"],listsToFill["treasures"])


    def toJSON(self):
        JSONdic = {"doors":[],"rocks":[],"traps":[],"treasures":[],"entities":[],"annotations":[]}
        listsToUse = {"doors":self.doors,"rocks":self.rocks,"traps":self.traps,"treasures":self.treasures,"entities":self.entities,"annotations":self.annotations}

        for key in JSONdic:
            for thing in listsToUse[key]:
                JSONdic[key] += [thing.toJSON()]

        JSONdic["aggregatedRooms"] = self.aggregatedRooms
        return JSONdic

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
        self.annotations = []
        for connector in questGraph.connectors:
            if connector.type == "Rock" and connector.open == False:
                for square in connector.squares:
                    self.rocks += [Rock(square)]
            if connector.type == "Door" and connector.open == True:
                self.doors += [Door(connector.frontSquare,connector.backSquare)]

        self.aggregatedRooms = []
        self.rooms = getRoomsAfterAggregation(self.aggregatedRooms)

    def outputTextFiles(self,folderPath="output/text/"):
        #clearing text folder
        clearFolder(folderPath)

        #annotations
        file= open(folderPath+"annotations.txt","w")
        newLines = []
        for index,annotation in enumerate(self.annotations):
            newLines += ["\n \n["+str(index+1)+"]\n"]
            newLines += [annotation.infos]
        file.writelines(newLines)
        file.close()

        #entities
        for index,entity in enumerate(self.entities):
            if entity.infos != "":
                file = open(folderPath+entity.name+"_infos.txt","w")
                newLines = ["["+entity.name+"("+str(index+1)+")]\n"]
                newLines += [entity.infos]
                file.writelines(newLines)
                file.close()

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
        for item in self.rocks+self.doors+self.traps+self.treasures:
            item.display(surface,shift,squareSize)
        for index,entity in enumerate(self.entities):
            entity.display(surface,shift,squareSize,index+1)
        for index,infos in enumerate(self.annotations):
            infos.display(surface,shift,squareSize,index+1)

    def itemAt(self,square):
        for item in self.rocks+self.entities+self.annotations+self.traps+self.treasures:
            if item.square.equal(square):
                return item
        return None

    def removeItemAT(self,item,square):
        for itemsList in [self.rocks,self.entities,self.annotations,self.traps,self.treasures]:
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


import os, shutil
def clearFolder(folderPath):
    for filename in os.listdir(folderPath):
        file_path = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
