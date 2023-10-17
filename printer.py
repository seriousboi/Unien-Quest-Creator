from drawCards import seeOutput
import pygame
import glob


def printerMain():
    #outputSheets('output/buyableWeapons/')
    #outputSheets('output/enemyWeapons/')
    #outputSheets('output/movesCards/')
    return


def outputSheets(folderPath):
    sheets = getImageFromCardFolder(folderPath)
    for index,sheet in enumerate(sheets):
        pygame.init()
        saveName = folderPath+"sheet"+str(index+1)+".png"
        pygame.image.save(sheet,saveName)


def getImageFromCardFolder(folderPath):
    #créer une image en concaténant les images des cartes (par paquet de 9)
    formula = folderPath+"*.png"
    fileNames = glob.glob(formula)

    cardAmount = len(fileNames)
    cardPacks = [[]]
    packIndex = 0
    cardPack = cardPacks[0]
    for cardFile in fileNames:
        if len(cardPack) == 9:
            cardPacks += [[]]
            packIndex += 1
            cardPack = cardPacks[packIndex]
        if cardFile[-8:] == "Card.png":
            cardImage = pygame.image.load(cardFile)
            cardPack += [cardImage]

    packsAmount = len(cardPacks)
    sheets = []

    if len(cardPacks[0]) == 0:
        return sheets

    for packIndex in range(packsAmount):
        cardPack = cardPacks[packIndex]
        cardWidth = cardPack[0].get_width()
        width = cardWidth*3
        cardHeight = cardPack[0].get_height()
        height = cardHeight*3

        sheetSurface = pygame.Surface((width,height),pygame.SRCALPHA)

        for xIndex in range(3):
            for yIndex in range(3):
                imageIndex = xIndex + yIndex*3
                if imageIndex < len(cardPack):
                     sheetSurface.blit(cardPack[imageIndex],(xIndex*cardWidth,yIndex*cardHeight))
        sheets += [sheetSurface]

    return sheets

printerMain()
