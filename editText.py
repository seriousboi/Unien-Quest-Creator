from constAndStyle import *
from PGinterfaces import *
from display import *
from Entity import *


def TEinitialize(variables):
    variables["buttons"]["text"].text = variables["text"]



def TEmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    longButWidth = 7*squareSize
    medButHeight = squareSize
    namesWidth = 3*squareSize

    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)

    variables["text"] = variables["buttons"]["text"].text


    variables["buttons"]["text"].minHeight = squareSize//2
    variables["buttons"]["text"].minWidth = longButWidth
    variables["buttons"]["text"].maxLineWidth = longButWidth
    variables["buttons"]["text"].textSize = squareSize//2
    variables["buttons"]["text"].x = xMargin
    variables["buttons"]["text"].y = (1/3)*squareSize
    variables["buttons"]["text"].update()

def TEmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]
    xMargin = (mapLength+2/3)*squareSize
    namesWidth = 3*squareSize

    if variables["mainVars"]["currentMap"] != None:
        variables["mainVars"]["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))

    variables["buttons"]["text"].display(window)

def TEback(variables,event):
    variables["state"] = "inEditor"


textEditor = Interface()

textEditor.initialize = TEinitialize
textEditor.mainDisplay = TEmainDisplay
textEditor.mainProcess = TEmainProcess

textEditor.buttons += [Button("back",otherInCol,otherOutCol,TEback)]


textEditor.buttons += [TextBox("text",multiLines=True,
inactiveInColor=(230,210,160),inactiveOutColor=(200,184,144),
activeInColor=(255,250,190),activeOutColor=(200,184,144))]
