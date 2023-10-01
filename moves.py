from constAndStyle import *



attacks = ["strong","fast","counter"]
defenses = ["block","dodge","feint"]
otherMoves = ["rest"]

throwBonus = {"strong":"STR","fast":"DEX","counter":"min{STR,DEX}+50%"}

movesToFr = {"strong":"attaque forte","fast":"attaque rapide","counter":"contre-attaque",
             "block":"garde","dodge":"esquive","feint":"feinte",
             "rest":"repos"}


counterColor = (187, 224, 52)
movesColorsList = [statsColors["strength"],statsColors["dexterity"],counterColor]
movesColors = {}
for index in range(3):
    movesColors[attacks[index]] = movesColorsList[index]
    movesColors[defenses[index]] = movesColorsList[index]
movesColors["rest"] = statsColors["stamina"]

exchangeTable = {"strong":"fast","fast":"counter","counter":"strong"}
exchangeLosingTable = {"fast":"strong","counter":"fast","strong":"counter"}
defenseTable = {"strong":"block","fast":"dodge","counter":"feint"}
defenseWinningTable = {"block":["counter","fast"],"dodge":["strong","counter"],"feint":["fast","strong"]}
defenseLosingTable = {"block":"strong","dodge":"fast","feint":"counter"}



movesEffects = {}

movesEffects["strong"] = "Si réussie, vous pouvez dépenser 1 STAM pour déplacer la cible de 1 ou 2 cases."
movesEffects["fast"] = "Si réussie, vous pouvez dépenser 1 STAM pour empécher la cible d'utiliser la mobilité de combat, dans ce cas la cible ne paye pas le coût de la mobilité de combat."
movesEffects["counter"] = "Si réussie, vous pouvez dépenser 1 STAM pour faire perdre 2 STAM à la cible."
movesEffects["block"] = "Si vous n'avez été ciblé par aucune attaque, récupérez 1 STAM."
movesEffects["dodge"] = "Si réussie, le coût de la mobilité de combat est réduit de 1 STAM."
movesEffects["feint"] = "Si réussie, vous pouvez dépenser 1 STAM pour échanger votre position avec un allié à 1 ou 2 cases de vous."
movesEffects["rest"] = "Récupérez 3 STAM."

#english version
'''
movesEffects["strong"] = "If successful, you can spend 1 stamina to move the target 1 or 2 squares away from its original position."
movesEffects["fast"] = "If successful, you can spend 1 stamina to prevent your target from using combat mobility, then the target does not pay the stamina cost of combat mobility."
movesEffects["counter"] = "If successful, you can spend 1 stamina to make your target lose 2 stamina."
movesEffects["block"] = "If you were not targeted by any attacks, regain 1 stamina."
movesEffects["dodge"] = "If successful, the cost of combat mobility is reduced by 1 stamina."
movesEffects["feint"] = "If successful, you can spend 1 stamina to exchange your position with an ally that is at most two squares away from you."
movesEffects["rest"] = "Regain 3 stamina."
'''
