from constAndStyle import *
from PGinterfaces import *
from QuestMap import *
from QuestGraph import *
from display import *
from pygame import *
from generators import *



def GIinitialize(variables):
    variables["connectivity"] = "low"



def GImainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]

    variables["buttons"]["goToEditor"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,17*squareSize,5*squareSize,squareSize)
    variables["buttons"]["generate"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,(1/3)*squareSize,5*squareSize,squareSize)
    variables["buttons"]["decreaseConnectivity"].rectangle = pygame.Rect((mapLength+2/3+5.2)*squareSize,(0.1+5/3)*squareSize,squareSize*0.8,squareSize*0.8)
    variables["buttons"]["increaseConnectivity"].rectangle = pygame.Rect((mapLength+2/3+6.2)*squareSize,(0.1+5/3)*squareSize,squareSize*0.8,squareSize*0.8)



def GImainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)
    if variables["currentGraph"] != None:
        variables["currentGraph"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,generatorInCol,(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,generatorOutCol,(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)



    button = variables["buttons"]["goToEditor"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Editor",25,(50,50,50))

    button = variables["buttons"]["generate"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Generate",25,button.outColor)

    displayConnectivity(window,variables,25)

    button = variables["buttons"]["increaseConnectivity"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"+",25,button.outColor)
    button = variables["buttons"]["decreaseConnectivity"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"-",25,button.outColor)



def displayConnectivity(surface,variables,size):
    squareSize = variables["squareSize"]
    rectangle = pygame.Rect((mapLength+2/3)*squareSize,(5/3)*squareSize,5*squareSize,squareSize)
    pygame.draw.rect(surface,generatorOptInCol,rectangle,0,4)
    pygame.draw.rect(surface,generatorOptOutCol,rectangle,2,4)
    x = rectangle[0]+rectangle[2]/2
    y = rectangle[1]+rectangle[3]/2
    text(surface,"Connectivity: "+variables["connectivity"],size,(50,50,50),"center",x,y)



def goToEditor(variables,event):
    variables["state"] = "inEditor"



def increaseConnectivity(variables,event):
    connectivityLevel = {"minimum":0,"low":1,"medium":2,"high":3,"maximum":4}[variables["connectivity"]]
    connectivityLevel = min(connectivityLevel+1,4)
    variables["connectivity"] = {0:"minimum",1:"low",2:"medium",3:"high",4:"maximum"}[connectivityLevel]



def decreaseConnectivity(variables,event):
    connectivityLevel = {"minimum":0,"low":1,"medium":2,"high":3,"maximum":4}[variables["connectivity"]]
    connectivityLevel = max(connectivityLevel-1,0)
    variables["connectivity"] = {0:"minimum",1:"low",2:"medium",3:"high",4:"maximum"}[connectivityLevel]



def generate(variables,event):
    visitedPenalty = {"minimum":0.001,"low":0.05,"medium":0.2,"high":0.8,"maximum":10}[variables["connectivity"]]

    graph = QuestGraph()
    config,visited = genHtCC(graph,visitedPenalty)
    graph.applyConfiguration(config,visited)
    map = QuestMap()
    map.loadGraph(graph)

    variables["currentGraph"] = graph
    variables["currentMap"] = map



generatorInterface = Interface()

generatorInterface.initialize = GIinitialize
generatorInterface.mainDisplay = GImainDisplay
generatorInterface.mainProcess = GImainProcess

generatorInterface.buttons += [Button("goToEditor",butInCol,butOutCol,goToEditor)]
generatorInterface.buttons += [Button("generate",(250,250,50),(100,100,200),generate)]
generatorInterface.buttons += [Button("increaseConnectivity",generatorOptInCol,generatorOptOutCol,increaseConnectivity)]
generatorInterface.buttons += [Button("decreaseConnectivity",generatorOptInCol,generatorOptOutCol,decreaseConnectivity)]
