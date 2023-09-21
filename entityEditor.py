from constAndStyle import *
from PGinterfaces import *
from display import *
from Entity import *


def EEinitialize(variables):
    global statsDic,statsTypes
    entity = variables["entity"]
    statsDic ={"Name":entity.name,"Side":entity.side,"Strength":entity.strength,"Dexterity":entity.dexterity,"Constitution":entity.constitution,"Weapon Damage":entity.weaponDamage,"Health":entity.health,"Critical Health":entity.criticalHealth,"Informations":entity.infos}
    statsTypes ={"Name":"text","Side":"text","Strength":"number","Dexterity":"number","Constitution":"number","Weapon Damage":"number","Health":"number","Critical Health":"number","Informations":"text"}

    squareSize = variables["squareSize"]
    for statName in statsDic:
        if statsTypes[statName] == "text":
            length = 4*squareSize
        elif statsTypes[statName] == "number":
            length = 1*squareSize
        variables["buttons"][statName] = TextBox(statName,squareSize//2,length,squareSize-5,inactiveInColor=butInCol,inactiveOutColor=butOutCol,activeInColor=butPresInCol,activeOutColor=butPresOutCol)
        variables["buttons"][statName].text = str(statsDic[statName])


def EEmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]

    if variables["mainVars"]["currentMap"] != None:
        variables["mainVars"]["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["apply"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Apply changes",25,(50,50,50))
    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))

    xMargin = (mapLength+2/3)*squareSize
    namesWidth = 3*squareSize
    for index,statName in enumerate(statsDic):
        variables["buttons"][statName].display(window)
        text(window,statName,squareSize//2,(50,50,50),"topright",xMargin+namesWidth,(index*1.25+1/3)*squareSize)


def EEmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    longButWidth = 7*squareSize
    medButHeight = squareSize

    variables["buttons"]["apply"].rectangle = pygame.Rect(xMargin,15.75*squareSize,medButWidth,medButHeight)
    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)

    namesWidth = 3*squareSize
    for index,statName in enumerate(statsDic):
        variables["buttons"][statName].x = xMargin+namesWidth+4
        variables["buttons"][statName].y = (index*1.25+1/3)*squareSize
        variables["buttons"][statName].update()

def EEback(variables,event):
    variables["state"] = "inEditor"


def EEapply(variables,event):
    for index,statName in enumerate(statsDic):
        statString = variables["buttons"][statName].text
        if statsTypes[statName] == "text":
            statsDic[statName] = statString
        elif statsTypes[statName] == "number" and isNumber(statString):
            if float(statString)%1 == 0:
                stat = int(float(statString))
            else:
                stat = round(float(statString),1)
            statsDic[statName] = stat
        else:
            print("problem")

    entity = variables["entity"]
    entity.name = statsDic["Name"]
    entity.side = statsDic["Side"]
    entity.strength = statsDic["Strength"]
    entity.dexterity = statsDic["Dexterity"]
    entity.constitution = statsDic["Constitution"]
    entity.weaponDamage = statsDic["Weapon Damage"]
    entity.health = statsDic["Health"]
    entity.criticalHealth = statsDic["Critical Health"]
    entity.infos = statsDic["Informations"]



def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


entityEditor = Interface()

entityEditor.initialize = EEinitialize
entityEditor.mainDisplay = EEmainDisplay
entityEditor.mainProcess = EEmainProcess

entityEditor.buttons += [Button("apply",otherInCol,otherOutCol,EEapply)]
entityEditor.buttons += [Button("back",otherInCol,otherOutCol,EEback)]
