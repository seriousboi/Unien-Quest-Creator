from display import *



class Square:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def equal(self,otherSquare):
        if self.x == otherSquare.x and self.y == otherSquare.y:
            return True
        else:
            return False



class Door:
    def __init__(self,frontSquare,backSquare):
        self.frontSquare = frontSquare
        self.backSquare = backSquare

    def display(self,surface,shift,squareSize):
        displayDoor(surface,shift,squareSize,self.frontSquare,self.backSquare)



class Rock:
    def __init__(self,square):
        self.square = square

    def display(self,surface,shift,squareSize):
        displayRock(surface,shift,squareSize,self.square)



class QuestMap:
    def __init__(self,doors=[],rocks=[]):
        self.doors = doors
        self.rocks = rocks

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
