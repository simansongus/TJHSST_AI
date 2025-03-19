import sys; args = sys.argv[1:]

DirectionDict = {"L":"L", "D":"D", "U":"U", "R":"R", "UR":"V", "URD":"W", "RD":"S", "RDL":"T", "DL":"E", "DLU":"F", "LU":"M", "LUR":"N", "UD":"|", "LR":"-", "UDLR":"+", "":"."}

def grfParse(args):
    graphDict = {}
    size = int(args[0])
    rwd = 12

    if len(args) > 1 and args[1].isnumeric():
        width = int(args[1])
        height = size//width
        start = 2
    else:
        width = int(size ** 0.5)
        height = size // width
        while size % width != 0 or width < height:
            width += 1
            height = size // width
        start = 1
        
    for x in range(size):
        graphDict[x] = {}
        graphDict[x]["Neighbors"] = {}
        graphDict[x]["Direct Adjacent"] = {}
        row, col = divmod(x, width)
        nextTo = [(row - 1, col, "U"), (row + 1, col, "D"), (row, col - 1, "L"), (row, col + 1, "R")]
        for r, c, v in nextTo:
            if 0 <= r < height and 0 <= c < width:
                graphDict[x]["Direct Adjacent"][(r * width + c)] = v
                graphDict[x]["Neighbors"] = graphDict[x]["Direct Adjacent"].copy()
    graphDict["Graph Properties"] = {}
    graphDict["Graph Properties"]["width"]= width
    graphDict["Graph Properties"]["SolveMethod"] = 1

    for arg in args[start:]:
        if arg[0].upper() == "G":# Indicates how to value rewards.
            if arg[1] == "0":
                graphDict["Graph Properties"]["SolveMethod"] = 0
            else:
                graphDict["Graph Properties"]["SolveMethod"] = 1

        elif arg[:2].upper() == "R:": #  R:#  Sets the implied reward to the number indicated (default is 12)
            rwd = int(arg[2:])

        elif arg[0].upper() == "R" and ":" not in arg: #  R#  Sets the reward at the cell indicated by number equal to the implied reward
            graphDict[int(arg[1:])]["Reward"] = rwd

        elif arg[0].upper() == "R" and ":" in arg and arg[-1].isnumeric(): #  R#:#  Sets the reward for the cell at the first # to be equal to the 2nd #
            idx = int(arg[1:arg.index(":")])
            num = int(arg[arg.index(":")+1:])
            graphDict[idx]["Reward"] = num

        elif arg[0] == "B" and arg[-1].isnumeric():  # B#  Toggles the links going in and out of the cell at the indicated position
            v = int(arg[1:])
            for nbr in graphDict[v]["Direct Adjacent"]:
                if nbr in graphDict[v]["Neighbors"]:
                    graphDict[v]["Neighbors"].pop(nbr)
                else:
                    graphDict[v]["Neighbors"][nbr] = graphDict[v]["Direct Adjacent"][nbr]
                if v in graphDict[nbr]["Neighbors"]:
                    graphDict[nbr]["Neighbors"].pop(v)
                else:
                    graphDict[nbr]["Neighbors"][v] = graphDict[nbr]["Direct Adjacent"][v]

        elif arg[0].upper() == "B" and not arg[-1].isnumeric():# B#[NSEW]+  Toggles the link (and its reciprocal) in the specified direction(s) from the cell at the indicated position.
            for idx, val in enumerate(arg):
                if val in "NSEW":
                    tempStrt = idx
            v = int(arg[1:tempStrt])
            for val in arg[tempStrt:]:
                listOfAffected = []
                row, col = divmod(v, width)
                if val == "N":
                    r = row-1
                    if 0 <= r < height:
                        listOfAffected.append(v - width)
                elif val == "S":
                    r = row+1
                    if 0 <= r < height:
                        listOfAffected.append(v + width)
                elif val == "E":
                    c = col+1
                    if 0 <= c < width:
                        listOfAffected.append(v + 1)
                elif val == "W":
                    c = col-1
                    if 0 <= c < width:
                        listOfAffected.append(v - 1)
            for nbr in listOfAffected:
                if nbr in graphDict[v]["Neighbors"]:
                    graphDict[v]["Neighbors"].pop(nbr)
                elif nbr not in graphDict[v]["Neighbors"]:
                    graphDict[v]["Neighbors"][nbr] = graphDict[v]["Direct Adjacent"][nbr] 

                if v in graphDict[nbr]["Neighbors"]:
                    graphDict[nbr]["Neighbors"].pop(v)
                elif v not in graphDict[nbr]["Neighbors"]:
                    graphDict[nbr]["Neighbors"][v] = graphDict[nbr]["Direct Adjacent"][v]
    graphDict["Graph Properties"]["rwd"] = rwd
    return graphDict

def grfNbrs(graph, v):
    list = [*graph[v]["Neighbors"].keys()]
    return list

def grfStrProps(graph):
    toRet = ""
    props = graph["Graph Properties"]
    toRet = f"rwd: {props['rwd']}, width: {props['width']}"

    for v in range(len(graph)-1):
        if "Reward" in graph[v]:
            toRet += "\n" + f"{v}: rwd: {graph[v]['Reward']}"
    return toRet

def grfVProps(graph, v):
    if "Reward" not in graph[v]:
        return {}
    else: return {"rwd": graph[v]["Reward"]}

def grfStrEdges(graph):
    toRet = ""
    for v in graph:
        if v != "Graph Properties":
            temp = graph[v]["Neighbors"]
            t = ""
            for v in temp:
                t += temp[v]
            for key in DirectionDict:
                if sorted(key) == sorted(t):
                    newT = DirectionDict[key]
            toRet += newT
    return toRet

def generatePaths(graph, solveMethod):
    paths = {}

    if solveMethod == 0: # G0: BFS maximizing reward with the shortest path
        for startVertex in range(len(graph) - 1):
            if "Reward" in graph[startVertex]:
                paths[startVertex] = [[startVertex]]
                continue
            queue = [(startVertex, [startVertex], 0)]
            visited = {}
            bestReward = 0
            shortestLength = float('inf')
            bestPaths = []
            while queue:
                currentVertex, path, highestReward = queue.pop(0)
                pathLength = len(path)
                if currentVertex in visited and pathLength > visited[currentVertex]:
                    continue
                visited[currentVertex] = pathLength
                if "Reward" in graph[currentVertex] and graph[currentVertex]["Reward"] > highestReward:
                    highestReward = graph[currentVertex]["Reward"]
                if highestReward >= bestReward:
                    if pathLength < shortestLength or highestReward > bestReward:
                        bestReward = highestReward
                        shortestLength = pathLength
                        bestPaths = [path]
                    elif pathLength == shortestLength:
                        bestPaths.append(path)
                if not "Reward" in graph[currentVertex]:
                    for nbr in grfNbrs(graph, currentVertex):
                        if nbr not in visited or pathLength + 1 <= visited[nbr]:
                            newPath = path + [nbr]
                            queue.append((nbr, newPath, highestReward))
            paths[startVertex] = bestPaths

    if solveMethod == 1:# G1: BFS maximizing reward divided by the number of steps to reach it
        for startVertex in range(len(graph) - 1):
            if "Reward" in graph[startVertex]:
                paths[startVertex] = [[startVertex]]
                continue
            queue = [(startVertex, [startVertex], 0)]
            visited = {}
            bestRatio = 0
            bestPaths = []
            while queue:
                currentVertex, path, highestRatio = queue.pop(0)
                pathLength = len(path)-1
                if currentVertex in visited and pathLength > visited[currentVertex]:
                    continue
                visited[currentVertex] = pathLength
                if "Reward" in graph[currentVertex]:
                    reward = graph[currentVertex]["Reward"]
                    ratio = reward / pathLength
                    if ratio > bestRatio:
                        bestRatio = ratio
                        bestPaths = [path]
                    elif ratio == bestRatio:
                        bestPaths.append(path)
                    continue
                for nbr in grfNbrs(graph, currentVertex):
                    if nbr not in visited or pathLength + 1 <= visited[nbr]:
                        newPath = path + [nbr]
                        newRatio = highestRatio
                        if "Reward" in graph[nbr]:
                            newRwd = graph[nbr]["Reward"]
                            newRatio = max(highestRatio, newRwd / (pathLength + 1))
                        queue.append((nbr, newPath, newRatio))
            paths[startVertex] = bestPaths
    return paths

def shortenPath(graph):
    newPaths = {}
    solveMethod = graph["Graph Properties"]["SolveMethod"]
    paths = generatePaths(graph, solveMethod)
    for vertex in paths:
        vSet = set()
        if len(paths[vertex]) == 0:
            vSet.add(".")
        else:
            for path in paths[vertex]:
                if len(path) == 1:
                    vSet.add("")
                else:
                    vSet.add(path[1])
        newPaths[vertex] = vSet
    return newPaths

def grfStr(graph):
    width = graph["Graph Properties"]["width"]
    helperDict = {width: "D", -width: "U", 1: "R", -1: "L"}
    toRet = ""
    paths = shortenPath(graph)
    for vertex in paths:
        tempStr = ""
        for nbr in paths[vertex]:
            if nbr == ".":
                tempStr += "."
            elif nbr == "" and "Reward" in graph[vertex]:
                tempStr += "*"
            elif nbr == "" and "Reward" not in graph[vertex]:
                tempStr += "."
            elif nbr-vertex in helperDict:
                tempStr += helperDict[nbr-vertex]
            else:
                tempStr += "."
        
        if "*" in tempStr:
            toRet += "*"
        elif "." in tempStr:
            toRet += "."
        else:
            for key in DirectionDict:
                if sorted(key) == sorted(tempStr):
                    toRet += DirectionDict[key]
        '''elif "." in tempStr and len(tempStr) > 1:
            tempStr = tempStr.replace(".", "")
            for key in DirectionDict:
                if sorted(key) == sorted(tempStr):
                    toRet += DirectionDict[key]'''
    return toRet

def print2d(w, edgesStr):
    print("\n".join(edgesStr[rs:rs+w] for rs in range(0, len(edgesStr), w)))

def main():
    grf = grfParse(args)
    width = grf["Graph Properties"]["width"]
    edgesStr = grfStrEdges(grf)
    propsStr = grfStrProps(grf)
    print2d(width, edgesStr)
    print(propsStr)
    print()

    #print(grfNbrs(grf, 11))
    #print(grf[11]["Direct Adjacent"])
    #print(grfVProps(grf,9))
    #paths = shortenPath(grf)
    #print(paths)
    #print(paths[10])

    grfString = grfStr(grf)
    print("Policy:")
    print2d(width, grfString)


if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025