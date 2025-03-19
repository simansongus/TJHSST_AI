#Gus Simanson, pd 2
import math
import random
import time
import time; start_Time = time.time()

'''curr best run:
Time taken to parse data: 5.8555450439453125
Training...
Epoch 1 - Training Error: 0.3186575370197363 - Time: 853.8263010978699
Epoch 2 - Training Error: 0.10119117795596 - Time: 2437.34947013855
Epoch 3 - Training Error: 0.07741752165674917 - Time: 2955.2173030376434
Epoch 4 - Training Error: 0.0645808641358434 - Time: 3475.376710176468
Epoch 5 - Training Error: 0.055882623771727764 - Time: 3999.4018790721893
Epoch 6 - Training Error: 0.04934512261282241 - Time: 4520.267781019211
Epoch 7 - Training Error: 0.04421202022344256 - Time: 5042.82919216156
Epoch 8 - Training Error: 0.04020429887746318 - Time: 5737.756109952927
Training Accuracy = 0.9597957011225369
Time Taken to Train: 5737.756139993668

Testing...
Testing Error = 0.04742371697745462
Testing Accuracy = 0.9525762830225454
Total Time taken: 5748.092723846436'''

def createData():
    inputDictTrain = {}
    outputDictTrain = {}
    inputDictTest = {}
    outputDictTest = {}
    
    with open("mnist_train.csv") as file:
        lines = file.readlines()
    selected_lines = random.sample(lines[1:], 60000)
    for i, line in enumerate(selected_lines):  # Skip the first line
        parts = line.strip().split(',')
        label = int(parts[0])
        pixels = [int(p) / 255.0 for p in parts[1:]]  # Normalize pixel values
        pixels.append(1) #bias
        inputDictTrain[i] = pixels
        outputDictTrain[i] = [0]*10
        outputDictTrain[i][label] = 1

    with open("mnist_test.csv") as file:
        lines = file.readlines()
    selected_lines = random.sample(lines[1:], 2000)
    for i, line in enumerate(selected_lines):  # Skip the first line
        parts = line.strip().split(',')
        label = int(parts[0])
        pixels = [int(p) / 255.0 for p in parts[1:]]  # Normalize pixel values
        pixels.append(1)
        inputDictTest[i] = pixels
        outputDictTest[i] = [0]*10
        outputDictTest[i][label] = 1

    return inputDictTrain, outputDictTrain, inputDictTest, outputDictTest

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

def initializeWeights():
    weights = []
    #weights = [[random.uniform(-0.5, 0.5) for x in range(235500)], [random.uniform(-0.5, 0.5) for x in range(3000)], [random.uniform(-0.5, 0.5) for x in range(10)]]
    weights = [[random.uniform(-0.5, 0.5) for x in range(31400)], [random.uniform(-0.5, 0.5) for x in range(1600)],  [random.uniform(-0.5, 0.5) for x in range(400)], [random.uniform(-0.5, 0.5) for x in range(10)]]
    return weights

def main():
    inputDictTrain, outputDictTrain, inputDictTest, outputDictTest = createData()
    #layer counts should be [785, 300, 10, 10]
    #[785, 40, 40, 10, 10]
    timeTakenToParse = time.time() - start_Time
    print(f"Time taken to parse data: {timeTakenToParse}")

    #train
    epochs = 8
    weights = initializeWeights()

    print("Training...")
    startTime = time.time()
    for epoch in range(epochs):
        epochError = 0
        for idx in inputDictTrain:
            inputs = inputDictTrain[idx]
            outputs = outputDictTrain[idx]
            nodeList = solveNN(inputs, weights)
            weights = backPropagate(nodeList, outputs, weights)
            currentError = findError(outputs, nodeList[-1])
            epochError += currentError

        avgError = epochError / len(inputDictTrain)
        print(f"Epoch {epoch + 1} - Training Error: {avgError} - Time: {time.time()-startTime}")

    print(f"Training Accuracy = {1 - avgError}")
    print(f"Time Taken to Train: {time.time()-startTime}")
    print()

    #test
    print("Testing...")
    totalTestError = 0
    for idx in inputDictTest:
        inputs = inputDictTest[idx]
        outputs = outputDictTest[idx]
        nodeList = solveNN(inputs, weights)
        currentError = findError(outputs, nodeList[-1])
        totalTestError += currentError

    averageTestError = totalTestError / len(inputDictTest)

    print(f"Testing Error = {averageTestError}")
    print(f"Testing Accuracy = {1 - averageTestError}")
    print(f"Total Time taken: {time.time() - start_Time}")

    #ouput weights onto the file
    print(f"Weight Layer Sizes: : {[len(x) for x in weights]}")
    print("Outputting weights to file...")
    with open("MNISTweights.txt", "w") as file:
        for weightLayer in weights:
            weightLayer = [str(i) for i in weightLayer]
            file.write(" ".join(weightLayer) + "\n")

if __name__ == "__main__": main()