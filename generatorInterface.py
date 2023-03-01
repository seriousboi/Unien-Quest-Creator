from constAndStyle import *
from PGinterfaces import *
from QuestMap import *
from QuestGraph import *
from display import *
from pygame import *
from generators import *



def GIinitialize(variables):
    graph = QuestGraph()
    config,visited = genHtCC(graph)
    graph.applyConfiguration(config,visited)
    map = QuestMap()
    map.loadGraph(graph)

    variables["currentGraph"] = graph
    variables["currentMap"] = map



def GImainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]

    variables["buttons"]["goToEditor"].rectangle = pygame.Rect((mapLength+2/3)*squareSize,17*squareSize,5*squareSize,squareSize)



def GImainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    variables["currentMap"].display(window,variables["shift"],squareSize)
    variables["currentGraph"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,generatorInCol,(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,generatorOutCol,(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["goToEditor"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Editor",25,(50,50,50))

    #test
    #variables["map"].display(window,variables["shift"],squareSize)
    #variables["testqg"].display(window,shift,squareSize,False)
    #test
    pass



def goToEditor(variables,event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        button = variables["buttons"]["goToEditor"]
        if button.rectangle.collidepoint(event.pos):
            variables["state"] = "inEditor"



generatorInterface = Interface()

generatorInterface.initialize = GIinitialize
generatorInterface.mainDisplay = GImainDisplay
generatorInterface.mainProcess = GImainProcess

generatorInterface.buttons += [Button("goToEditor",butInCol,butOutCol,goToEditor)]
