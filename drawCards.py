from constAndStyle import *
from display import *
import pygame

from Entity import *

cardWidth = 59
cardHeight = 86


def outPutTest():
    pygame.init()
    testEntity = Entity(name="Kamir",species="demon",strength=5,dexterity=10,constitution=15,weaponName="claws")
    cardSurface = getMonsterCard(testEntity,1,6)
    seeOutput(cardSurface)


def getMonsterCard(entity,borderSize=2,sizeFactor=8):
    global cardWidth,cardHeight,speciesList
    width = cardWidth*sizeFactor
    height = cardHeight*sizeFactor
    borderSize = borderSize*sizeFactor

    #background
    cardSurface = getCardSurface(width,height,borderSize)

    #illustration
    if entity.species in speciesList:
        imageName = entity.species
    else:
        imageName = "monster"
    illusSize = width//3
    illustration = getImage("data/images/modern_"+imageName+".png",illusSize,illusSize)
    paste(cardSurface,illustration,(width-borderSize*2,borderSize*2),"topright")

    #name
    textSize = width//10
    textColor = (0,0,0)
    xMargin = borderSize*2
    yMargin = borderSize*4
    nameSurface = text(cardSurface,entity.name,textSize,textColor,"topleft",xMargin,yMargin)
    yMargin += nameSurface.h + 4*borderSize

    #species,healths,stamina
    smallTextSize = width//12
    verySmallTextSize = width//16
    infos = ["["+entity.species+"]","health: "+str(entity.health),
             "regen ceiling: "+str(entity.criticalHealth),"stamina: "+str(entity.stamina)]
    for index,info in enumerate(infos):
        print(info)
        yMargin += text(cardSurface,info,smallTextSize,textColor,"topleft",xMargin,yMargin).h + borderSize

    #stats
    statGraph = getStatGraph(entity,width//3,11*width//20,verySmallTextSize)
    paste(cardSurface,statGraph,(width-borderSize*2,1*height//4),"topright")

    #range
    drawingSize = width//3
    rangeDrawing = getRange(entity,drawingSize,drawingSize)
    paste(cardSurface,rangeDrawing,(width-borderSize*2,height-borderSize*2),"bottomright")
    text(cardSurface,"range",verySmallTextSize,textColor,"midbottom",width-borderSize*2-drawingSize//2,height-borderSize*2-drawingSize)

    #stamina costs
    tableHeight = width//3
    costsTable = getCosts(entity,9*width//16,tableHeight,verySmallTextSize)
    yPos = height-borderSize*2
    paste(cardSurface,costsTable,(borderSize*2,yPos),"bottomleft")
    yMargin = yPos - (tableHeight + 2*borderSize)

    #weapon,weaponDamage
    infos = ["weapon damage: "+str(entity.weaponDamage),"weapon: "+entity.weaponName]
    for index,info in enumerate(infos):
        print(info)
        yMargin += -text(cardSurface,info,smallTextSize,textColor,"bottomleft",xMargin,yMargin).h + borderSize


    return cardSurface


def getCosts(entity,width,height,textSize):
    costsTable = pygame.Surface((width+1,height+1),pygame.SRCALPHA)
    xStep = width//3
    yStep = height//3
    for index in range(4):
        pygame.draw.line(costsTable,(50,50,50),(0,yStep*index),(width,yStep*index),2)
    for index in range(4):
        if index in [1,2]:
            hStart = yStep
        else:
            hStart = 0
        pygame.draw.line(costsTable,(50,50,50),(xStep*index,hStart),(xStep*index,3*yStep),2)

    text(costsTable,"attack costs",textSize,(0,0,0),"center",width//2,yStep//2)
    labels = ["strong","fast","counter"]
    costs = [entity.strongAtkCost,entity.fastAtkCost,entity.counterAtkCost]
    for index,label in enumerate(labels):
        text(costsTable,label,textSize,(0,0,0),"center",(width//6)+xStep*index,3*yStep//2)
        text(costsTable,str(costs[index]),textSize*3//2,(0,0,0),"center",(width//6)+xStep*index,5*yStep//2)

    return costsTable



def getRange(entity,width,height):
    rangeDrawing = pygame.Surface((width+1,height+1),pygame.SRCALPHA)
    xStep = width//3
    yStep = height//3
    topleft = (0,0)
    midtop1 = (1*xStep,0*yStep)
    midtop2 = (2*xStep,0*yStep)
    topright = (3*xStep,0*yStep)
    midright = (3*xStep,1*yStep)
    bottomright = (3*xStep,2*yStep)
    midbottom2 = (2*xStep,2*yStep)
    bottomBottomright = (2*xStep,3*yStep)
    bottomBottomleft = (1*xStep,3*yStep)
    midbottom1 = (1*xStep,2*yStep)
    bottomleft = (0*xStep,2*yStep)
    midleft = (0*xStep,1*yStep)

    contour=[topleft,topright,bottomright,midbottom2,bottomBottomright,bottomBottomleft,midbottom1,bottomleft]
    for index in range(len(contour)):
        pygame.draw.line(rangeDrawing,(50,50,50),contour[index-1],contour[index],2)

    xMiniStep = width//12
    yMiniStep = height//12
    point = (1*xStep+2*xMiniStep,2*yStep+1*yMiniStep)
    leftBase = (1*xStep+1*xMiniStep,2*yStep+3*yMiniStep)
    rightBase = (1*xStep+3*xMiniStep,2*yStep+3*yMiniStep)

    contour = [point,leftBase,rightBase]
    for index in range(len(contour)):
        pygame.draw.line(rangeDrawing,(50,50,50),contour[index-1],contour[index],2)

    for points in [[midtop1,midbottom1],[midtop2,midbottom2],[midleft,midright],[midbottom1,midbottom2]]:
        pygame.draw.line(rangeDrawing,(100,100,100),points[0],points[1],1)

    return rangeDrawing


def getStatGraph(entity,width,height,textSize):
    global strengthColor ,dexterityColor ,constitutionColor
    statGraph = pygame.Surface((width+1,height+1),pygame.SRCALPHA)
    labels = ["str","dex","con"]
    stats = [entity.strength,entity.dexterity,entity.constitution]
    xStep = width//6
    for index,label in enumerate(labels):
        ySpace = text(statGraph,str(stats[index]),textSize*3//2,(0,0,0),"midbottom",xStep*(1+2*index),height).h - height//12
        ySpace += text(statGraph,label,textSize,(0,0,0),"midbottom",xStep*(1+2*index),height-ySpace).h
    yCut = height - ySpace - 2
    pygame.draw.line(statGraph,(50,50,50),(0,yCut), (width,yCut))
    colors = [strengthColor,dexterityColor,constitutionColor]
    xStep = width//12
    for index,color in enumerate(colors):
        recHeight = yCut*stats[index]//18
        pygame.draw.rect(statGraph,color,pygame.Rect(xStep*(1+4*index),yCut-recHeight,xStep*2,recHeight))
    return statGraph


def getImage(fileName,width,height,withBorder=False,borderSize=2):
    image = pygame.image.load(fileName)
    image = pygame.transform.scale(image,(width,height))
    if withBorder:
        pygame.draw.rect(image,(0,0,0),pygame.Rect(0,0,width,height),borderSize)
    return image


def paste(target,surface,pos,anchor="topleft"):
    vect= {"topleft":[0,0],
           "bottomleft":[0,-2],
           "topright":[-2,0],
           "bottomright":[-2,-2],
           "midtop":[-1,0],
           "midleft":[0,-1],
           "midbottom":[-1,-2],
           "midright":[-2,-1],
           "center":[-1,-1]}
    x = pos[0] + vect[anchor][0]*surface.get_width()//2
    y = pos[1] + vect[anchor][1]*surface.get_height()//2
    target.blit(surface,(x,y))


def getCardSurface(width=59,height=86,borderSize=2,backGroundColor=(250,230,180),borderColor=(200,184,144),):
    cardSurface = pygame.Surface((width,height),pygame.SRCALPHA)
    pygame.draw.rect(cardSurface,backGroundColor,pygame.Rect(0,0,width,height))
    pygame.draw.rect(cardSurface,borderColor,pygame.Rect(0,0,width,height),borderSize)
    return cardSurface


def seeOutput(surface):
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.QUIT])

    width = surface.get_width()
    height = surface.get_height()
    window = pygame.display.set_mode((width,height))
    window.blit(surface,(0,0))

    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return


outPutTest()
