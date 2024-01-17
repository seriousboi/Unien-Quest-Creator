from constAndStyle import *
from moves import counterColor
from drawCards import *


sheetWidth = 105
sheetHeight = 148


def main():
    pygame.init()
    player = True
    stateSheet = getStateSheet(player)
    seeOutput(stateSheet)
    pygame.image.save(stateSheet,"output/adventurerSheet/adventurerSateSheet.png")

    pygame.init()
    player = False
    stateSheet = getStateSheet(player)
    seeOutput(stateSheet)
    pygame.image.save(stateSheet,"output/adventurerSheet/enemyStateSheet.png")

    pygame.quit()


def getStateSheet(player = True,sizeFactor = 6,):
    global sheetWidth,sheetHeight
    width = sheetWidth*sizeFactor
    height = sheetHeight*sizeFactor
    spaceSize = width//100

    sheetSurface = pygame.Surface((width,height),pygame.SRCALPHA)

    #background
    #backGroundColor = (255,255,255)
    #pygame.draw.rect(sheetSurface,backGroundColor,pygame.Rect(0,0,width,height))

    textSize = width//15
    smallTextSize = width//20
    verySmallTextSize = width//25
    textColor = (0,0,0)

    #stat memos
    bonusHeight = 9*height/24
    attackBonuses = getAttackBonuses(width -2*spaceSize,bonusHeight,smallTextSize)

    paste(sheetSurface,attackBonuses,(width-spaceSize,0),"topright")

    #tracking columns
    trackHeight = height - (bonusHeight+spaceSize)
    trackColsSurface = getTrackingCols(width,trackHeight,textSize,player)
    vSpacesAmount = 3
    paste(sheetSurface,trackColsSurface,(0,bonusHeight+vSpacesAmount*spaceSize),"topleft")

    return sheetSurface


def getTrackingCols(width,height,textSize,player=True,lineWidth = 2):
    global statsColors,statsAbridged
    trackColsSurface = pygame.Surface((width+2,height+2),pygame.SRCALPHA)

    if player:
        texts = ["PV",statsAbridged["perception"],statsAbridged["charisma"]]
        colors = [statsColors["health"],statsColors["perception"],statsColors["charisma"]]
    else:
        texts = ["PV",statsAbridged["stamina"]]
        colors = [statsColors["health"],statsColors["stamina"]]


    nbCols = len(texts)
    Hstep = width/nbCols
    for index in range (nbCols-1):
        pygame.draw.line(trackColsSurface,(50,50,50),((1+index)*Hstep,0),((1+index)*Hstep,height),lineWidth)

    for index in range(nbCols):
        text(trackColsSurface,texts[index],textSize,colors[index],"midtop",(0.5+index)*Hstep,0,descFontName)
    return trackColsSurface


def getAttackBonuses(width,height,textSize,lineWidth = 2):
    global statsColors,statsAbridged
    bonusesSurface = pygame.Surface((width+2,height+2),pygame.SRCALPHA)
    spaceSize = width/65
    Hstep = (width-spaceSize)/5
    Vstep = height/5

    xShift = spaceSize
    for columnIndex in range(2,6):
        pygame.draw.line(bonusesSurface,(50,50,50),(xShift+Hstep*columnIndex,Vstep),(xShift+Hstep*columnIndex,height),lineWidth)
    for lineIndex in range(1,6):
        pygame.draw.line(bonusesSurface,(50,50,50),(xShift+Hstep*2,Vstep*lineIndex),(xShift+Hstep*5,Vstep*lineIndex),lineWidth)

    textColor = (0,0,0)
    text(bonusesSurface,"bonus d'attaque",textSize,textColor,"midbottom",xShift+3.5*Hstep,Vstep,descFontName)
    text(bonusesSurface,"+ arme",textSize,textColor,"midright",xShift+Hstep*2 - spaceSize,Vstep*4.5,descFontName)

    attacks = ["forte","rapide","contre"]
    texts = [statsAbridged["strength"],statsAbridged["dexterity"],""]
    colors = [statsColors["strength"],statsColors["dexterity"],(0,0,0)]
    for index in range(3):
        text(bonusesSurface,attacks[index],textSize,textColor,"center",xShift+(2.5+index)*Hstep,Vstep*1.5,descFontName)
        text(bonusesSurface,texts[index],textSize,colors[index],"center",xShift+(2.5+index)*Hstep,Vstep*2.5,descFontName)

    verySmallTextSize = 5*textSize//7
    smallTextSize = 6*textSize//7
    text(bonusesSurface,"min +50%",verySmallTextSize,textColor,"midbottom",xShift+(2.5+index)*Hstep,Vstep*2.5,descFontName)
    text(bonusesSurface,statsAbridged["strength"],smallTextSize,statsColors["strength"],"topright",xShift-spaceSize/2 + (2.5+index)*Hstep,Vstep*2.5,descFontName)
    text(bonusesSurface,statsAbridged["dexterity"],smallTextSize,statsColors["dexterity"],"topleft",xShift+spaceSize/2 + (2.5+index)*Hstep,Vstep*2.5,descFontName)


    for columnIndex in range(0,3):
        pygame.draw.line(bonusesSurface,(50,50,50),(Hstep*columnIndex,Vstep),(Hstep*columnIndex,height-Vstep),lineWidth)
    for lineIndex in range(1,5):
        pygame.draw.line(bonusesSurface,(50,50,50),(0,Vstep*lineIndex),(Hstep*2,Vstep*lineIndex),lineWidth)

    names = ["défense","arme"]
    texts = [statsAbridged["constitution"],""]
    colors = [statsColors["constitution"],(textColor)]
    for index in range(2):
        text(bonusesSurface,names[index],textSize,textColor,"center",(0.5+index)*Hstep,Vstep*1.5,descFontName)
        text(bonusesSurface,texts[index],smallTextSize,colors[index],"midtop",(0.5+index)*Hstep,Vstep*2.5,descFontName)
    text(bonusesSurface,"3/4",verySmallTextSize,textColor,"midbottom",(0.5+0)*Hstep,Vstep*2.5,descFontName)

    return bonusesSurface


main()
