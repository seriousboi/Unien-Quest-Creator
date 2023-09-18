from display import *
import json



class Square():
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y

    @classmethod
    def fromDict(cls,dict):
        return cls(dict["x"],dict["y"])

    def equal(self,otherSquare):
        if self.x == otherSquare.x and self.y == otherSquare.y:
            return True
        else:
            return False

    def toJSON(self):
        return {"x":self.x,"y":self.y}



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



class QuestMap:
    def __init__(self,doors=[],rocks=[]):
        self.doors = doors
        self.rocks = rocks

    @classmethod
    def fromDict(cls,dict):
        doors = []
        for door in dict["doors"]:
            doors += [Door.fromDict(door)]
        rocks = []
        for rock in dict["rocks"]:
            rocks += [Rock.fromDict(rock)]
        return cls(doors,rocks)

    def toJSON(self):
        doors = []
        for door in self.doors:
            doors += [door.toJSON()]
        rocks = []
        for rock in self.rocks:
            rocks += [rock.toJSON()]
        return {"doors":doors,"rocks":rocks}


    def loadGraph(self,questGraph):
        self.doors = []
        self.rocks = []
        for connector in questGraph.connectors:
            if connector.type == "Rock" and connector.open == False:
                for square in connector.squares:
                    self.rocks += [Rock(square)]
            if connector.type == "Door" and connector.open == True:
                self.doors += [Door(connector.frontSquare,connector.backSquare)]

    def display(self,surface,shift,squareSize):
        displayBoard(surface,shift,squareSize)
        for rock in self.rocks:
            rock.display(surface,shift,squareSize)
        for door in self.doors:
            door.display(surface,shift,squareSize)

    def itemAt(self,square):
        for rock in self.rocks:
            if rock.square.equal(square):
                return rock
        return None

    def doorAt(self,frontSquare,backSquare): #retourne la porte entre frontSquare et backSquare, None si il n'y en a pas
        for door in self.doors:
            if ((door.frontSquare.equal(frontSquare) and door.backSquare.equal(backSquare)) or
                (door.frontSquare.equal(backSquare) and door.backSquare.equal(frontSquare))):
                return door
        return None
