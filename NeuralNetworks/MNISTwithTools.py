#Gus Simanson
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import csv
import time

def createData(file, amount):
    data = []
    labels = []
    with open(file) as file:
        reader = list(csv.reader(file))
        lines = reader[1:]
        np.random.shuffle(lines)
        for line in lines[:amount]:
            label = int(line[0])
            pixels = np.array([int(p) / 255.0 for p in line[1:]], dtype=np.float32)
            data.append(pixels)
            labels.append(label)
    return np.array(data), np.array(labels)

trainData, trainLabels = createData("mnist_train.csv", 60000)
testData, testLabels = createData("mnist_test.csv", 10000)

trainDataset = TensorDataset(torch.tensor(trainData), torch.tensor(trainLabels, dtype=torch.long))
testDataset = TensorDataset(torch.tensor(testData), torch.tensor(testLabels, dtype=torch.long))

trainLoader = DataLoader(trainDataset, batch_size=64, shuffle=True)
testLoader = DataLoader(testDataset, batch_size=64, shuffle=False)

model = nn.Sequential(nn.Linear(28 * 28, 256),nn.ReLU(),nn.Dropout(0.5),nn.Linear(256, 128),nn.ReLU(),nn.Dropout(0.5),nn.Linear(128, 64),nn.ReLU(),nn.Dropout(0.5),nn.Linear(64, 10),nn.LogSoftmax(dim=1))

criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def findAccuracy(outputs, actuals):
    correct = 0
    for i in range(len(outputs)):
        if outputs[i] == actuals[i]:
            correct += 1
    return correct / len(outputs) 

# Training
print("Training...")
startTime = time.time()
epochs = 2
for epoch in range(epochs):
    eTime = time.time()
    for data, target in trainLoader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
    correct = 0
    total = 0 
    with torch.no_grad():
        for data, target in trainLoader:
            output = model(data)
            _, predicted = torch.max(output, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    print(f"Epoch {epoch + 1}, Training Loss: {loss.item()}, Training Accuracy: {correct/total}, Time Taken: {time.time() - eTime}")
print(f"Total Time Training: {time.time() - startTime}")

# Testing
print("Testing...")
correct = 0
total = 0
with torch.no_grad():
    for data, target in testLoader:
        output = model(data)
        _, predicted = torch.max(output, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()
print(f"Testing Accuracy: {correct / total}")

print("Saving Weights...")
with open("MNISTtoolweights.txt", "w") as file:
    for name, param in model.named_parameters():
        if param.requires_grad:
            weightLayer = param.data.numpy().flatten()
            weightLayer = [str(i) for i in weightLayer]
            file.write(" ".join(weightLayer) + "\n")
print("Done")