from Square import *
from display import *



entityAmount = 0

class Entity():
    def __init__(self,x=None,y=None,name="Anonymous",side="enemy",strength=6,dexterity=6,constitution=6,weaponDamage=15,health=100,criticalHealth=50,infos="",control="AI"):
        global entityAmount
        self.x = x
        self.y = y
        if not (x==None or y==None):
            self.square = Square(x,y)
        else:
            self.square = None
        self.side = side
        self.name = name
        self.control = control
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.weaponDamage = weaponDamage
        self.health = health
        self.criticalHealth = criticalHealth
        self.index = entityAmount
        entityAmount += 1

        self.infos = infos


    @classmethod
    def fromDict(cls,dict):
        return cls(dict["square"]["x"],dict["square"]["y"],dict["name"],dict["side"],dict["strength"],dict["dexterity"],dict["constitution"],dict["weaponDamage"],dict["health"],dict["criticalHealth"],dict["infos"])

    def toJSON(self):
        return {"name":self.name
                ,"side":self.side
                ,"health":self.health,"criticalHealth":self.criticalHealth
                ,"strength":self.strength,"dexterity":self.dexterity,"constitution":self.constitution
                ,"weaponDamage":self.weaponDamage
                ,"square":self.square.toJSON()
                ,"infos":self.infos}

    def display(self,surface,shift,squareSize):
        displayMonster(surface,shift,squareSize,self.square)


    def receiveDamage(self,damage,verbose=True):
        if damage < 0:
            damage = 0
            if verbose:
                print("negative damage changed to 0")

        self.health = max(self.health-damage,0)
