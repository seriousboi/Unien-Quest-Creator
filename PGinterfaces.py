from PGbutton import *
import pygame



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
