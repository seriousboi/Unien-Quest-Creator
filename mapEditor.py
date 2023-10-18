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
from furnitureSelect import *
from entityEditor import *
from copy import copy
from drawCards import *
from printer import *



def initialize(variables):
    variables["currentItem"] = None
    variables["copiedItem"] = None
    variables["indexToSwitch"] = None
    variables["itemToSwitchType"] = None
    variables["subState"] = "nothingSpecial"

def mainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    medButHeight = (4/5)*squareSize
    vSpace = squareSize

    #hiboxes definition
    #upper buttons
    for index,buttonName in enumerate(["Door","Rock","Trap","Treasure","furniture","Entity","Annotation"]):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,index*vSpace+(1/3)*squareSize,medButWidth,medButHeight)

    middleVspace = 1*squareSize + squareSize/3 + index*(vSpace)
    #middle buttons
    for index,buttonName in enumerate(["edit","copyItem","indexItem","fuseRooms","resetMap"]):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,middleVspace + index*vSpace+(1/3)*squareSize,medButWidth,medButHeight)

    #lower buttons
    for index,buttonName in enumerate(["goToGenerator","saveImage","saveMap","loadMap"]):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,-index*vSpace+(17.75)*squareSize,medButWidth,medButHeight)

    #button color update
    for button in variables["buttons"].values():
        button.updateColor()

    #removal of the copied item if were not int copying state
    if variables["subState"] != "copying":
        variables["copiedItem"] = None


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
                                    ["saveImage","Output files"],["edit","Edit items"],["copyItem","Copy item"],
                                    ["indexItem","Index items"],["furniture","Furniture"]]:

        button = variables["buttons"][buttonName]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,buttonText,25,(50,50,50))

    button = variables["buttons"]["goToGenerator"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Generator",25,(100,100,200))

    #doors amount text
    doorsAmount = len(variables["currentMap"].doors)
    if doorsAmount > nbMaxDoors:
        msgColor = (250,25,25)
    else:
        msgColor = (50,50,50)
    text(window,str(doorsAmount)+"/"+str(nbMaxDoors),int(squareSize*(1/2)),msgColor,"midleft",xMargin+5.5*squareSize,(0.5+1/3)*squareSize)

    #copy text
    if variables["copiedItem"] != None:
        XcopyText = variables["buttons"]["copyItem"].rectangle.x + variables["buttons"]["copyItem"].rectangle.w*1.1
        YcopyText = variables["buttons"]["copyItem"].rectangle.y + variables["buttons"]["copyItem"].rectangle.h/2
        text(window,"copied",int(squareSize*(1/2)),(50,50,50),"midleft",XcopyText,YcopyText)

    #indexing text
    if variables["subState"] == "indexing" and variables["indexToSwitch"] != None:
        XcopyText = variables["buttons"]["indexItem"].rectangle.x + variables["buttons"]["indexItem"].rectangle.w*1.1
        YcopyText = variables["buttons"]["indexItem"].rectangle.y + variables["buttons"]["indexItem"].rectangle.h/2
        text(window,str(variables["indexToSwitch"]+1),int(squareSize*(1/2)),(50,50,50),"midleft",XcopyText,YcopyText)

    #furniture text
    if variables["currentItem"] in furniture:
        XcopyText = variables["buttons"]["furniture"].rectangle.x + variables["buttons"]["furniture"].rectangle.w*1.02
        YcopyText = variables["buttons"]["furniture"].rectangle.y + variables["buttons"]["furniture"].rectangle.h/2
        text(window,variables["currentItem"],int(squareSize*(1/2)),(50,50,50),"midleft",XcopyText,YcopyText)


def placeOrEditItem(variables,event):
    global mapLength,mapWidth,itemNames
    sqsz = variables["squareSize"]

    if event.type == pygame.MOUSEBUTTONDOWN:
        x = event.pos[0] - variables["shift"][0]
        y = event.pos[1] - variables["shift"][1]

        currentItem = variables["currentItem"]
        if currentItem == "Door" and variables["subState"] == "placing":
            placeDoor(variables,x,y)

        elif variables["subState"] != "nothingSpecial":
            if (x >= 0 and x <= mapLength*sqsz and
                y >= 0 and y <= mapWidth*sqsz):
                xSquare = int(x/sqsz)
                ySquare = int(y/sqsz)
                square = Square(xSquare,ySquare)
                item = variables["currentMap"].itemAt(square)

                if variables["subState"] == "editing":
                    editItem(variables,item)

                elif variables["subState"] == "indexing":
                    indexItem(variables,item)

                elif variables["subState"] == "copying":
                    if item != None :
                        copyItem(variables,item)
                    elif variables["copiedItem"] != None:
                        placeCopiedItem(variables,square)

                elif variables["subState"] == "placing":
                    if item == None:
                        if currentItem == "Rock":
                            variables["currentMap"].rocks += [Rock(square)]
                        elif currentItem == "Trap":
                            variables["currentMap"].traps += [Trap(square)]
                        elif currentItem == "Treasure":
                            variables["currentMap"].treasures += [Treasure(square)]
                        elif currentItem == "Entity":
                            variables["currentMap"].entities += [Entity(square.x,square.y)]
                        elif currentItem == "Annotation":
                            variables["currentMap"].annotations += [Informations(square)]
                        elif currentItem in furniture:
                            variables["currentMap"].furniture += [Furniture(square,currentItem)]
                    else:
                        variables["currentMap"].removeItemAT(item,square)


def indexItem(variables,item):

    if item != None:

        itemType = type(item)
        if variables["indexToSwitch"] == None or variables["itemToSwitchType"] != itemType:
            if itemType == Entity:
                variables["indexToSwitch"] = variables["currentMap"].entities.index(item)
                variables["itemToSwitchType"] = itemType
            elif itemType == Informations:
                variables["indexToSwitch"] = variables["currentMap"].annotations.index(item)
                variables["itemToSwitchType"] = itemType
        else:
            if itemType == Entity:
                itemToSwitch = variables["currentMap"].entities[variables["indexToSwitch"]]
                otherIdexToSwitch = variables["currentMap"].entities.index(item)
                variables["currentMap"].entities[variables["indexToSwitch"]] = item
                variables["currentMap"].entities[otherIdexToSwitch] = itemToSwitch
            elif itemType == Informations:
                itemToSwitch = variables["currentMap"].annotations[variables["indexToSwitch"]]
                otherIdexToSwitch = variables["currentMap"].annotations.index(item)
                variables["currentMap"].annotations[variables["indexToSwitch"]] = item
                variables["currentMap"].annotations[otherIdexToSwitch] = itemToSwitch
            variables["indexToSwitch"] = None
            variables["itemToSwitchType"] = None


def copyItem(variables,item):
    if type(item) == Entity or type(item) == Informations:
        #doing weird stuff to because we want a new object rather than a reference to an existing one
        #(and because there I havent done a copy method)
        variables["copiedItem"] = item.fromDict(item.toJSON())


def placeCopiedItem(variables,square):
    item = variables["copiedItem"].fromDict(variables["copiedItem"].toJSON())
    item.square.x = square.x
    item.square.y = square.y
    if type(item) == Entity:
        variables["currentMap"].entities += [item]
    if type(item) == Informations:
        variables["currentMap"].annotations += [item]

def editItem(variables,item):
    if type(item) == Entity:
        EEvariables = copy(variables)
        EEvariables["entity"] = item
        window = variables["window"]
        entityEditor.run(window,EEvariables,"editing entity")
        if EEvariables["state"] == "quitting":
            variables["state"] = "quitting"
    elif type(item) == Informations:
        TEvariables = copy(variables)
        TEvariables["text"] = item.infos
        textEditor.run(variables["window"],TEvariables,"editing annotation text")
        item.infos = TEvariables["text"]
        if TEvariables["state"] == "quitting":
            variables["state"] = "quitting"


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

    #clearing map and entity folder
    clearFolder("output/map/")
    clearFolder("output/entityCards/")

    squareSize = variables["squareSize"]
    window = variables["window"]
    imageOutput = Surface((squareSize*mapLength,squareSize*mapWidth))
    imageOutput.blit(window,(0,0))
    pygame.image.save(imageOutput,"output/map/map.png")

    for entity in variables["currentMap"].entities:
        card = getMonsterCard(entity)
        pygame.image.save(card,"output/entityCards/"+entity.name+"Card.png")
    outputSheets("output/entityCards/")


    fakeBooardSurface = Surface((squareSize*mapLength,squareSize*mapWidth))
    displayBoard(fakeBooardSurface,(0,0),squareSize,variables["currentMap"].rooms)
    for aggregatedRoom in variables["currentMap"].aggregatedRooms:
        room1 = aggregatedRoom[0]
        room2 = aggregatedRoom[1]
        room3 = roomDicToTuple(aggregateRooms(tupleToRoomDic(room1),tupleToRoomDic(room2)))
        roomSurface = Surface((squareSize*room3[2],squareSize*room3[3]))
        roomSurface.blit(fakeBooardSurface,(-squareSize*room3[0],-squareSize*room3[1]))
        pygame.image.save(roomSurface,"output/map/"+str(room3)+".png")

    variables["currentMap"].outputTextFiles()
    print("Files saved in output folder")

def saveMap(variables,event):
    try:
        variables["currentMap"].saveToFile()
    except FileNotFoundError:
        print("FileNotFoundError: bruh")


def loadMap(variables,event):
    MSvariables = copy(variables)
    window = variables["window"]
    mapSelectInterface.run(window,MSvariables,"selecting")
    if MSvariables["currentMap"] != None:
        variables["currentMap"] = MSvariables["currentMap"]

    if MSvariables["state"] == "quitting":
        variables["state"] = "quitting"


def fusionSelect(variables,event):
    FSvariables = copy(variables)
    window = variables["window"]
    fusionSelectInterface.run(window,FSvariables,"selecting")
    if FSvariables["state"] == "quitting":
        variables["state"] = "quitting"


def resetMap(variables,event):
    variables["currentMap"] = QuestMap([],[],[],[],[],[],[])


def edit(variables,event):
    desactivateAllButtons(variables["buttons"])
    variables["buttons"]["edit"].active = True
    variables["subState"] = "editing"


def selectCopy(variables,event):
    desactivateAllButtons(variables["buttons"])
    variables["buttons"]["copyItem"].active = True
    variables["subState"] = "copying"


def selectIndex(variables,event):
    desactivateAllButtons(variables["buttons"])
    variables["buttons"]["indexItem"].active = True
    variables["subState"] = "indexing"
    variables["indexToSwitch"] = None
    variables["itemToSwitchType"] = None


def desactivateAllButtons(buttons):
    for buttonName in buttons:
        buttons[buttonName].active = False


def selectFurniture(variables,event):
    FSvariables = copy(variables)
    window = variables["window"]
    furnitureSelectInterface.run(window,FSvariables,"selecting")

    if FSvariables["state"] == "quitting":
        variables["state"] = "quitting"

    if FSvariables["furnitureSelected"] != None:
        desactivateAllButtons(variables["buttons"])
        button = variables["buttons"]["furniture"]
        button.active = True
        variables["currentItem"] = FSvariables["furnitureSelected"]
        variables["subState"] = "placing"



mainInterface = Interface()

mainInterface.initialize = initialize
mainInterface.mainDisplay = mainDisplay
mainInterface.mainProcess = mainProcess


mainInterface.buttons += [Button("place",None,None,placeOrEditItem,False)]
mainInterface.buttons += [Button("furniture",butInCol,butOutCol,selectFurniture,activeInColor=butPresInCol,activeOutColor=butPresOutCol)]
mainInterface.buttons += [Button("edit",but2InCol,but2OutCol,edit,activeInColor=but2PresInCol,activeOutColor=but2PresOutCol)]
mainInterface.buttons += [Button("indexItem",but2InCol,but2OutCol,selectIndex,activeInColor=but2PresInCol,activeOutColor=but2PresOutCol)]
mainInterface.buttons += [Button("copyItem",but2InCol,but2OutCol,selectCopy,activeInColor=but2PresInCol,activeOutColor=but2PresOutCol)]
mainInterface.buttons += [Button("fuseRooms",but2InCol,but2OutCol,fusionSelect)]
mainInterface.buttons += [Button("resetMap",but2InCol,but2OutCol,resetMap)]

mainInterface.buttons += [Button("loadMap",otherInCol,otherOutCol,loadMap)]
mainInterface.buttons += [Button("saveMap",otherInCol,otherOutCol,saveMap)]
mainInterface.buttons += [Button("saveImage",otherInCol,otherOutCol,saveImage)]
mainInterface.buttons += [Button("goToGenerator",(250,250,50),(100,100,200),goToGenerator)]


for buttonName in itemNames:

    def selectItem(variables,event,itemName = buttonName):
        desactivateAllButtons(variables["buttons"])
        button = variables["buttons"][itemName]
        button.active = True
        variables["currentItem"] = itemName
        variables["subState"] = "placing"


    mainInterface.buttons += [Button(buttonName,butInCol,butOutCol,selectItem,activeInColor=butPresInCol,activeOutColor=butPresOutCol)]
