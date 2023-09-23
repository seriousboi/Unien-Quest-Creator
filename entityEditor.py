from constAndStyle import *
from PGinterfaces import *
from display import *
from Entity import *
from editText import *
from copy import copy




def EEinitialize(variables):
    global statsDic,statsTypes
    entity = variables["entity"]
    variables["Informations"] = entity.infos
    statsDic ={"Name":entity.name,"Side":entity.side,"Species":entity.species,"Strength":entity.strength,"Dexterity":entity.dexterity,"Constitution":entity.constitution,"Weapon Damage":entity.weaponDamage,"Health":entity.health,"Critical Health":entity.criticalHealth}
    statsTypes ={"Name":"text","Side":"text","Species":"text","Strength":"number","Dexterity":"number","Constitution":"number","Weapon Damage":"number","Health":"number","Critical Health":"number"}

    squareSize = variables["squareSize"]
    for statName in statsDic:
        if statsTypes[statName] == "text":
            length = 4*squareSize
        elif statsTypes[statName] == "number":
            length = 1*squareSize
        variables["buttons"][statName] = TextBox(statName,squareSize//2,length,squareSize-5,inactiveInColor=butInCol,inactiveOutColor=butOutCol,activeInColor=butPresInCol,activeOutColor=butPresOutCol)
        variables["buttons"][statName].text = str(statsDic[statName])


def EEmainProcess(variables):
    global mapLength,mapWidth
    squareSize = variables["squareSize"]
    xMargin = (mapLength+2/3)*squareSize
    medButWidth = 5*squareSize
    longButWidth = 7*squareSize
    medButHeight = squareSize
    namesWidth = 3*squareSize

    variables["buttons"]["apply"].rectangle = pygame.Rect(xMargin,15.75*squareSize,medButWidth,medButHeight)
    variables["buttons"]["back"].rectangle = pygame.Rect(xMargin,17*squareSize,medButWidth,medButHeight)

    for index,statName in enumerate(statsDic):
        variables["buttons"][statName].x = xMargin+namesWidth+4
        variables["buttons"][statName].y = (index*1.25+1/3)*squareSize
        variables["buttons"][statName].update()

    variables["buttons"]["editInfos"].rectangle = pygame.Rect(xMargin+namesWidth+4,((index+1)*1.25+1/3)*squareSize,4*squareSize,squareSize-5)


def EEmainDisplay(window,variables):
    global mapLength,mapWidth,itemNames
    squareSize = variables["squareSize"]
    shift = variables["shift"]
    xMargin = (mapLength+2/3)*squareSize
    namesWidth = 3*squareSize

    if variables["currentMap"] != None:
        variables["currentMap"].display(window,variables["shift"],squareSize)

    pygame.draw.rect(window,(250,230,180),(mapLength*squareSize,0,8*squareSize,mapWidth*squareSize),0)
    pygame.draw.line(window,(200,184,144),(mapLength*squareSize,0),(mapLength*squareSize,mapWidth*squareSize),6)

    button = variables["buttons"]["apply"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Apply changes",25,(50,50,50))
    button = variables["buttons"]["back"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,"Back",25,(50,50,50))

    for index,statName in enumerate(statsDic):
        variables["buttons"][statName].display(window)
        text(window,statName,squareSize//2,(50,50,50),"topright",xMargin+namesWidth,(index*1.25+1/3)*squareSize)

    button = variables["buttons"]["editInfos"]
    displayButton(window,button.rectangle,2,4,button.inColor,button.outColor,variables["Informations"][0:9]+"...",25,(50,50,50))
    text(window,"Informations",squareSize//2,(50,50,50),"topright",xMargin+namesWidth,((index+1)*1.25+1/3)*squareSize)


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
    entity.species = statsDic["Species"]
    entity.strength = statsDic["Strength"]
    entity.dexterity = statsDic["Dexterity"]
    entity.constitution = statsDic["Constitution"]
    entity.weaponDamage = statsDic["Weapon Damage"]
    entity.health = statsDic["Health"]
    entity.criticalHealth = statsDic["Critical Health"]
    entity.infos = variables["Informations"]


def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def EEeditInfos(variables,event):
    TEvariables = copy(variables)
    TEvariables["text"] = variables["Informations"]
    textEditor.run(variables["window"],TEvariables,"editing entity text")
    variables["Informations"] = TEvariables["text"]
    if TEvariables["state"] == "quitting":
        variables["state"] = "quitting"

entityEditor = Interface()

entityEditor.initialize = EEinitialize
entityEditor.mainDisplay = EEmainDisplay
entityEditor.mainProcess = EEmainProcess

entityEditor.buttons += [Button("editInfos",butInCol,butOutCol,EEeditInfos,activeInColor=butPresInCol,activeOutColor=butPresOutCol)]
entityEditor.buttons += [Button("apply",otherInCol,otherOutCol,EEapply)]
entityEditor.buttons += [Button("back",otherInCol,otherOutCol,EEback)]
