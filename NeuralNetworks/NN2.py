import sys; args = sys.argv[1:]
import math
import random
import time; startTime = time.time()

def parseArgs(args):
    inputDict = {}
    outputDict = {}
    #lines = open(args[0]).read().splitlines()
    lines = open("NN2test.txt").read().splitlines()
    for idx, line in enumerate(lines):
        inputs = [float(x) for x in line[:line.index("=")].split()]
        inputs.append(1.0)
        outputs = [float(x) for x in line[line.index(">")+1:].split()]
        inputDict[idx] = inputs
        outputDict[idx] = outputs
    return inputDict, outputDict

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
    '''if num < -700:
        return 0
    if num > 700:
        return 1
    else:
        return 1/(1 + math.exp(-num))'''
    return 1/(1 + math.exp(-num))

def doFunctDeriv(num):
    return num * (1 - num)

def findError(outputs, actuals):
    return (sum(abs(outputs[idx] - actuals[idx]) for idx in range(len(outputs)))**2)/2

def backPropagate(nodeList, outputs, weights):
    alpha = 0.1
    gradients = [] #list of gradients (matches a weight)
    errors = [] #list of errors (matches a node)

    tempError = [nodeList[-1][idx] - outputs[idx] for idx in range(len(outputs))]
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

def main():
    inputDict, outputDict = parseArgs(args)
    #print(inputDict)
    #print(outputDict)
    '''weights = [[0.3, -2, -1.5, 2, 0, 2], [0.3, -0.5], [-1]]
    for x in range(2):
        print(f"Epoch {x+1}")
        for idx in inputDict:
            inputs = inputDict[idx]
            outputs = outputDict[idx]
            nodeList = solveNN(inputs, weights)
            weights = backPropagate(nodeList, outputs, weights)
            print(f"inputs: {inputs}")
            for val in weights:
                print(" ".join(str(x) for x in val))'''
    epochs = 3000
    totalError = float("inf")
    while totalError > 0.01:
        weights = [[random.uniform(-2, 2) for x in range(len(inputDict[0])*2)], [random.uniform(-2, 2) for x in range(2*len(outputDict[0]))], [random.uniform(-2, 2) for x in range(len(outputDict[0]))]]
        epochCount = 0
        for epoch in range(epochs):
            epochCount += 1 
            tempError = 0
            for idx in inputDict:
                inputs = inputDict[idx]
                outputs = outputDict[idx]
                nodeList = solveNN(inputs, weights)
                weights = backPropagate(nodeList, outputs, weights)
                tempError += findError(outputs, nodeList[-1])
                #print(tempError)
            if tempError < totalError:
                totalError = tempError
                print("Layer Counts: " + " ".join([str(len(layer)) for layer in nodeList]))
                #print("Weights: " + str(weights))
                for val in weights:
                   print(" ".join(str(x) for x in val))
                print("Current Error: ", totalError)
                #print(f"Expected Out: {outputDict[1]} \nActual: {solveNN(inputDict[1], weights)[-1]}")
                if totalError < 0.01:
                    break
    print(f"Weight Layer Sizes: : {[len(x) for x in weights]}")
    print(f"{epochCount=}")
    #print(f"Expected Out: {outputDict[2]} \nActual: {solveNN(inputDict[2], weights)[-1]}")
    #print(f"Time taken: {time.time()-startTime}")

if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025