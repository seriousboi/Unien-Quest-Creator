from constAndStyle import *
from PGinterfaces import *
from display import *



def FSinitialize(variables):
    if variables["currentMap"] == None:
        return

    variables["selectedRooms"] = [None,None]

    for room in variables["currentMap"].rooms:

        def selectRoom(variables,event,selectedRoom = room):
            selectedRoom1 = variables["selectedRooms"][0]
            selectedRoom2 = variables["selectedRooms"][1]

            if selectedRoom1 == None and selectedRoom2 == None:
                variables["selectedRooms"][0] = selectedRoom
            elif selectedRoom1 != None and selectedRoom2 == None:
                variables["selectedRooms"][1] = selectedRoom
            else:
                variables["selectedRooms"][0] = variables["selectedRooms"][1]
                variables["selectedRooms"][1] = selectedRoom


        button = Button("room "+str(room[0:4]),None,None,selectRoom)
        variables["buttons"][room[0:4]] = button



def FSmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    shift = variables["shift"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    medButHeight = squareSize

    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)
    variables["buttons"]["fuse"].rectangle = pygame.Rect(xMargin,2*squareSize,medButWidth,medButHeight)
    variables["buttons"]["resetFusions"].rectangle = pygame.Rect(xMargin,15.75*squareSize,medButWidth,medButHeight)

    for room in variables["currentMap"].rooms:
        x,y,w,h = room[0:4]
        variables["buttons"][room[0:4]].rectangle = pygame.Rect(shift[0]+squareSize*x,shift[1]+squareSize*y,w*squareSize,h*squareSize)


def FSmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]
    xMargin = (mapLength+2/3)*squareSize

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    selectedRoom1 = variables["selectedRooms"][0]
    selectedRoom2 = variables["selectedRooms"][1]

    if selectedRoom1 == None and selectedRoom2 == None:
        text(window,"Select rooms to fuse",int(squareSize*(2/3)),(50,50,50),"topleft",xMargin,(1/2)*squareSize)
    elif selectedRoom1 != None and selectedRoom2 == None:
        text(window,"Room "+str(selectedRoom1[0:4])+" selected",int(squareSize*(2/3)),(50,50,50),"topleft",xMargin,(1/2)*squareSize)
    else:
        text(window,"Room "+str(selectedRoom1[0:4])+" selected",int(squareSize*(2/3)),(50,50,50),"topleft",xMargin,(1/2)*squareSize)
        text(window,"Room "+str(selectedRoom2[0:4])+" selected",int(squareSize*(2/3)),(50,50,50),"topleft",xMargin,squareSize)

    if selectedRoom1 != None and selectedRoom2 != None:
        button = variables["buttons"]["fuse"]
        displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Fuse rooms",25,(50,50,50))

    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))
    button = variables["buttons"]["resetFusions"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Reset all fusions",25,(50,50,50))



def FSback(variables,event):
    variables["state"] = "inEditor"


def fuse(variables,event):
    variables["currentMap"].fuseRooms(variables["selectedRooms"][0],variables["selectedRooms"][1])
    variables["state"] =  "inEditor" #we go back to the editor because we need to re-initialize the room buttons because of the new room


def FSreset(variables,event):
    variables["currentMap"].clearAggregatedRooms()
    variables["state"] =  "inEditor" #we go back to the editor because we need to re-initialize the room buttons

fusionSelectInterface = Interface()

fusionSelectInterface.initialize = FSinitialize
fusionSelectInterface.mainDisplay = FSmainDisplay
fusionSelectInterface.mainProcess = FSmainProcess

fusionSelectInterface.buttons += [Button("back",otherInCol,otherOutCol,FSback)]
fusionSelectInterface.buttons += [Button("fuse",but2InCol,but2OutCol,fuse)]
fusionSelectInterface.buttons += [Button("resetFusions",but2InCol,but2OutCol,FSreset)]
