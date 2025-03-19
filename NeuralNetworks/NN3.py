import sys; args = sys.argv[1:]
import math
import random
import time; startTime = time.time()

def parseArgs(args):
    input = args[0]
    sign = input[7:8]
    radius = input[8:]
    if "=" in input:
        sign  = input[7:9]
        radius = input[9:]
    radius = float(radius)
   
    #sign = "<"
    #radius = float(1.3467107233345779)
    return sign, radius

def solveNN(inputs, weightList): #fix
    nodes = [inputs]
    for layer, weights in enumerate(weightList):
        nextLayer = []
        if layer == len(weightList) - 1:
            for idx, weight in enumerate(weights):
                val = weight * nodes[-1][idx]
                nextLayer.append(val)
        else:
            nodesCount = len(nodes[-1])
            for start in range(0, len(weights), nodesCount):
                weight = weights[start:start + nodesCount]
                value = doFunct(dotProduct(weight, nodes[-1]))
                nextLayer.append(value)
        nodes.append(nextLayer)
    return nodes

def dotProduct(v1, v2):
    return sum([v1[idx] * v2[idx] for idx in range(len(v1))])

def doFunct(num):
    return 1/(1 + math.exp(-num))

def doFunctDeriv(num):
    return num * (1 - num)

def findError(output, actual):
    return ((abs(output - actual))**2)/2

def backPropagate(nodeList, output, weights):
    alpha = 0.1
    gradients = [] #list of gradients (matches a weight)
    errors = [] #list of errors (matches a node)

    tempError = [nodeList[-1][0] - output]
    errors = [weights[len(weights)-1][idx] * (doFunctDeriv(nodeList[len(weights)-1][idx])) * error for idx,error in enumerate(tempError)]
    tempGradients = [nodeList[len(weights)-1][idx] * error for idx, error in enumerate(tempError)]
    gradients = [tempGradients] + gradients

    for layer in range(len(weights)-2, -1, -1):
        tempErrors = [] 
        tempGradients = [nodeList[layer][idx] * error for error in errors for idx in range(len(nodeList[layer]))]
        gradients = [tempGradients] + gradients
        ctr = 0
        for _, node in enumerate(nodeList[layer]):
            errorWeights = [weights[layer][idx] for idx in range(ctr, len(weights[layer]), len(nodeList[layer]))]
            error = dotProduct(errorWeights, errors) * (doFunctDeriv(node))
            tempErrors.append(error)
            ctr += 1
        errors = tempErrors

    for idx, layer in enumerate(weights):
        weights[idx] = [weight - alpha * gradients[idx][x] for x, weight in enumerate(layer)]

    return weights

def findOutput(x, y, sign, radius):
    if sign == "<=":
        if x**2 + y**2 <= radius:
            return 1
        else:
            return 0
    if sign == ">=":
        if x**2 + y**2 >= radius:
            return 1
        else:
            return 0
    if sign == "<":
        if x**2 + y**2 < radius:
            return 1
        else:
            return 0
    if sign == ">":
        if x**2 + y**2 > radius:
            return 1
        else:
            return 0

def initializeDict(sign, radius):
    vertexDictionary = {}
    for x in range(20000):
        x = random.uniform(-1.5, 1.5)
        y = random.uniform(-1.5, 1.5)
        output = findOutput(x, y, sign, radius)
        vertexDictionary[(x, y, 1)] = output
    return vertexDictionary

def main():
    sign, radius = parseArgs(args)
    #print(inputDict)
    #print(outputDict)
    epochs = 3000
    totalError = float("inf")
    while totalError > 0.01:
        #format of net is [3, 6, 3, 2, 1, 1]
        weights = [[random.uniform(-2, 2) for x in range(18)], [random.uniform(-2, 2) for x in range(18)], [random.uniform(-2, 2) for x in range(6)], [random.uniform(-2, 2) for x in range(2)], [random.uniform(-2, 2)]]
        epochCount = 0
        for epoch in range(epochs):
            vertexDictionary  = initializeDict(sign, radius)
            epochCount += 1 
            tempError = 0
            for inputs in vertexDictionary:
                output = vertexDictionary[inputs]
                inputs = [*inputs]
                nodeList = solveNN(inputs, weights)
                weights = backPropagate(nodeList, output, weights)
                tempError += findError(output, nodeList[-1][0])
                #print(tempError)
            if tempError < totalError:
                totalError = tempError
                print("Layer Counts: " + " ".join([str(len(layer)) for layer in nodeList]))
                print("Weights:")
                for val in weights:
                    print(" ".join(str(x) for x in val))
                #print("Current Error: ", totalError)
                #print(f"Expected Out: {outputDict[1]} \nActual: {solveNN(inputDict[1], weights)[-1]}")
                if totalError < 0.01:
                    break
    
    print(f"{epochCount=}")
    #print(f"Expected Out: {outputDict[2]} \nActual: {solveNN(inputDict[2], weights)[-1]}")
    #print(f"Time taken: {time.time()-startTime}")

if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025