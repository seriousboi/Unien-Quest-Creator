from constAndStyle import *
from PGinterfaces import *
from display import *



def FSinitialize(variables):
    variables["furnitureSelected"] = "chair"
    variables["orientation"] = "north"
    variables["furnitureCount"] = variables["currentMap"].countFurniture()

def FSmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))

    button = variables["buttons"]["rotate"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Change orientation: "+variables["orientation"],25,(50,50,50))


    for itemName in furniture:
        button = variables["buttons"][itemName]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,itemName,25,(50,50,50))

        XcopyText = button.rectangle.x + button.rectangle.w*1.1
        YcopyText = button.rectangle.y + button.rectangle.h/2
        itemAmount = variables["furnitureCount"][itemName]
        text(window,str(itemAmount)+"/"+str(furnitureAmounts[itemName]),int(squareSize*(1/2)),(50,50,50),"midleft",XcopyText,YcopyText)


def FSmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    longButWidth = 7*squareSize
    medButHeight = (4/5)*squareSize
    vSpace = squareSize

    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)

    for index,buttonName in enumerate(furniture):
        variables["buttons"][buttonName].rectangle = pygame.Rect(xMargin,index*vSpace+(1/3)*squareSize,medButWidth,medButHeight)

    middleVspace = squareSize
    variables["buttons"]["rotate"].rectangle = pygame.Rect(xMargin,middleVspace+(index+1)*vSpace+(1/3)*squareSize,medButWidth,medButHeight)


def FSback(variables,event):
    variables["state"] = "inEditor"


def rotate(variables,event):
    nextOrientation = {"north":"east","east":"south","south":"west","west":"north"}
    variables["orientation"] = nextOrientation[variables["orientation"]]


furnitureSelectInterface = Interface()

furnitureSelectInterface.initialize = FSinitialize
furnitureSelectInterface.mainDisplay = FSmainDisplay
furnitureSelectInterface.mainProcess = FSmainProcess

furnitureSelectInterface.buttons += [Button("rotate",but2InCol,but2OutCol,rotate)]
furnitureSelectInterface.buttons += [Button("back",otherInCol,otherOutCol,FSback)]


for buttonName in furniture:

    def selectFurnitureItem(variables,event,itemName = buttonName):
        variables["furnitureSelected"] = itemName
        variables["state"] = "inEditor"

    furnitureSelectInterface.buttons += [Button(buttonName,butInCol,butOutCol,selectFurnitureItem)]
