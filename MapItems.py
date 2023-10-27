from Square import *
from display import *


class MapItem:
    def __init__(self,square):
        self.square = square

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["square"]))

    def toJSON(self):
        return {"square":self.square.toJSON()}


class Rock(MapItem):
    def __init__(self,square):
        super().__init__(square)

    def display(self,surface,shift,squareSize):
        displayRock(surface,shift,squareSize,self.square)


class Trap(MapItem):
    def __init__(self,square):
        super().__init__(square)

    def display(self,surface,shift,squareSize):
        displayTrap(surface,shift,squareSize,self.square)


class Furniture(MapItem):
    def __init__(self,square,name="chair",orientation="north"):
        super().__init__(square)
        self.name = name
        self.orientation = orientation

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["square"]),dict["name"],dict["orientation"])

    def display(self,surface,shift,squareSize):
        displayFurniture(surface,shift,squareSize,self.square,self.name,self.orientation)

    def toJSON(self):
        return {"square":self.square.toJSON(),"name":self.name,"orientation":self.orientation}



class Treasure(MapItem):
    def __init__(self,square):
        super().__init__(square)

    def display(self,surface,shift,squareSize):
        displayTreasure(surface,shift,squareSize,self.square)


class Informations:
    def __init__(self,square,infos = ""):
        self.square = square
        self.infos = infos

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["square"]),dict["infos"])

    def display(self,surface,shift,squareSize,index=None):
        displayInfos(surface,shift,squareSize,self.square,index)

    def toJSON(self):
        return {"square":self.square.toJSON(),"infos":self.infos}


class Door:
    def __init__(self,frontSquare,backSquare,type="normal"):
        self.frontSquare = frontSquare
        self.backSquare = backSquare
        self.type = type

    def switchToNextType(self):
        nextDoorType = {"normal":"invisible","invisible":"steel","steel":"ornate","ornate":"normal"}
        self.type = nextDoorType[self.type]

    @classmethod
    def fromDict(cls,dict):
        if "type" not in dict:
            dict["type"] = "normal"
        return cls(Square.fromDict(dict["frontSquare"]),Square.fromDict(dict["backSquare"]),dict["type"])

    def display(self,surface,shift,squareSize):
        displayDoor(surface,shift,squareSize,self.frontSquare,self.backSquare,self.type)

    def toJSON(self):
        return {"frontSquare":self.frontSquare.toJSON(),"backSquare":self.backSquare.toJSON(),"type":self.type}
