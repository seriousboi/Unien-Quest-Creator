from Square import *
from display import *



entityAmount = 0

class Entity():
    def __init__(self,x=None,y=None,
                 name="Anonymous",side="enemy",species="Unkown",
                 strength=6,dexterity=6,constitution=6,
                 weaponName="unkown weapon",weaponDamage=15,
                 stamina=50,strongAtkCost=10,fastAtkCost=10,counterAtkCost=10,
                 health=100,criticalHealth=50,
                 range="normal",infos="",control="AI"):
        global entityAmount
        self.x = x
        self.y = y
        if not (x==None or y==None):
            self.square = Square(x,y)
        else:
            self.square = None
        self.name = name
        self.side = side
        self.species = species
        self.control = control
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.weaponName = weaponName
        self.weaponDamage = weaponDamage
        self.stamina = stamina
        self.strongAtkCost = strongAtkCost
        self.fastAtkCost = fastAtkCost
        self.counterAtkCost = counterAtkCost
        self.health = health
        self.criticalHealth = criticalHealth
        self.range = range
        self.index = entityAmount
        entityAmount += 1

        self.infos = infos


    @classmethod
    def fromDict(cls,dict):
        return cls(dict["square"]["x"],dict["square"]["y"],
                   dict["name"],dict["side"],dict["species"],
                   dict["strength"],dict["dexterity"],dict["constitution"],
                   dict["weaponName"],dict["weaponDamage"],
                   dict["stamina"],dict["strongAtkCost"],dict["fastAtkCost"],dict["counterAtkCost"],
                   dict["health"],dict["criticalHealth"],
                   dict["range"],dict["infos"])

    def toJSON(self):
        return {"name":self.name,"side":self.side,"species":self.species,
                "strongAtkCost":self.strongAtkCost,"fastAtkCost":self.fastAtkCost,"counterAtkCost":self.counterAtkCost,
                "stamina":self.stamina,"health":self.health,"criticalHealth":self.criticalHealth,
                "strength":self.strength,"dexterity":self.dexterity,"constitution":self.constitution,
                "weaponName":self.weaponName,"weaponDamage":self.weaponDamage,"range":self.range,
                "square":self.square.toJSON(),
                "infos":self.infos}

    def display(self,surface,shift,squareSize,index=None):
        image = None
        speciesList = ["orc","goblin","skeleton","zombie","mummy","fimir","warrior","demon"]
        if self.species in speciesList:
            image = pygame.image.load("data/images/"+self.species+".png")
        displayMonster(surface,shift,squareSize,self.square,index,image)


    def receiveDamage(self,damage,verbose=True):
        if damage < 0:
            damage = 0
            if verbose:
                print("negative damage changed to 0")

        self.health = max(self.health-damage,0)
