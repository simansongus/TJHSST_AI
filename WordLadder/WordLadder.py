import sys; args = sys.argv[1:]
wordList = open(args[0]).read().splitlines()
glength = len(wordList)
import time
startTime = time.time()
if len(args) > 1:
    word1 = args[1]
    word2 = args[2]

def isEdge(str1, str2):
    diffCount = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diffCount += 1
            if diffCount > 1:
                return False
    return diffCount == 1  

def edgeListCreator(words):
    edgeCount = 0
    edgeList = [[] for _ in range(len(words))]
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if isEdge(words[i], words[j]):
                edgeList[i].append(words[j])
                edgeList[j].append(words[i])
                edgeCount += 1
    return edgeList, edgeCount

def degreeCalc(edges):
    max_degree = max(len(edge) for edge in edges)
    degrees = [0] * (max_degree + 1)
    for edge in edges:
            degrees[len(edge)] += 1
    return degrees

edgeList, edgeCount = edgeListCreator(wordList)
degrees = degreeCalc(edgeList)

def secondDegree(degreesLst):
    secondDegreeAMT = 0
    degreesLst.reverse()
    for idx, val in enumerate(degreesLst):
        if idx != 0 and val != 0:
            secondDegreeAMT = len(degreesLst) - 2
    for idxa, vala in enumerate(edgeList):
        if len(vala) == secondDegreeAMT:
            return wordList[idxa]
        
def connectedComponentSizes():
    def BFSa(start):
        if start in visited:
            return
        component_size = 0
        queue = [start]
        visited.add(start)
        ptr = 0
        while ptr < len(queue):
            node = queue[ptr]
            ptr += 1
            component_size += 1
            for neighbor in edgeList[wordList.index(node)]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return component_size
    visited = set()
    component_sizes = []
    for word in wordList:
        if word not in visited:
            size = BFSa(word)
            component_sizes.append(size)
    k3 = 0
    k4 = 0
    for size in component_sizes:
        if size == 3:
            neighbors = edgeList[wordList.index(word)]
            neighbor_degrees = [len(edgeList[wordList.index(neighbor)]) for neighbor in neighbors]
            if all(degree == 2 for degree in neighbor_degrees):
                k3 += 1
        elif size == 4:
            neighbors = edgeList[wordList.index(word)]
            neighbor_degrees = [len(edgeList[wordList.index(neighbor)]) for neighbor in neighbors]
            if all(degree == 3 for degree in neighbor_degrees):
                k4 += 1
    component_sizes.sort()
    size_list = [0] * (component_sizes[-1] + 1)
    for size in component_sizes:
        size_list[size] += 1
    return size_list, k3, k4

def BFS(start, goal): 
    if start == goal: return 0
    parseMe = [start]
    dctSeen = {start: None}
    ptr = 0
    while ptr < len(parseMe):
        node = parseMe[ptr]
        ptr +=1
        neighbors = edgeList[wordList.index(node)]
        for neighbor in neighbors:
            if neighbor == goal:
                dctSeen[neighbor] = node
                return reconstruct_path(dctSeen)
            if neighbor not in dctSeen:
                dctSeen[neighbor] = node
                parseMe.append(neighbor)
    return [], -1
                
def reconstruct_path(puzzledict):
    path = []
    current_state = list(puzzledict.keys())[-1]
    while current_state is not None:
        path.append(current_state)
        current_state = puzzledict[current_state]
    path = path[::-1]
    return path, len(path)

def farthestWord(word1):
    max_distance = 0
    farthest_word = None
    parseMe = [(word1, 0)]
    dctSeen = {word1: 0}
    ptr = 0
    while ptr < len(parseMe):
        node, distance = parseMe[ptr]
        ptr += 1
        if distance > max_distance:
            max_distance = distance
            farthest_word = node
        for neighbor in edgeList[wordList.index(node)]:
            if neighbor not in dctSeen:
                dctSeen[neighbor] = distance + 1
                parseMe.append((neighbor, distance + 1))
    return farthest_word


second_degree_word = secondDegree(degrees)
print("Word count: " + str(glength))
print("Edge count: " + str(edgeCount))
degrees.reverse()
print("Degree List: " + ",".join(map(str,degrees)))
print("Construction time: " + str(time.time()-startTime)[:4]+"s")
if second_degree_word is not None:
    print("Second degree word: " + second_degree_word)
else:
    print("Second degree word: None")
sizeList, k3, k4 = connectedComponentSizes()
print("Connected component size count: " + str(len([i for i in sizeList if i != 0])))
print("Largest component size: " + str(len(sizeList)-1))
print("K2 count: " + str(sizeList[2]))
print("K3 count: " + str(k3))
print("K4 count: " + str(k4))
if len(args) > 1:
    print("Neighbors: " + " ".join(edgeList[wordList.index(word1)]))
    wordPath, pathLength = BFS(word1, word2)
    print("Path: " + " ".join(wordPath))
    print("Farthest: " + farthestWord(word1))
#Gus Simanson, period 2, 2025