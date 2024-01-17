from constAndStyle import *
from drawCards import *


sheetWidth = 210
sheetHeight = 148


def main():
    pygame.init()
    adventurerSheet = getHeroSheet()
    seeOutput(adventurerSheet)
    pygame.image.save(adventurerSheet,"output/adventurerSheet/emptySheet.png")
    pygame.quit()



def getHeroSheet(sizeFactor = 6):
    global sheetWidth,sheetHeight
    width = sheetWidth*sizeFactor
    height = sheetHeight*sizeFactor
    spaceSize = width//100

    sheetSurface = pygame.Surface((width,height),pygame.SRCALPHA)
    #background
    #backGroundColor = (255,255,255)
    #pygame.draw.rect(sheetSurface,backGroundColor,pygame.Rect(0,0,width,height))

    textSize = width//30
    smallTextSize = width//40
    verySmallTextSize = width//50
    textColor = (0,0,0)

    #leftside text fields
    xMargin = spaceSize
    yMargin = spaceSize
    yMargin += text(sheetSurface,"Nom:",textSize,textColor,"topleft",xMargin,yMargin).h
    yMargin += spaceSize
    yMargin += text(sheetSurface,"Espèce:",textSize,textColor,"topleft",xMargin,yMargin).h
    yMargin += spaceSize
    leftYMargin = yMargin

    #stat table
    statTableX = width - spaceSize
    statTableY = spaceSize
    statTable = getStatTable(2*width//3,height//4,smallTextSize)
    paste(sheetSurface,statTable,(statTableX,statTableY),"topright")

    yMargin = statTableY+statTable.get_height()+spaceSize

    #affinity
    text(sheetSurface,"Affinité:",textSize,textColor,"topleft",statTableX-(5*statTable.get_width()//6),yMargin)

    #gauges
    gaugesSurface =  getGauges(statTable.get_width()//2,height//4,smallTextSize)
    paste(sheetSurface,gaugesSurface,(width-spaceSize,yMargin),"topright")

    #body stats
    #yMargin = leftYMargin + spaceSize*4
    yMargin += text(sheetSurface,"Vie:",textSize,textColor,"topleft",xMargin,yMargin).h
    yMargin += spaceSize
    yMargin += text(sheetSurface,"Endurance:",textSize,textColor,"topleft",xMargin,yMargin).h
    yMargin += spaceSize
    yMargin += text(sheetSurface,"Régénération:",textSize,textColor,"topleft",xMargin,yMargin).h
    yMargin += spaceSize
    yMargin += text(sheetSurface,"Charge maximale:",textSize,textColor,"topleft",xMargin,yMargin).h


    #equipements
    equipementsRecHeight = (height//3)*1.2
    equipementsRecWidth = (2*width//3)*0.9
    yMargin = height - equipementsRecHeight -spaceSize
    pygame.draw.rect(sheetSurface,(50,50,50),pygame.Rect(xMargin,yMargin,equipementsRecWidth,equipementsRecHeight),2,10)
    xMargin += spaceSize
    yMargin += spaceSize
    yMargin += text(sheetSurface,"Équipements:",textSize,textColor,"topleft",xMargin,yMargin).h

    #range drawing
    rangeIllusSize = height//4
    rangeIllusX = width - (width-equipementsRecWidth-spaceSize)/2
    rangeIllusY = height-2*spaceSize
    rangeIllus = getRange(None,rangeIllusSize,rangeIllusSize)
    paste(sheetSurface,rangeIllus,(rangeIllusX,rangeIllusY),"midbottom")
    text(sheetSurface,"Portée",smallTextSize,textColor,"midbottom",rangeIllusX,rangeIllusY-rangeIllusSize-spaceSize)
    return sheetSurface


def getGauges(width,height,textSize,lineWidth = 2):
    global statsColors,statsAbridged
    gaugesSurface = pygame.Surface((width+2,height+2),pygame.SRCALPHA)

    Hstep = width//3
    Vstep = height//3
    for columnIndex in range(4):
        pygame.draw.line(gaugesSurface,(50,50,50),(Hstep*columnIndex,Vstep),(Hstep*columnIndex,height),lineWidth)
    for lineIndex in range(1,4):
        pygame.draw.line(gaugesSurface,(50,50,50),(0,Vstep*lineIndex),(width,Vstep*lineIndex),lineWidth)

    for index,statName in enumerate(["intelligence","perception","charisma"]):
        text(gaugesSurface,statsAbridged[statName],textSize,statsColors[statName],"center",(index+1/2)*Hstep,1.5*Vstep,descFontName).h

    textColor = (0,0,0)
    text(gaugesSurface,"Jauges",textSize,textColor,"midbottom",width//2,Vstep)
    return gaugesSurface

def getStatTable(width,height,textSize,lineWidth = 2):
    global skillStats, statsToFr, statsAbridged
    tableSurface = pygame.Surface((width+2,height+2),pygame.SRCALPHA)
    textColor = (0,0,0)

    Hstep = width//6
    for columnIndex in range(7):
        pygame.draw.line(tableSurface,(50,50,50),(Hstep*columnIndex,0),(Hstep*columnIndex,height),lineWidth)

    Vstep = height//3
    for lineIndex in range(4):
        pygame.draw.line(tableSurface,(50,50,50),(0,Vstep*lineIndex),(width,Vstep*lineIndex),lineWidth)

    for index,statName in enumerate(skillStats):
        Yspace = text(tableSurface,statsToFr[statName],textSize,textColor,"midtop",(index+1/2)*Hstep,0).h
        Yspace = Yspace*0.8
        text(tableSurface,statsAbridged[statName],textSize,statsColors[statName],"midtop",(index+1/2)*Hstep,Yspace,descFontName).h

    return tableSurface

main()
