import pygame



class Button:
    def __init__(self,name="unamedButton",inColor=[200,200,200],outColor=[100,100,100],function = None,regularTrigger = True,activeInColor=None,activeOutColor=None):
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



class Interface:
    def __init__(self):
        self.initialize = None
        self.mainProcess = None
        self.mainDisplay = None
        self.buttons = []

    def run(self,surface,variables,state):
        # we give the functions access to the buttons -> if a button is added later you must add it to the variables
        initialState = state
        variables["state"] = state
        variables["buttons"] = {}
        for button in self.buttons:
            variables["buttons"][button.name] = button

        self.initialize(variables)
        #must set the allowed event types before running the interface
        while variables["state"] == initialState:
            self.mainProcess(variables)
            self.mainDisplay(surface,variables)
            pygame.display.update()

            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                variables["state"] = "quitting"
                return

            for button in variables["buttons"].values():
                if button.regularTrigger == True and button.rectangle != None:
                    if event.type == pygame.MOUSEBUTTONDOWN and button.rectangle.collidepoint(event.pos):
                        button.function(variables,event)
                else:
                    button.function(variables,event)

        return



class TextBox(Button):
    def __init__(self,name="unamedTextBox",textSize=20,minWidth=200,minHeight=30,hasBackGround=True,hasBorder=True,inactiveInColor=[200]*3,inactiveOutColor=[100]*3,activeInColor=[245]*3,activeOutColor=[100]*3,textColor=[50]*3,fontName = "default",x=None,y=None):

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

        if fontName == "default":
            font = pygame.font.Font("data/blackchancery/BLKCHCRY.TTF", textSize)
        else:
            font = pygame.font.Font(fontName,textSize)
        self.font = font

        self.update()

    def update(self):
        self.updateColor()

        self.textSurface = self.font.render(self.text,True,self.textColor)
        if self.x != None and self.y != None:
            width = max(self.minWidth,self.textSurface.get_width()+10)
            height = max(self.minHeight,self.textSurface.get_height()+10)
            anchor = "topleft"
            vect= {"topleft":[0,0],"bottomleft":[0,-2],"topright":[-2,0],"bottomright":[-2,-2],"midtop":[-1,0],"midleft":[0,-1],"midbottom":[-1,-2],"midright":[-2,-1],"center":[-1,-1]}
            x = self.x + vect[anchor][0]*width/2
            y = self.y + vect[anchor][1]*height/2
            self.rectangle = pygame.Rect(x,y,width,height)
        else:
            self.rectangle = None

    def handleEvent(self,variables,event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rectangle != None:
            if self.rectangle.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.scancode in keyboardDic:
                        char = keyboardDic[event.scancode]
                        if pygame.key.get_pressed()[pygame.K_RSHIFT] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            char = toUpperCase[char]
                        self.text += char
        self.update()

    def display(self,surface):
        if self.x != None and self.y != None:

            if self.hasBackGround:
                pygame.draw.rect(surface,self.inColor,self.rectangle,0,self.borderCurve)
            if self.hasBorder:
                pygame.draw.rect(surface,self.outColor,self.rectangle,self.borderWidth,self.borderCurve)
            surface.blit(self.textSurface,(self.rectangle.x+5, self.rectangle.y+5))



keyboardDic = {20: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 51: 'm', 17: 'n', 18: 'o', 19: 'p', 4: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 29: 'w', 27: 'x', 28: 'y', 26: 'z', 30: '&', 31: 'é', 32: '"', 33: "'", 34: '(', 35: '-', 36: 'è', 37: '_', 38: 'ç', 39: 'à', 45: ')', 46: '=', 16: ',', 54: ';', 55: ':', 56: '!', 52: 'ù'}
toUpperCase = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z', '&': '1', 'é': '2', '"': '3', "'": '4', '(': '5', '-': '6', 'è': '7', '_': '8', 'ç': '9', 'à': '0', ')': '°', '=': '+', ',': '?', ';': '.', ':': '/', '!': '§', 'ù': '%'}
