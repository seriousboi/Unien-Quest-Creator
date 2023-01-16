from constAndStyle import *
import pygame



def displayRock(window,shift,squareSize,square):
    X,Y = shift
    xPos = square.x*squareSize
    Ypos = square.y*squareSize
    step = squareSize/5

    rocksCenters = []
    rocksRadius = []
    rocksCenters += [(int(X+xPos+step*4),int(Y+Ypos+step*4))]
    rocksRadius += [int(step*1)]
    rocksCenters += [(int(X+xPos+step*2.5),int(Y+Ypos+step*3))]
    rocksRadius += [int(step*2)]
    rocksCenters += [(int(X+xPos+step*1.5),int(Y+Ypos+step*1.5))]
    rocksRadius += [int(step*1.5)]
    rocksCenters += [(int(X+xPos+step*4),int(Y+Ypos+step*1))]
    rocksRadius += [int(step*1)]

    for rockIndex in range(4):
        pygame.draw.circle(window,(130,125,120),rocksCenters[rockIndex],rocksRadius[rockIndex])
        pygame.draw.circle(window,(50,50,50),rocksCenters[rockIndex],rocksRadius[rockIndex],2)



def displayDoor(window,shift,squareSize,frontSquare,backSquare):
    X,Y = shift

    doorWidth = squareSize//5
    doorLenght = (squareSize*6)//5
    #checking if the squares are neighbors
    if frontSquare.x == backSquare.x and (frontSquare.y-backSquare.y)**2 == 1:
        xDrawPos = int(X + (frontSquare.x+1/2)*squareSize - doorLenght/2)
        yDrawPos = int(Y + max(frontSquare.y,backSquare.y)*squareSize - doorWidth/2)
        pygame.draw.rect(window,(193,90,58),(xDrawPos,yDrawPos,doorLenght,doorWidth),0,2)
        pygame.draw.rect(window,(50,50,50),(xDrawPos,yDrawPos,doorLenght,doorWidth),2,2)
    elif frontSquare.y == backSquare.y and (frontSquare.x-backSquare.x)**2 == 1:
        xDrawPos = int(X + max(frontSquare.x,backSquare.x)*squareSize - doorWidth/2)
        yDrawPos = int(Y + (frontSquare.y+1/2)*squareSize - doorLenght/2)
        pygame.draw.rect(window,(193,90,58),(xDrawPos,yDrawPos,doorWidth,doorLenght),0,2)
        pygame.draw.rect(window,(50,50,50),(xDrawPos,yDrawPos,doorWidth,doorLenght),2,2)
    else:
        print("squares are not neighbors",frontSquare,backSquare)



def displayBoard(window,shift,squareSize):
    global mapLength,mapWidth
    X,Y = shift

    pygame.draw.rect(window,(230,214,212),(X,Y,mapLength*squareSize,mapWidth*squareSize),0)

    #list of rooms (x,y,width,length,color)
    rooms = getRooms()

    for room in rooms:
        rectangle = getRectangleFromSquares(shift,room[0],room[1],room[2],room[3],squareSize)
        pygame.draw.rect(window,room[4],rectangle,0)

    drawGrid(window,shift,squareSize)

    for room in rooms:
        if room[0] == 17 and room[1] == 10:
             continue #we skip the odd cropped room

        left = room[0]*squareSize + X
        right = left + room[2]*squareSize
        top = room[1]*squareSize + Y
        bottom = top + room[3]*squareSize

        pygame.draw.line(window,(50,50,50),(left,top),(right,top),2)
        pygame.draw.line(window,(50,50,50),(right,top),(right,bottom),2)
        pygame.draw.line(window,(50,50,50),(right,bottom),(left,bottom),2)
        pygame.draw.line(window,(50,50,50),(left,bottom),(left,top),2)

    pygame.draw.line(window,(50,50,50),(X+17*squareSize,Y+10*squareSize),(X+21*squareSize,Y+10*squareSize),2) #drawing the two missing lines from the weird room
    pygame.draw.line(window,(50,50,50),(X+17*squareSize,Y+10*squareSize),(X+17*squareSize,Y+13*squareSize),2)



def getRectangleFromSquares(shift,xSquare,ySquare,width,length,squareSize):
    X,Y = shift
    #(xSquare,ySquare) is the topleft square of the room in the board
    return (X+xSquare*squareSize,Y+ySquare*squareSize,width*squareSize,length*squareSize)



def drawGrid(window,shift,squareSize):
    global mapLength,mapWidth
    X,Y = shift
    for index in range(1,mapLength):
        pygame.draw.line(window,(50,50,50),(X+index*squareSize,Y),(X+index*squareSize,Y+(mapWidth)*squareSize))

    for index in range(1,mapWidth):
        pygame.draw.line(window,(50,50,50),(X,Y+index*squareSize),(X+(mapLength)*squareSize,Y+index*squareSize))



def displayButton(surface,buttonRectangle,borderWidth,borderCurve,inColor,outColor,message,size,textColor):
    pygame.draw.rect(surface,inColor,buttonRectangle,0,borderCurve)
    pygame.draw.rect(surface,outColor,buttonRectangle,borderWidth,borderCurve)
    x = buttonRectangle[0]+buttonRectangle[2]/2
    y = buttonRectangle[1]+buttonRectangle[3]/2
    text(surface,message,size,textColor,"center",x,y)



def text(surface,message,size,color,anchor,x,y):

    font = pygame.font.Font("data/blackchancery/BLKCHCRY.TTF", size)
    text = font.render(message,True,color)
    area = text.get_rect()
    width = area.width
    height = area.height

    vect= {"topleft":[0,0],
           "bottomleft":[0,-2],
           "topright":[-2,0],
           "bottomright":[-2,-2],
           "midtop":[-1,0],
           "midleft":[0,-1],
           "midbottom":[-1,-2],
           "midright":[-2,-1],
           "center":[-1,-1]}

    x = x + vect[anchor][0]*width/2
    y = y + vect[anchor][1]*height/2

    return surface.blit(text,(x,y))



def getRooms():
    rooms = [(10,7,6,5,(168,148,135)), #big room

    (1,1,4,3,(174,120,87)), #topleft rooms
    (5,1,4,3,(166,82,74)),
    (1,4,4,5,(118,118,123)),
    (5,4,4,5,(162,189,83)),
    (9,1,3,5,(149,188,192)),

    (1,10,4,4,(225,210,127)), #bottomleft rooms
    (1,14,4,4,(160,159,191)),
    (5,10,2,3,(192,222,232)),
    (7,10,2,3,(124,158,150)),
    (5,13,4,5,(188,116,103)),
    (9,13,3,5,(180,158,102)),

    (14,1,3,5,(166,61,40)), #topright rooms
    (17,1,4,4,(179,185,203)),
    (21,1,4,4,(210,172,107)),
    (17,5,4,4,(194,143,64)),
    (21,5,4,4,(205,210,109)),

    (17,10,4,4,(168,172,209)), #bottomright rooms
    (21,10,4,4,(210,189,100)),
    (18,14,3,4,(185,141,96)),
    (21,14,4,4,(124,184,105)),
    (14,13,4,5,(172,126,118)) #must be last to be drawn properly
    ]
    return rooms
