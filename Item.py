


class Item():
    def __init__(self,name,price,requirements=None,description=None):
        self.name = name
        self.price = price
        self.description = description
        self.imageFile = None

        self.requirements = {"strength":0,"dexterity":0,"constitution":0,
                             "intelligence":0,"perception":0,"charisma":0}
        if requirements != None:
            for stat in requirements:
                self.requirements[stat] = requirements[stat]


class Weapon(Item):
    def __init__(self,name,price,damage,requirements=None,description=None):
        super().__init__(name,price,requirements,description)
        self.damage = damage


class Tool(Item):
    def __init__(self,name,price,requirements=None,description=None):
        super().__init__(name,price,requirements,description)



buyableWeapons = []
buyableWeapons += [Weapon("Mains Nues",0,5)]
buyableWeapons += [Weapon("Poignard",26,9,{"dexterity":2})]
buyableWeapons += [Weapon("Epée courte",30,10,{"strength":5})]
buyableWeapons += [Weapon("Sabre",33,13,{"dexterity":7})]
buyableWeapons += [Weapon("Hachoir Large",52,15,{"strength":9})]
buyableWeapons += [Weapon("Lance",60,17,{"dexterity":11})]
buyableWeapons += [Weapon("Epée Longue",75,19,{"strength":12})]
buyableWeapons += [Weapon("Rapière",79,25,{"dexterity":16})]
buyableWeapons += [Weapon("Hache de Combat",80,25,{"strength":18})]
buyableWeapons += [Weapon("Faux",84,31,{"dexterity":20})]
buyableWeapons += [Weapon("Marteau de Guerre",91,33,{"strength":24})]
buyableWeapons += [Weapon("Sabre Oriental",163,39,{"dexterity":27})]
buyableWeapons += [Weapon("Tueuse de Dragon",140,40,{"strength":30})]
enemyWeapons = []
enemyWeapons += [Weapon("Sabre Sauvage",8,19,{"strength":13})]
enemyWeapons += [Weapon("Hachoir Rouillé",5,22,{"strength":18})]
enemyWeapons += [Weapon("Fléau",9,16,{"dexterity":11})]
enemyWeapons += [Weapon("Stylet",9,21,{"dexterity":17})]
enemyWeapons += [Weapon("Sabre Rouillé",4,13,{"dexterity":8})]
enemyWeapons += [Weapon("Hachette",6,18,{"strength":14})]
enemyWeapons += [Weapon("Double Hache",16,23,{"dexterity":16})]
enemyWeapons += [Weapon("Faux Spectrale",12,29,{"dexterity":21})]
enemyWeapons += [Weapon("Crocs Nécrosants",0,35,{"constitution":13})]


weaponsList = buyableWeapons + enemyWeapons

weapons = {}
for weapon in weaponsList:
    weapons[weapon.name] = weapon
    weapon.imageFile = "data/images/icons/"+weapon.name+".png"


toolsList = []
toolsList += [Tool("Verrou Déployable",27,{"strength":8},"Peut être posé sur une porte, la porte reste fermée jusqu'à ce que le verrou soit détruit. Le verrou est considéré comme une entité avec 20 PV et 40 CONST qui utilise toujours la garde.")]
toolsList += [Tool("Piège à Loup",30,{"dexterity":8},"Piège déployable sur une dalle. Immobilise une entité pour deux tours et infligle 2 x DEX du déployeur en dégats.")]
toolsList += [Tool("Pierre de Réflexion",26,{"intelligence":8},"Deux exemplaires par achat. Utilisable lors des situations de tensions. Ajoute deux minutes de temps au chronomètre.")]
toolsList += [Tool("Loupe",29,{"perception":8},"Deux exemplaires par achat. Trouve un indice sur un lieu ou une situation.")]
toolsList += [Tool("Cape",32,{"charisma":8},"Ajoute 8 points de charisme, avant application de l'affinité.")]
toolsList += [Tool("Liqueur de Vigueur",54,{"intelligence":15},"Deux exemplaires par achat. Utilisable lors d'une réanimation. Soigne 2 x INT de l'utilisateur à l'entité réanimée et annule la pénalité d'endurence.")]
toolsList += [Tool("Ecailles d'Invisilbilité",66,{"perception":15},"Utilisable à tout moment. Rend l'utilisateur invisible pour trois tours.")]
toolsList += [Tool("Masque Perfide",55,{"charisma":15},"Utilisable à tout moment. Donne l'apparence et la voix à l'utilisateur d'une autre personne au choix pour trois tours.")]

tools = {}
for tool in toolsList:
    tools[tool.name] = tool
    tool.imageFile = "data/images/icons/"+tool.name+".png"
