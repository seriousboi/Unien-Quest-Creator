from constAndStyle import *
from PGinterfaces import *
from QuestMap import *
from QuestGraph import *
from Entity import *
from display import *
from pygame import *
from generators import *
from mapSelect import *
from  fusionSelect import *
from entityEditor import *
from copy import copy



def initialize(variables):
    variables["currentItem"] = None
    variables["editing"] = False


def mainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    medButHeight = squareSize

    #hiboxes definition
    #upper buttons
    for index,buttonName in enumerate(["Door","Rock","Monster","Informations","edit","fuseRooms","resetMap"]):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,(index*1.25+1/3)*squareSize,medButWidth,medButHeight)

    #lower buttons
    for index,buttonName in enumerate(["goToGenerator","saveImage","saveMap","loadMap"]):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,(17-1.25*index)*squareSize,medButWidth,medButHeight)

    #button color update
    for button in variables["buttons"].values():
        button.updateColor()


def mainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]
    xMargin = (mapLength+2/3)*squareSize

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    for itemName in itemNames:
        button = variables["buttons"][itemName]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,itemName,25,(50,50,50))

    for buttonName,buttonText in [["fuseRooms","Fuse rooms"],["resetMap","Reset map"],
                                    ["loadMap","Load a map"],["saveMap","Save to file"],
                                    ["saveImage","Save to image"],["edit","Edit items"]]:

        button = variables["buttons"][buttonName]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,buttonText,25,(50,50,50))

    button = variables["buttons"]["goToGenerator"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Generator",25,(100,100,200))

    doorsAmount = len(variables["currentMap"].doors)
    if doorsAmount > nbMaxDoors:
        msgColor = (250,25,25)
    else:
        msgColor = (50,50,50)
    text(window,str(doorsAmount)+"/"+str(nbMaxDoors),int(squareSize*(1/2)),msgColor,"midleft",xMargin+5.5*squareSize,(0.5+1/3)*squareSize)


def placeOrEditItem(variables,event):
    global mapLength,mapWidth
    sqsz = variables["squareSize"]

    if event.type == pygame.MOUSEBUTTONDOWN:
        x = event.pos[0] - variables["shift"][0]
        y = event.pos[1] - variables["shift"][1]

        currentItem = variables["currentItem"]
        if currentItem == "Door":
            placeDoor(variables,x,y)

        elif (currentItem in ["Rock","Monster","Informations"]) or variables["editing"]:
            if (x >= 0 and x <= mapLength*sqsz and
                y >= 0 and y <= mapWidth*sqsz):
                xSquare = int(x/sqsz)
                ySquare = int(y/sqsz)
                square = Square(xSquare,ySquare)
                item = variables["currentMap"].itemAt(square)

                if variables["editing"]:
                    editItem(variables,item)

                elif item == None:
                    if currentItem == "Rock":
                        variables["currentMap"].rocks += [Rock(square)]
                    elif currentItem == "Monster":
                        variables["currentMap"].entities += [Entity(square.x,square.y)]
                    elif currentItem == "Informations":
                        variables["currentMap"].informations += [Informations(square)]

                else:
                    variables["currentMap"].removeItemAT(item,square)



def editItem(variables,item):
    if type(item) == Entity:
        EEvariables = copy(variables)
        EEvariables["mainVars"] = variables
        EEvariables["entity"] = item
        window = variables["window"]
        entityEditor.run(window,EEvariables,"editing entity")
        if EEvariables["state"] == "quitting":
            variables["state"] = "quitting"
    elif type(item) == Informations:
        print("infos")



def placeInfos(variables,x,y):
    variables["currentItem"] = None
    variables["editing"] = True


def placeDoor(variables,x,y):
    global mapLength,mapWidth
    sqsz = variables["squareSize"]

    if (x > (1/4)*sqsz and x < (mapLength-1/4)*sqsz and
        y > (1/4)*sqsz and y < (mapWidth-1/4)*sqsz):

        if y%sqsz <= (3/10)*(sqsz-1) or y%sqsz >= (7/10)*(sqsz-1):

            xSquare = int(x/sqsz)
            ySquare = round(y/sqsz)
            frontSquare = Square(xSquare,ySquare-1)
            backSquare = Square(xSquare,ySquare)
            if variables["currentMap"].doorAt(frontSquare,backSquare) == None:
                variables["currentMap"].doors += [Door(frontSquare,backSquare)]
            else:
                variables["currentMap"].doors.remove(variables["currentMap"].doorAt(frontSquare,backSquare))

        elif x%sqsz <= (3/10)*(sqsz-1) or x%sqsz >= (7/10)*(sqsz-1):

            xSquare = round(x/sqsz)
            ySquare = int(y/sqsz)
            frontSquare = Square(xSquare-1,ySquare)
            backSquare = Square(xSquare,ySquare)
            if variables["currentMap"].doorAt(frontSquare,backSquare) == None:
                variables["currentMap"].doors += [Door(frontSquare,backSquare)]
            else:
                variables["currentMap"].doors.remove(variables["currentMap"].doorAt(frontSquare,backSquare))


def goToGenerator(variables,event):
    variables["state"] = "inGenerator"
    variables["currentGraph"] = None


def saveImage(variables,event):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    window = variables["window"]
    imageOutput = Surface((squareSize*mapLength,squareSize*mapWidth))
    imageOutput.blit(window,(0,0))
    pygame.image.save(imageOutput,"map.png")
    print("Map saved to map.png")



def saveMap(variables,event):
    try:
        variables["currentMap"].saveToFile()
    except FileNotFoundError:
        print("FileNotFoundError: bruh")



def loadMap(variables,event):
    MSvariables = copy(variables)
    MSvariables["mainVars"] = variables

    window = variables["window"]
    mapSelectInterface.run(window,MSvariables,"selecting")

    if MSvariables["state"] == "quitting":
        variables["state"] = "quitting"



def fusionSelect(variables,event):
    FSvariables = copy(variables)
    FSvariables["mainVars"] = variables

    window = variables["window"]
    fusionSelectInterface.run(window,FSvariables,"selecting")

    if FSvariables["state"] == "quitting":
        variables["state"] = "quitting"


def resetMap(variables,event):
    variables["currentMap"] = QuestMap([],[],[],[])


def edit(variables,event):
    if variables["currentItem"] != None: # we reset the color of the last button pressed
        previousButtonPressed = variables["buttons"][variables["currentItem"]]
        previousButtonPressed.active = False
        variables["currentItem"] = None
    variables["buttons"]["edit"].active = True
    variables["editing"] = True

mainInterface = Interface()

mainInterface.initialize = initialize
mainInterface.mainDisplay = mainDisplay
mainInterface.mainProcess = mainProcess

mainInterface.buttons += [Button("place",None,None,placeOrEditItem,False)]
mainInterface.buttons += [Button("edit",but2InCol,but2OutCol,edit,activeInColor=but2PresInCol,activeOutColor=but2PresOutCol)]
mainInterface.buttons += [Button("fuseRooms",but2InCol,but2OutCol,fusionSelect)]
mainInterface.buttons += [Button("resetMap",but2InCol,but2OutCol,resetMap)]

mainInterface.buttons += [Button("loadMap",otherInCol,otherOutCol,loadMap)]
mainInterface.buttons += [Button("saveMap",otherInCol,otherOutCol,saveMap)]
mainInterface.buttons += [Button("saveImage",otherInCol,otherOutCol,saveImage)]
mainInterface.buttons += [Button("goToGenerator",(250,250,50),(100,100,200),goToGenerator)]


for buttonName in itemNames:

    def selectItem(variables,event,itemName = buttonName):
        if variables["currentItem"] != None: # we reset the color of the last button pressed
            previousButtonPressed = variables["buttons"][variables["currentItem"]]
            previousButtonPressed.active = False
            variables["currentItem"] = None

        if variables["editing"]:
            variables["buttons"]["edit"].active = False
            variables["editing"] = False

        button = variables["buttons"][itemName]
        variables["currentItem"] = itemName
        button.active = True


    mainInterface.buttons += [Button(buttonName,butInCol,butOutCol,selectItem,activeInColor=butPresInCol,activeOutColor=butPresOutCol)]
