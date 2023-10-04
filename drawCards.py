from constAndStyle import *
from moves import *
from display import *
import pygame

from Entity import *
from Item import *

cardWidth = 59
cardHeight = 86
standardBackGroundColor = (250,230,180)
standardBorderColor = (200,184,144)
descFontName = "data/fonts/Jost/Jost-VariableFont_wght.ttf"


def mainDraw():
    #outPutTest()
    #generateMovesCards()
    #generateItemsCards()
    return


def outPutTest():
    pygame.init()
    #testEntity = Entity(name="Kamul",species="demon",strength=5,dexterity=10,constitution=15,weaponName="claws")
    #cardSurface = getMonsterCard(testEntity,1,5)
    #cardSurface = getMoveCard("feint")
    cardSurface = getItemCard(weapons["rapière"])
    #cardSurface = getItemCard(tools["Verrou Déployable"],borderSize=1,sizeFactor=4)
    seeOutput(cardSurface)


def generateItemsCards():
    global weapons,tools
    for item in buyableWeapons+enemyWeapons+toolsList:
        pygame.init()
        cardSurface = getItemCard(item,sizeFactor=6)
        #seeOutput(cardSurface)
        if item in buyableWeapons:
            folderName = "buyableWeapons"
        elif item in enemyWeapons:
            folderName = "enemyWeapons"
        elif item in toolsList:
            folderName = "tools"
        pygame.image.save(cardSurface,"output/"+folderName+"/"+item.name+"Card.png")



def getItemCard(item,borderSize=1,sizeFactor=7):
    global cardWidth,cardHeight,attacks,defenses
    width = cardWidth*sizeFactor
    height = cardHeight*sizeFactor
    borderSize = borderSize*sizeFactor
    textSize = width//10
    smallTextSize = width//16
    verySmallTextSize = width//20

    #background
    cardSurface = getCardSurface(width,height,borderSize)

    #infos on the requirements
    highestStatReq = "health"
    highestReq = 0
    reqLine = ""
    for stat in item.requirements:
        if item.requirements[stat] > 0:
            reqLine +=  statsAbridged[stat]+" "+str(item.requirements[stat])+"   "
        if item.requirements[stat] > highestReq:
            highestStatReq = stat
            highestReq = item.requirements[stat]
    if reqLine != "":
        reqLine = " prérequis: " + reqLine

    #item name
    textColor = (0,0,0)
    yMargin = borderSize*2
    nameSurface = text(cardSurface,item.name,textSize,textColor,"midtop",width//2,yMargin)
    yMargin += nameSurface.h + borderSize

    #illustration background
    illusSize = 5*height//12
    borderColor = standardBorderColor
    backGroundColor = getWhiterColor(statsColors[highestStatReq],0.8)
    illustrationBackground = getIllustrationBackground(illusSize+6*borderSize,illusSize+2*borderSize,borderSize,backGroundColor,borderColor)
    paste(cardSurface,illustrationBackground,(width//2,yMargin),"midtop")

    #illustration
    if item.imageFile != None:
        illusSize = 5*height//12
        itemIllustration = getImage(item.imageFile,illusSize,illusSize)
        paste(cardSurface,itemIllustration,(width//2,yMargin+borderSize),"midtop")

    yMargin += illustrationBackground.get_height() + borderSize

    #cardType and requirements
    xMargin = borderSize*2
    if type(item) == Weapon:
        cardType = "[arme]"
    elif type(item) == Tool:
        cardType = "[outil]"
    yMargin += text(cardSurface,cardType+reqLine,smallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h

    if type(item) == Weapon:
        yMargin += text(cardSurface,"Dégats: "+str(item.damage),smallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h

    #description
    if item.description != None:
        yMargin += borderSize
        descTextSurface = pygame.Surface((width-4*borderSize,height//3),pygame.SRCALPHA)
        drawTextLines(descTextSurface,item.description,verySmallTextSize,textColor,0.2,descFontName)
        paste(cardSurface,descTextSurface,(xMargin,yMargin),"topleft")

    #price
    text(cardSurface,"prix: "+str(item.price),smallTextSize,textColor,"bottomright",width-2*borderSize,height-2*borderSize,descFontName)


    return cardSurface


def generateMovesCards():
    global attacks, defenses
    for move in secondaryMoves+otherMoves+attacks+defenses:
        pygame.init()
        cardSurface = getMoveCard(move,sizeFactor=6)
        seeOutput(cardSurface)
        pygame.image.save(cardSurface,"output/movesCards/"+move+"Card.png")


def getMoveCard(move,borderSize=1,sizeFactor=7):
    global cardWidth,cardHeight,attacks,defenses
    width = cardWidth*sizeFactor
    height = cardHeight*sizeFactor
    borderSize = borderSize*sizeFactor

    #background
    cardSurface = getCardSurface(width,height,borderSize)

    #move name
    textSize = width//10
    textColor = (0,0,0)
    yMargin = borderSize*2
    nameSurface = text(cardSurface,movesToFr[move],textSize,textColor,"midtop",width//2,yMargin)
    yMargin += nameSurface.h + borderSize

    #illustration background
    illusSize = 5*height//12
    borderColor = standardBorderColor
    backGroundColor = getWhiterColor(movesColors[move],0.9)
    illustrationBackground = getIllustrationBackground(illusSize+6*borderSize,illusSize+2*borderSize,borderSize,backGroundColor,borderColor)
    paste(cardSurface,illustrationBackground,(width//2,yMargin),"midtop")

    #illustration
    moveIllustration = getImage("data/images/"+move+".png",illusSize,illusSize)
    paste(cardSurface,moveIllustration,(width//2,yMargin+borderSize),"midtop")
    yMargin += illustrationBackground.get_height() + borderSize

    smallTextSize = width//16
    verySmallTextSize = width//20
    xMargin = borderSize*2

    #type
    if move in attacks:
        moveType = "[attaque]"
    elif move in defenses or move == "rest":
        moveType = "[défense]"
    elif move in secondaryMoves:
        moveType = "[action secondaire]"
    yMargin += text(cardSurface,moveType,smallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h

    if move in attacks:
        line = "Gagne contre: "+movesToFr[exchangeTable[move]]+" et "+movesToFr[defenseTable[move]]
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h
        line = "Perd contre: "+movesToFr[exchangeLosingTable[move]]
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h
    elif move in defenses:
        line = "Protège contre: "+movesToFr[defenseWinningTable[move][0]]+" et "+movesToFr[defenseWinningTable[move][1]]
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h
        line = "Perd contre: "+movesToFr[defenseLosingTable[move]]
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h
    elif move == "rest":
        line = "Perd contre: n'importe quelle attaque"
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h

    #throwBonus
    if move in attacks:
        yMargin += text(cardSurface,"Bonus de lancé: "+throwBonus[move],verySmallTextSize,textColor,"topleft",xMargin,yMargin,descFontName).h

    #effect text
    yMargin += borderSize
    effectTextSurface = pygame.Surface((width-4*borderSize,height//3),pygame.SRCALPHA)
    drawTextLines(effectTextSurface,"Effet: "+movesEffects[move],verySmallTextSize,textColor,0.2,descFontName)
    paste(cardSurface,effectTextSurface,(xMargin,yMargin),"topleft")
    return cardSurface


def drawTextLines(surface,text,textSize,textColor,overlap=0.0,fontName="default"):
    if fontName == "default":
        font = pygame.font.Font("data/fonts/blackchancery/BLKCHCRY.TTF", textSize)
    else:
        font = pygame.font.Font(fontName,textSize)

    #calculating lines
    maxLineWidth = surface.get_width()
    lineBreaks = [0]
    textLen = len(text)
    done = False
    while not done:
        lineStart = lineBreaks[-1]
        testSurface = font.render(text[lineStart:textLen],True,textColor)
        lineWidth = testSurface.get_width() + 10
        if lineWidth > maxLineWidth:
            for charIndex in range(lineStart+1,textLen):
                testSurface = font.render(text[lineStart:charIndex+1],True,textColor)
                newLineWidth = testSurface.get_width() + 10
                if newLineWidth > maxLineWidth:
                    breakIndex = 1 + findFirstSpaceBefore(text,charIndex)
                    lineBreaks += [breakIndex]
                    break
        else:
            done = True
    lineBreaks += [textLen]

    #drawing
    lineHeight = 0
    for lineIndex in range(len(lineBreaks)-1):
        lineStart = lineBreaks[lineIndex]
        lineEnd = lineBreaks[lineIndex+1]
        lineSurface = font.render(text[lineStart:lineEnd],True,textColor)
        surface.blit(lineSurface,(0,lineHeight))
        lineHeight += lineSurface.get_height()*(1-overlap)


def findFirstSpaceBefore(text,startCharIndex):
    for charIndex in range(startCharIndex,-1,-1):
        if text[charIndex] == " ":
            return charIndex
    return None


def getWhiterColor(color,whiteProportion=0.5):
    return getColorMix([255]*3,color,whiteProportion)

def getDarkerColor(color,blackProportion=0.5):
    return getColorMix([0]*3,color,blackProportion)

def getColorMix(color1,color2,proportion=0.5):
    r = int(color1[0]*proportion + color2[0]*(1-proportion))
    g = int(color1[1]*proportion + color2[1]*(1-proportion))
    b = int(color1[2]*proportion + color2[2]*(1-proportion))
    return [r,g,b]


def getIllustrationBackground(width=59,height=86,borderSize=2,backGroundColor=standardBackGroundColor,borderColor=standardBorderColor):
    return getCardSurface(width,height,borderSize,backGroundColor,borderColor)


def getMonsterCard(entity,borderSize=1,sizeFactor=8):
    global cardWidth,cardHeight,speciesList
    width = cardWidth*sizeFactor
    height = cardHeight*sizeFactor
    borderSize = borderSize*sizeFactor

    #background
    cardSurface = getCardSurface(width,height,borderSize)

    #illustration
    if entity.species in speciesList:
        if entity.species in monsters:
            imageName = "data/images/modern_"+entity.species+".png"
        elif entity.species in nonMonsters:
            imageName = "data/images/icons/"+entity.species+".png"
        illusSize = width//3
        illustration = getImage(imageName,illusSize,illusSize)
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
        moveColor = (0,0,0)
        #moveColor = getDarkerColor(movesColors[label],0.20)
        text(costsTable,label,textSize,moveColor,"center",(width//6)+xStep*index,3*yStep//2)
        text(costsTable,str(costs[index]),textSize*3//2,moveColor,"center",(width//6)+xStep*index,5*yStep//2)

    return costsTable



def getRange(entity,width,height):
    rangeDrawing = pygame.Surface((width+2,height+2),pygame.SRCALPHA)
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
    statsNames = ["strength","dexterity","constitution"]
    xStep = width//12
    for index,statName in enumerate(statsNames):
        recHeight = yCut*stats[index]//18
        pygame.draw.rect(statGraph,statsColors[statName],pygame.Rect(xStep*(1+4*index),yCut-recHeight,xStep*2,recHeight))
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


def getCardSurface(width=59,height=86,borderSize=2,backGroundColor=standardBackGroundColor,borderColor=standardBorderColor):
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



mainDraw()
