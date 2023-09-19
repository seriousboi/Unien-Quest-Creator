from Square import *
from display import *



class Rock:
    def __init__(self,square):
        self.square = square

    @classmethod
    def fromDict(cls,dict):
        return cls(Square.fromDict(dict["square"]))

    def display(self,surface,shift,squareSize):
        displayRock(surface,shift,squareSize,self.square)

    def toJSON(self):
        return {"square":self.square.toJSON()}



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
