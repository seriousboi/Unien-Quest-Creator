from constAndStyle import *
from PGinterfaces import *
from display import *
from QuestMap import *
import glob



def MSinitialize(variables):
    fileNames = glob.glob('./data/maps/*.json')
    variables["fileNames"] = fileNames
    variables["mapsAmount"] = len(fileNames)

    variables["mapNames"] = []
    for index,fileName in enumerate(fileNames):
        mapName = fileName[12:-5]
        variables["mapNames"] += [mapName]

        def selectMap(variables,event,mapIndex = index):
            try:
                variables["currentMap"] = QuestMap.loadFile(variables["mapNames"][mapIndex])
            except FileNotFoundError:
                print("FileNotFoundError: bruh")

        variables["buttons"][index] = Button("map"+str(index),butInCol,butOutCol,selectMap)




def MSmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))

    for index in range(variables["mapsAmount"]):
        button = variables["buttons"][index]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,variables["mapNames"][index],25,(50,50,50))


def MSmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    longButWidth = 7*squareSize
    medButHeight = squareSize

    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)

    for index in range(variables["mapsAmount"]):
        variables["buttons"][index].rectangle = pygame.Rect(xMargin,(1.25*index+1/3)*squareSize,longButWidth,medButHeight)



def MSback(variables,event):
    variables["state"] = "inEditor"



mapSelectInterface = Interface()

mapSelectInterface.initialize = MSinitialize
mapSelectInterface.mainDisplay = MSmainDisplay
mapSelectInterface.mainProcess = MSmainProcess

mapSelectInterface.buttons += [Button("back",otherInCol,otherOutCol,MSback)]
