from constAndStyle import *



attacks = ["strong","fast","counter"]
defenses = ["block","dodge","feint"]
otherMoves = ["rest"]


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

movesEffects["strong"] = "If successful, you can spend 1 stamina to move the target 1 or 2 squares away from its original position."
movesEffects["fast"] = "If successful, you can spend 1 stamina to prevent your target from using combat mobility, then the target does not pay the stamina cost of combat mobility."
movesEffects["counter"] = "If successful, you can spend 1 stamina to make your target lose 2 stamina."
movesEffects["block"] = "If you were not targeted by any attacks, regain 1 stamina."
movesEffects["dodge"] = "If successful, the cost of combat mobility is reduced by 1 stamina."
movesEffects["feint"] = "If successful, you can spend 1 stamina to exchange your position with an ally that is at most two squares away from you."
movesEffects["rest"] = "Regain 3 stamina."
