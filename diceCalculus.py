


def getDiceResults(nbDices = 3):
    results = [0]

    for dice in range(nbDices):
        newResults = []
        for value in [1,2,3,4,5,6]:
            for result in results:
                newResults += [result+value]
        results = newResults
    return results



def getDiceFrequencies(nbDices = 3):
    results = getDiceResults(nbDices)
    frequencies = {}

    for result in results:
        if result in frequencies:
            frequencies[result] += 1
        else:
            frequencies[result] = 1
    return frequencies



def getDiceProbabilites(nbDices = 3):
    frequencies = getDiceFrequencies(nbDices)
    nbOutcomes = 6**nbDices

    probas = {}
    for result in frequencies:
        probas[result] = round(frequencies[result]/nbOutcomes,3)
    return probas



def getDiceCumulative(nbDices = 3):
    probas = getDiceProbabilites(nbDices)
    minRes = nbDices
    maxRes = nbDices*6
    cumulative = {minRes-1:0}

    for result in range(minRes,maxRes+1):
        cumulative[result] = cumulative[result-1] + probas[result]
    cumulative.pop(minRes-1)
    return cumulative



def getDifferenceProbabilities(nbDices = 3):
    probas = getDiceProbabilites(nbDices)
    diffProbas = {}

    for resultA in probas:
        for resultB in probas:
            difference = resultA - resultB
            if difference in diffProbas:
                diffProbas[difference] += probas[resultA]*probas[resultB]
            else:
                diffProbas[difference] = probas[resultA]*probas[resultB]

    for difference in diffProbas:
        diffProbas[difference] = diffProbas[difference]
    return diffProbas



def getDifferenceCumulative(nbDices = 3):
    diffProbas = getDifferenceProbabilities()
    minDiff = -nbDices*5
    maxDiff = nbDices*5
    diffCumulative = {minDiff-1:0}

    for diff in range(minDiff,maxDiff+1):
        diffCumulative[diff] = diffCumulative[diff-1] + diffProbas[diff]
    diffCumulative.pop(minDiff-1)
    return diffCumulative



class Warrior():
    def __init__(self,strength=6,dexterity=6,constitution=6,weapon=15):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.weapon = weapon



def getExchangeAvg(warriorA=Warrior(),warriorB=Warrior(),nbDices=3):
    diffProbas = getDifferenceProbabilities(nbDices)
    AwinsBonus = warriorA.strength + warriorA.dexterity - warriorB.constitution
    BwinsBonus = warriorB.strength + warriorB.dexterity - warriorA.constitution
    AwinsDamage = 0
    BwinsDamage = 0
    AdrawDamage = 0
    BdrawDamage = 0

    for diff in diffProbas:
        if diff + AwinsBonus >= 0:
            AwinsDamage += diffProbas[diff]*(diff+AwinsBonus+warriorA.weapon)
        if diff + BwinsBonus >= 0:
            BwinsDamage += diffProbas[diff]*(diff+BwinsBonus+warriorB.weapon)

        drawDiff = diff + warriorA.strength - warriorB.strength
        if drawDiff > 0:
            AdrawDamage += diffProbas[diff]*(drawDiff+warriorA.weapon)
        elif drawDiff < 0:
            BdrawDamage += diffProbas[diff]*(warriorB.weapon-drawDiff)
        elif drawDiff == 0:
            AdrawDamage += diffProbas[diff]*warriorA.weapon
            BdrawDamage += diffProbas[diff]*warriorB.weapon

    AavgDamage = (AwinsDamage+AdrawDamage+0)/3
    BavgDamage = (BwinsDamage+BdrawDamage+0)/3
    return AavgDamage,BavgDamage



#print(getExchangeAvg())
