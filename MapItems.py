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
    def __init__(self,square,name="chair"):
        super().__init__(square)
        self.name = name

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["square"]),dict["name"])

    def display(self,surface,shift,squareSize):
        displayFurniture(surface,shift,squareSize,self.square,self.name)

    def toJSON(self):
        return {"square":self.square.toJSON(),"name":self.infos}



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
    def __init__(self,frontSquare,backSquare):
        self.frontSquare = frontSquare
        self.backSquare = backSquare

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["frontSquare"]),Square.fromDict(dict["backSquare"]))

    def display(self,surface,shift,squareSize):
        displayDoor(surface,shift,squareSize,self.frontSquare,self.backSquare)

    def toJSON(self):
        return {"frontSquare":self.frontSquare.toJSON(),"backSquare":self.backSquare.toJSON()}
