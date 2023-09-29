from constAndStyle import *
from moves import *
from display import *
import pygame

from Entity import *

cardWidth = 59
cardHeight = 86
standardBackGroundColor=(250,230,180)
standardBorderColor=(200,184,144)


def outPutTest():
    pygame.init()
    testEntity = Entity(name="Kamul",species="demon",strength=5,dexterity=10,constitution=15,weaponName="claws")
    cardSurface = getMonsterCard(testEntity,1,5)
    #cardSurface = getMoveCard("feint")
    seeOutput(cardSurface)


def generateMovesCards():
    global attacks, defenses
    for move in attacks+defenses+otherMoves:
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
    if move in attacks:
        moveName = move + " attack"
    else:
        moveName = move
    nameSurface = text(cardSurface,moveName,textSize,textColor,"midtop",width//2,yMargin)
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

    smallTextSize = width//12
    verySmallTextSize = width//16
    xMargin = borderSize*2

    #type
    if move in attacks:
        moveType = "[attack]"
    elif move in defenses:
        moveType = "[defense]"
    else:
        moveType = "[passive]"
    yMargin += text(cardSurface,moveType,smallTextSize,textColor,"topleft",xMargin,yMargin).h

    if move in attacks:
        line = "beats: "+exchangeTable[move]+" attack and "+defenseTable[move]
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin).h
        line = "loses against: "+exchangeLosingTable[move]+" attack"
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin).h
    elif move in defenses:
        line = "protects from: "+defenseWinningTable[move][0]+" and "+defenseWinningTable[move][1]+" attacks"
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin).h
        line = "loses against: "+defenseLosingTable[move]+" attack"
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin).h
    else:
        line = "loses against: any attack"
        yMargin += text(cardSurface,line,verySmallTextSize,textColor,"topleft",xMargin,yMargin).h

    #effect text
    yMargin += borderSize
    effectTextSurface = pygame.Surface((width-4*borderSize,height//3),pygame.SRCALPHA)
    drawTextLines(effectTextSurface,"effect: "+movesEffects[move],verySmallTextSize,textColor,0.2)
    paste(cardSurface,effectTextSurface,(xMargin,yMargin),"topleft")
    return cardSurface


def drawTextLines(surface,text,textSize,textColor,overlap=0.0,fontName="default"):
    if fontName == "default":
        font = pygame.font.Font("data/blackchancery/BLKCHCRY.TTF", textSize)
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


#outPutTest()
generateMovesCards()
