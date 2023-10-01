


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



weaponsList = []
weaponsList += [Weapon("Mains Nues",0,5)]
weaponsList += [Weapon("Poignard",26,9,{"dexterity":2})]
weaponsList += [Weapon("Epée courte",30,10,{"strength":5})]
weaponsList += [Weapon("Sabre",33,13,{"dexterity":7})]
weaponsList += [Weapon("Hachoir Large",52,15,{"strength":9})]
weaponsList += [Weapon("Lance",60,17,{"dexterity":11})]
weaponsList += [Weapon("Epée Longue",75,19,{"strength":12})]
weaponsList += [Weapon("Rapière",79,25,{"dexterity":16})]
weaponsList += [Weapon("Hache de Combat",80,25,{"strength":18})]
weaponsList += [Weapon("Faux",84,31,{"dexterity":20})]
weaponsList += [Weapon("Marteau de Guerre",91,33,{"strength":24})]
weaponsList += [Weapon("Sabre Oriental",163,39,{"dexterity":27})]
weaponsList += [Weapon("Tueuse de Dragon",140,40,{"strength":30})]

weapons = {}
for weapon in weaponsList:
    weapons[weapon.name] = weapon
    weapon.imageFile = "data/images/icons/"+weapon.name+".png"


toolsList = []
toolsList += [Tool("Verrou Déployable",27,{"strength":8},"Peut être posé sur une porte, la porte reste fermée jusqu'à ce que le verrou soit détruit. le verrou est une considéré comme une entité avec 20 PV et 40 CONST qui utilise toujours la garde.")]
toolsList += [Tool("Piège à Loup",30,{"dexterity":8},"Piège déployable sur une dalle. Immobilise une entité pour deux tours et infligle 2 x DEX du déployeur en dégats.")]
toolsList += [Tool("Pierre de Réflexion",26,{"intelligence":8},"Deux exemplaires par achat. Utilisable lors de situations de tensions. Ajoute deux minutes de temps au chronomètre.")]
toolsList += [Tool("Loupe",29,{"perception":8},"Deux exemplaires par achat. Trouve un indice sur un lieu ou une situation.")]
toolsList += [Tool("Cape",32,{"charisma":8},"Ajoute 8 points de charisme, avant application de l'affinité.")]
toolsList += [Tool("Liqueur de Vigueur",54,{"intelligence":15},"Deux exemplaires par achat. Utilisibale lors d'une réanimation. Soigne 2 x INT de l'utilisateur à l'entité réanimée et annule la pénalité d'endurence.")]
toolsList += [Tool("Ecailles d'Invisilbilité",66,{"perception":15},"Utilisale à tout moment. Rend l'utilisateur invisible pour trois tours.")]
toolsList += [Tool("Masque Perfide",55,{"charisma":15},"Utilisale à tout moment. Donne l'apparence et la voix à l'utilisateur d'une autre personne au choix pour trois tours.")]

tools = {}
for tool in toolsList:
    tools[tool.name] = tool
    tool.imageFile = "data/images/icons/"+tool.name+".png"
