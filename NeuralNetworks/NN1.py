import sys; args = sys.argv[1:]
import math

def parseArgs(args):
    inputs = []
    weightList = []
    tempList = open(args[0]).read().splitlines()
    for line in tempList:
        indivList = []
        for val in line.split(" "):
            indivList.append(float(val))
        weightList.append(indivList)
    functionType = args[1]
    for arg in args[2:]:
        inputs.append(float(arg))
    print(weightList)
    return inputs, weightList, functionType

def solve(inputs, weightList, functionType):
    currentNums = [*inputs]
    for currWeights in weightList[:-1]:
        lenNewNodes = len(currWeights)//len(currentNums)
        newNodes = [0] * lenNewNodes
        for cidx, currNum in enumerate(currentNums):
            affectedWeights = currWeights[cidx::len(currentNums)]
            for widx, weight in enumerate(affectedWeights):
                newNodes[widx] += currNum * weight
        newNodes = [doFunct(num, functionType) for num in newNodes]
        currentNums = newNodes
    finalWeights = weightList[-1]
    for cidx, currNum in enumerate(currentNums):
       currentNums[cidx] = currNum * finalWeights[cidx]
    return currentNums

def doFunct(num, functionType):
    if functionType == "T1":
        return num
    if functionType == "T2":
        if num > 0:
            return num
        else:
            return 0
    if functionType == "T3":
        return 1/(1 + math.exp(-num))
    if functionType == "T4":    
        return 2*(1/(1 + math.exp(-num))) - 1

def main():
    inputs, weightList, functionType = parseArgs(args)
    outputs = solve(inputs, weightList, functionType)
    print(str(outputs))

if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025