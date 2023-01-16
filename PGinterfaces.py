import pygame



class Button:
    def __init__(self,name="unamed",inColor=[200,200,200],outColor=[100,100,100],function = None):
        self.function = function
        self.name = name
        self.rectangle = [0,0,0,0]
        self.inColor = inColor
        self.outColor = outColor



class Interface:
    def __init__(self,buttons = []):
        self.initialize = None
        self.mainProcess = None
        self.mainDisplay = None
        self.buttons = buttons

    def run(self,surface,variables):
        # we give the functions access to the buttons -> if a button is added later you must add it to the variables
        variables["buttons"] = {}
        for button in self.buttons:
            variables["buttons"][button.name] = button

        variables = self.initialize(variables)
        #must set the allowed event types before running the interface
        running = variables["running"]
        while running:
            variables = self.mainProcess(variables)
            self.mainDisplay(surface,variables)
            pygame.display.update()

            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.display.quit()
                return variables

            for button in self.buttons:
                variables = button.function(variables,event)

            running = variables["running"]

        return variables
