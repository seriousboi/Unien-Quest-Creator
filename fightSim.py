from diceCalculus import *
from random import choice



class Entity():
    def __init__(self,x,y,name="Anonymous",control="AI",strength=6,dexterity=6,constitution=6,weaponDamage=15,maxHealth=100,index=None):
        self.index = index
        self.x = x
        self.y = y
        self.name = name
        self.control = control
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.weaponDamage = weaponDamage
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.index = index

    def receiveDamage(self,damage,verbose=True):
        if damage < 0:
            damage = 0
            if verbose:
                print("negative damage changed to 0")

        self.health = max(self.health-damage,0)


class fightMove():
    def __init__(self,type,maker,x=None,y=None):
        self.type = type
        if type in ["strong","fast","counter"]:
            self.isAttack = True
            #x and y are the target coordinates
            self.x = x
            self.y = y
        elif type in ["block","dodge","feint"]:
            self.isAttack = False
        else:
            print("/!\   UNKNOWN MOVE   /!\ ")
        self.maker = maker


class Simulation():
    def __init__(self,width=4,height=4,walls=[],obstacles=[],entities=[],script=[]):
        self.width = width
        self.height = height
        self.walls = walls
        self.obstacles = obstacles
        self.entities = entities
        self.state = "choosing"
        self.script = []

    def run(self):
        for index,entity in enumerate(self.entities):
            entity.index = index
        self.drawUnicode()

        while self.state != "quit":

            if self.state == "choosing":
                self.getChoices()
                self.state = "progress"
            elif self.state == "progress":
                self.drawUnicode()
                self.progress()
                userInput = input()
                if userInput == "quit":
                    self.state = "quit"
                else:
                    self.state = "choosing"

    def getChoices(self):
        self.moves = []
        for entity in self.entities:
            if entity.control == "AI":
                self.moves += [fightMove("block",entity)]
            elif entity.control == "script":
                self.moves += [self.script[0]]
                self.script.pop(0)
            elif entity.control == "manual":
                print("choose a move for "+entity.name)
                type = input()
                if type in ["strong","fast","counter"]:
                    print("input target x")
                    x = int(input())
                    print("input target y")
                    y = int(input())
                    move = fightMove(type,entity,x,y)
                else:
                    move = fightMove(type,entity)
                self.moves += [move]

    def progress(self):
        movesProcessed = [False]*len(self.moves)
        for index,move in enumerate(self.moves):
            if not movesProcessed[index]:
                move = self.moves[index]
                if move.isAttack:
                    target = self.getEntityAt(move.x,move.y)
                    if target != None:
                        targetMove = self.moves[target.index]
                        verbose = True

                        makeAttack(move.maker,target,move,targetMove,movesProcessed,verbose)
                movesProcessed[index] = True

    def getEntityAt(self,x,y):
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None

    def drawUnicode(self):
        cellWidth = 3
        cellHeight = 1
        lines = []

        lines += [u'\u250F' + (u'\u2501'*cellWidth +u'\u2533')*(self.width-1) +u'\u2501'*cellWidth + u'\u2513']
        for row in range(self.height-1):
            for step in range(cellHeight):
                lines += [(u'\u2503'+" "*cellWidth)*self.width + u'\u2503']
            lines += [u'\u2523' + (u'\u2501'*cellWidth +u'\u254B')*(self.width-1) +u'\u2501'*cellWidth + u'\u252B']
        for step in range(cellHeight):
            lines += [(u'\u2503'+" "*cellWidth)*self.width + u'\u2503']
        lines += [u'\u2517' + (u'\u2501'*cellWidth +u'\u253B')*(self.width-1) +u'\u2501'*cellWidth + u'\u251B']

        for entity in self.entities:
            line = lines[1 + cellHeight//2 +(cellHeight+1)*entity.y]
            list1 = list(line)
            list1[1 + cellWidth//2 + (cellWidth+1)*entity.x] = entity.name[0]
            lines[1 + cellHeight//2 +(cellHeight+1)*entity.y] = ''.join(list1)

        for line in lines:
            print(line)


def makeAttack(maker,target,move,targetMove,movesProcessed,verbose):
    if not targetMove.isAttack:
        applyDefense(maker,target,move,targetMove,verbose)
        movesProcessed[target.index] = True
    else:
        if targetMove.x == move.maker.x and targetMove.y == move.maker.y:
            applyExchange(maker,target,move,targetMove,verbose)
            movesProcessed[target.index] = True
        else:
            if verbose:
                print("clear shot")


def applyExchange(maker,target,move,targetMove,verbose):
    if move.type != targetMove.type:
        applyDominantExchange(maker,target,move,targetMove,verbose)
    else:
        applyEqualExchange(maker,target,move,targetMove,verbose)


def applyDominantExchange(maker,target,move,targetMove,verbose):
    exchangeTable = {"strong":"fast","fast":"counter","counter":"strong"}
    if exchangeTable[move.type] == exchangeTable[targetMove.type]:
        winner = maker
        loser = target
        winnerMove = move
        loserMove = targetMove
    else:
        winner = target
        loser = maker
        winnerMove = targetMove
        loserMove = move

    winnerRoll = choice(getDiceResults())
    loserRoll = choice(getDiceResults())
    damage = winnerRoll - loserRoll + winner.strength + winner.dexterity - loser.constitution + winner.weaponDamage
    loser.receiveDamage(damage)

    if verbose:
        print(winner.name+" beats "+loser.name+"'s "+loserMove.type+" attack with "+winnerMove.type+" attack")
        print(winner.name+" rolls a",winnerRoll)
        print(loser.name+" rolls a",loserRoll)
        print(loser.name+" receive",damage,"damage")

def applyEqualExchange(maker,target,move,targetMove,verbose):
    if verbose:
        print(maker.name,"and",target.name,move.type,"attacks clash together")
    makerRoll  = choice(getDiceResults())
    targetRoll = choice(getDiceResults())
    difference = makerRoll - targetRoll + max(maker.strength,maker.dexterity) - max(target.strength,target.dexterity)
    if verbose:
        print(maker.name+" rolls a",makerRoll)
        print(target.name+" rolls a",targetRoll)
    if difference == 0:
        maker.receiveDamage(target.weaponDamage - maker.constitution)
        target.receiveDamage(maker.weaponDamage - target.constitution)
        if verbose:
            print("blows are traded")
            print(maker.name+" receive",target.weaponDamage - maker.constitution,"damage")
            print(target.name+" receive",maker.weaponDamage - target.constitution,"damage")
    else:
        if difference > 0:
            winner = maker
            loser = target
        else:
            winner = target
            loser = maker
        damage = abs(difference)+winner.weaponDamage-loser.constitution
        loser.receiveDamage(damage)
        if verbose:
            print(winner.name+" beats "+loser.name)
            print(loser.name+" receive",damage,"damage")


def applyDefense(maker,target,move,targetMove,verbose):
    defenseTable = {"strong":"block","fast":"dodge","counter":"feint"}

    if targetMove.type == defenseTable[move.type]:
        attackingRoll = choice(getDiceResults())
        defendingRoll = choice(getDiceResults())
        damage = attackingRoll - defendingRoll + maker.strength + maker.dexterity - target.constitution + maker.weaponDamage
        target.receiveDamage(damage)
        if verbose:
            print(maker.name+" beats "+target.name+"'s "+targetMove.type+" with "+move.type+" attack")
            print(maker.name+" rolls a",attackingRoll)
            print(target.name+" rolls a",defendingRoll)
            print(target.name+" receive",damage,"damage")
    else:
        if verbose:
            print(target.name,targetMove.type+"s",maker.name+"'s",move.type," attack")


def applayClearShot(maker,target,move,targetMove,verbose):
    print("poop")




sim = Simulation(5,4)
E = Entity(2,0,"Enemy","script")
A = Entity(2,3,"Athos","script")
sim.entities += [E,A]
sim.script = [fightMove("dodge",E,2,3),fightMove("strong",A,2,0)]*10
sim.run()
