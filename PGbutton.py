import pygame



class Button:
    def __init__(self,name="unamedButton",
    inColor=[200,200,200],outColor=[100,100,100],
    function = None,regularTrigger = True,
    activeInColor=None,activeOutColor=None):

        self.function = function
        self.name = name
        self.rectangle = None
        self.inColor = inColor
        self.outColor = outColor
        self.regularTrigger = regularTrigger

        #doing weird stuff because the class was changed after many object instanciations in the code
        if activeInColor == None:
            self.activeInColor = inColor
        else:
            self.activeInColor = activeInColor
        if activeOutColor == None:
            self.activeOutColor = outColor
        else:
            self.activeOutColor = activeOutColor

        self.inactiveInColor = inColor
        self.inactiveOutColor = outColor
        self.active = False

    def updateColor(self):
        if self.active:
            self.inColor = self.activeInColor
            self.outColor = self.activeOutColor
        else:
            self.inColor = self.inactiveInColor
            self.outColor = self.inactiveOutColor


class TextBox(Button):
    def __init__(self,name="unamedTextBox",
    textSize=20,minWidth=200,minHeight=30,
    hasBackGround=True,hasBorder=True,
    inactiveInColor=[200]*3,inactiveOutColor=[100]*3,
    activeInColor=[245]*3,activeOutColor=[100]*3,
    textColor=[50]*3,fontName = "default",
    multiLines = False,maxLineWidth = None,
    x=None,y=None):

        regularTrigger = False
        function = self.handleEvent
        super().__init__(name,inactiveInColor,inactiveOutColor,function,regularTrigger,activeInColor,activeOutColor)

        self.inactiveInColor = inactiveInColor
        self.inactiveOutColor = inactiveOutColor
        self.activeInColor = activeInColor
        self.activeOutColor = activeOutColor
        self.textColor = textColor
        self.textSize = textSize
        self.text = ""
        self.hasBackGround = hasBackGround
        self.hasBorder = hasBorder
        self.borderWidth = 2
        self.borderCurve = 4
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.x = x
        self.y = y

        if maxLineWidth == None:
            self.maxLineWidth = minWidth

        self.multiLines = multiLines
        self.lineBreaks = [0,0]
        self.cursorPos = 0

        if fontName == "default":
            font = pygame.font.Font("data/fonts/Jost/Jost-VariableFont_wght.ttf", textSize)
        else:
            font = pygame.font.Font(fontName,textSize)
        self.font = font

        self.update()

    def update(self):
        self.updateColor()

        if self.multiLines:
            self.initLineBreaks()

        if self.x != None and self.y != None:
            if (not self.multiLines) or (len(self.lineBreaks)-1 == 1):
                self.textSurface = self.font.render(self.text,True,self.textColor)
                width = min(max(self.minWidth,self.textSurface.get_width()+10),self.maxLineWidth)
                height = max(self.minHeight,self.textSurface.get_height()+10)
            else:
                testSurface = self.font.render(self.text[0:self.lineBreaks[1]],True,self.textColor)
                width = self.maxLineWidth
                height = 5 + (self.minHeight-5)*len(self.lineBreaks)
            anchor = "topleft"
            vect= {"topleft":[0,0],"bottomleft":[0,-2],"topright":[-2,0],"bottomright":[-2,-2],"midtop":[-1,0],"midleft":[0,-1],"midbottom":[-1,-2],"midright":[-2,-1],"center":[-1,-1]}
            x = self.x + vect[anchor][0]*width/2
            y = self.y + vect[anchor][1]*height/2
            self.rectangle = pygame.Rect(x,y,width,height)
        else:
            self.rectangle = None

    def initLineBreaks(self):
        self.lineBreaks = [0]
        done = False
        textLen = len(self.text)
        while not done:
            lineStart = self.lineBreaks[-1]
            testSurface = self.font.render(self.text[lineStart:textLen],True,self.textColor)
            lineWidth = testSurface.get_width() + 10
            if lineWidth > self.maxLineWidth:
                for charIndex in range(lineStart+1,textLen):
                    testSurface = self.font.render(self.text[lineStart:charIndex+1],True,self.textColor)
                    newLineWidth = testSurface.get_width() + 10
                    if newLineWidth > self.maxLineWidth:
                        breakIndex = 1 + findFirstSpaceBefore(self.text,charIndex)
                        self.lineBreaks += [breakIndex]
                        break
            else:
                done = True
        self.lineBreaks += [textLen]

    def handleEvent(self,variables,event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rectangle != None:
            if self.rectangle.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            textLen = len(self.text)
            insertionPos = textLen + self.cursorPos
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:

                    self.text = self.text[0:max(0,insertionPos-1)] + self.text[insertionPos:textLen]
                elif event.key == pygame.K_RIGHT:
                    self.cursorPos = min(0,self.cursorPos+1)
                elif event.key == pygame.K_LEFT:
                    self.cursorPos = max(-len(self.text),self.cursorPos-1)
                else:
                    if event.scancode in keyboardDic:
                        char = keyboardDic[event.scancode]
                        if pygame.key.get_pressed()[pygame.K_RSHIFT] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            if char in toUpperCase:
                                char = toUpperCase[char]
                        self.text = self.text[0:insertionPos] + char + self.text[insertionPos:textLen]
        self.update()

    def display(self,surface):
        if self.x != None and self.y != None:

            if self.hasBackGround:
                pygame.draw.rect(surface,self.inColor,self.rectangle,0,self.borderCurve)
            if self.hasBorder:
                pygame.draw.rect(surface,self.outColor,self.rectangle,self.borderWidth,self.borderCurve)

            if (not self.multiLines) or (len(self.lineBreaks)-1 == 1):
                limitRect = pygame.Surface((self.rectangle.w,self.rectangle.h),pygame.SRCALPHA)
                limitRect.blit(self.textSurface,(5,5))
                surface.blit(limitRect,(self.rectangle.x,self.rectangle.y))
            else:
                for lineIndex in range(len(self.lineBreaks)-1):
                    lineStart = self.lineBreaks[lineIndex]
                    lineEnd = self.lineBreaks[lineIndex+1]
                    lineSurface = self.font.render(self.text[lineStart:lineEnd],True,self.textColor)
                    surface.blit(lineSurface,(self.rectangle.x+5,self.rectangle.y+5+lineIndex*(self.minHeight-5)))


def findFirstSpaceBefore(text,startCharIndex):
    for charIndex in range(startCharIndex,-1,-1):
        if text[charIndex] == " ":
            return charIndex
    return None


keyboardDic = {20: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 51: 'm', 17: 'n', 18: 'o', 19: 'p', 4: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 29: 'w', 27: 'x', 28: 'y', 26: 'z',
               30: '&', 31: 'é', 32: '"', 33: "'", 34: '(', 35: '-', 36: 'è', 37: '_', 38: 'ç', 39: 'à', 45: ')', 46: '=',
               16: ',', 54: ';', 55: ':', 56: '!', 52: 'ù',44:" ",
               98:"0",89:"1",90:"2",91:"3",92:"4",93:"5",94:"6",95:"7",96:"8",97:"9",99:"."}

toUpperCase = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z',
               '&': '1', 'é': '2', '"': '3', "'": '4', '(': '5', '-': '6', 'è': '7', '_': '8', 'ç': '9', 'à': '0', ')': '°', '=': '+',
               ',': '?', ';': '.', ':': '/', '!': '§', 'ù': '%'}
