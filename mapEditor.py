from constAndStyle import *
from PGinterfaces import *
from QuestMap import *
from QuestGraph import *
from display import *
from pygame import *
from generators import *



def initialize(variables):
    variables["currentItem"] = None

    #we reset the button colors because the button objects are the same between two calls of runInterface
    for itemName in itemNames:
        button = variables["buttons"][itemName]
        button.inColor = butInCol
        button.outColor = butOutCol



def mainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    variables["buttons"]["Door"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,(1/3)*squareSize,5*squareSize,squareSize)
    variables["buttons"]["Rock"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,(1.25+1/3)*squareSize,5*squareSize,squareSize)

    variables["buttons"]["goToGenerator"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,17*squareSize,5*squareSize,squareSize)



def mainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    for itemName in itemNames:
        button = variables["buttons"][itemName]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,itemName,25,(50,50,50))

    button = variables["buttons"]["goToGenerator"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Generator",25,(50,50,50))



def placeItem(variables,event):
    global mapLength,mapWidth
    sqsz = variables["squareSize"]

    mapChanged = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        x = event.pos[0] - variables["shift"][0]
        y = event.pos[1] - variables["shift"][1]

        if variables["currentItem"] == "Door":
            if (x > (1/4)*sqsz and x < (mapLength-1/4)*sqsz and
                y > (1/4)*sqsz and y < (mapWidth-1/4)*sqsz):

                if y%sqsz <= (3/10)*(sqsz-1) or y%sqsz >= (7/10)*(sqsz-1):
                    mapChanged = True

                    xSquare = int(x/sqsz)
                    ySquare = round(y/sqsz)
                    frontSquare = Square(xSquare,ySquare-1)
                    backSquare = Square(xSquare,ySquare)
                    if variables["currentMap"].doorAt(frontSquare,backSquare) == None:
                        variables["currentMap"].doors += [Door(frontSquare,backSquare)]
                    else:
                        variables["currentMap"].doors.remove(variables["currentMap"].doorAt(frontSquare,backSquare))

                elif x%sqsz <= (3/10)*(sqsz-1) or x%sqsz >= (7/10)*(sqsz-1):
                    mapChanged = True

                    xSquare = round(x/sqsz)
                    ySquare = int(y/sqsz)
                    frontSquare = Square(xSquare-1,ySquare)
                    backSquare = Square(xSquare,ySquare)
                    if variables["currentMap"].doorAt(frontSquare,backSquare) == None:
                        variables["currentMap"].doors += [Door(frontSquare,backSquare)]
                    else:
                        variables["currentMap"].doors.remove(variables["currentMap"].doorAt(frontSquare,backSquare))

        if variables["currentItem"] == "Rock":
            if (x >= 0 and x <= mapLength*sqsz and
                y >= 0 and y <= mapWidth*sqsz):

                mapChanged = True

                xSquare = int(x/sqsz)
                ySquare = int(y/sqsz)
                square = Square(xSquare,ySquare)
                if variables["currentMap"].itemAt(square) == None:
                    variables["currentMap"].rocks += [Rock(square)]
                else:
                    variables["currentMap"].rocks.remove(variables["currentMap"].itemAt(square))
    if mapChanged:
        variables["currentGraph"] = None



def goToGenerator(variables,event):
    variables["state"] = "inGenerator"



mainInterface = Interface()

mainInterface.initialize = initialize
mainInterface.mainDisplay = mainDisplay
mainInterface.mainProcess = mainProcess

mainInterface.buttons += [Button("place",None,None,placeItem,False)]
mainInterface.buttons += [Button("goToGenerator",generatorInCol,generatorOutCol,goToGenerator)]

for buttonName in itemNames:

    def selectItem(variables,event,itemName = buttonName):
        if variables["currentItem"] != None: # we reset the color of the last button pressed
            previousButtonPressed = variables["buttons"][variables["currentItem"]]
            previousButtonPressed.inColor = butInCol
            previousButtonPressed.outColor = butOutCol
        button = variables["buttons"][itemName]
        variables["currentItem"] = itemName
        button.inColor = butPresInCol
        button.outColor = butPresOutCol

    mainInterface.buttons += [Button(buttonName,butInCol,butOutCol,selectItem)]
