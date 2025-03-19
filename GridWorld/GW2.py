import sys; args = sys.argv[1:]

DirectionDict = {"N":"N", "S":"S", "E":"E", "W":"W", "NS":"|", "NE":"L", "NW":"J", "SE":"r", "SW":"7", "EW":"-", "SNW":"<", "SNE":">", "NEW":"^", "SEW":"v", "NEWS":"+", "":"."}
def grfParse(args):
    edgeLord = {}
    graphDict = {}
    for arg in args:
        if arg[0] == "G": #proceed with Graph directives
            GW = True
            grwd = 12
            if arg[1] == "N":
                GW = False

            size = arg[:5] #change to be until there is a letter character
            #trim the size to only be numbers
            while "W" in size or "R" in size or not size[-1].isdigit():
                size = size[:-1]
            while "N" in size or not size[0].isdigit():
                size = size[1:]
            size = int(size)

            if "W" in arg:
                amt = int(arg[arg.index("W")+1])
                if amt == 0:
                    width = 0
                    height = 0
                else:
                    if "R" not in arg:
                        width = int(arg[arg.index("W")+1:])
                    else: 
                        width = int(arg[arg.index("W")+1:arg.index("R")])
                    height = size // width
            elif size in (0, 1, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
                width = size
                height = 1
            else: 
                width = int(size ** 0.5)
                height = size // width
                while size % width != 0 or width < height:
                    width += 1
                height = size // width
            if "R" in arg:
                pos = (arg.index("R") + 1)
                if pos < len(arg):
                    grwd = int(arg[pos:])

            if GW and width != 0:
                for x in range(size):
                    graphDict[x] = {}
                    graphDict[x]["Neighbors"] = {}
                    graphDict[x]["Direct Adjacent"] = {}
                    graphDict[x]["Jumps"] = set()
                    row, col = divmod(x, width)
                    nextTo = [(row - 1, col, "N"), (row + 1, col, "S"), (row, col - 1, "W"), (row, col + 1, "E")]
                    for r, c, v in nextTo:
                        if 0 <= r < height and 0 <= c < width:
                            graphDict[x]["Direct Adjacent"][(r * width + c)] = v
                    graphDict[x]["Neighbors"] = graphDict[x]["Direct Adjacent"].copy()
            else:
                for x in range(size):
                    graphDict[x] = {}
                    graphDict[x]["Neighbors"] = {}
                    graphDict[x]["Jumps"] = set()
            graphDict["Graph Properties"] = {"width": width, "rwd": grwd, "gridWorld": GW}

        elif arg[0] == "V": #proceed with vertex directive
            toggle = False
            if "B" in arg:
                toggle = True

            rwd = None
            #if b, all standard edges are toggled and all jumps are removed
            if "R" in arg:
                rwd = grwd
                vslcs = arg[1:arg.index("R")]
                while "T" in vslcs or "B" in vslcs or not vslcs[-1] in "1234567890:":
                    vslcs = vslcs[:-1]

                pos = (arg.index("R") + 1)
                if pos < len(arg) and arg[pos].isdigit():
                    trwd = arg[pos:]
                    while not trwd[-1].isdigit():
                        trwd = trwd[:-1]
                    rwd = int(trwd)
            elif "T" in arg:
                vslcs = arg[1:arg.index("T")]
                while "R" in vslcs or "B" in vslcs or not vslcs[-1] in "1234567890:":
                    vslcs = vslcs[:-1]
            elif "B" in arg:
                vslcs = arg[1:arg.index("B")]
                while "T" in vslcs or "R" in vslcs or not vslcs[-1] in "1234567890:":
                    vslcs = vslcs[:-1]
            else: vslcs = arg[1:]
            listOfAffected = parseVSlices(vslcs, size)
            if rwd != None:
                for v in listOfAffected:
                    graphDict[v]["Vertex Rwd"] = rwd

            changes = {}
            #print(listOfAffected)
            if toggle:
                for v in listOfAffected:
                    #take care of jumps
                    newV = graphDict[v]["Jumps"].copy()
                    for j in graphDict[v]["Jumps"]:
                        #newJ = graphDict[j]["Jumps"].copy()
                        if j not in listOfAffected:
                            newV.discard(j)
                            if (v,j) in edgeLord:
                                edgeLord.pop((v,j))

                    for pos in graphDict:
                        if pos != "Graph Properties" and pos != "edgeLord":
                            newP = graphDict[pos]["Jumps"].copy()
                            if v in graphDict[pos]["Jumps"] and pos not in listOfAffected:
                                newP.discard(v)
                                if (pos, v) in edgeLord:
                                    edgeLord.pop((pos,v))
                            graphDict[pos]["Jumps"] = newP
                        #if v in graphDict[j]["Jumps"] and j not in listOfAffected:
                            #newJ.discard(v)
                    graphDict[v]["Jumps"] = newV
                    #every other toggle
                    
                    changes[v] = {"add": [], "remove": []}
                    for nbr in graphDict[v]["Neighbors"]:
                        if nbr not in listOfAffected:
                            changes[v]["remove"].append(nbr)
                            if nbr not in changes:
                                changes[nbr] = {"add": [], "remove": []}
                            if v in graphDict[nbr]["Neighbors"]:
                                changes[nbr]["remove"].append(v)
                                if (nbr,v) in edgeLord:
                                    edgeLord.pop((nbr,v))
                            if v not in graphDict[nbr]["Neighbors"]:
                                changes[nbr]["add"].append(v)
                            if (v,nbr) in edgeLord:
                                edgeLord.pop((v,nbr))
                    for nbr in graphDict[v]["Direct Adjacent"]:
                        if nbr not in listOfAffected and nbr not in graphDict[v]["Neighbors"]:
                            changes[v]["add"].append(nbr)
                            if nbr not in changes:
                                changes[nbr] = {"add": [], "remove": []}
                            if v in graphDict[nbr]["Neighbors"]:
                                changes[nbr]["remove"].append(v)
                                if (nbr,v) in edgeLord:
                                    edgeLord.pop((nbr,v))
                            if v not in graphDict[nbr]["Neighbors"]:
                                changes[nbr]["add"].append(v)

            for v, change in changes.items():
                for nbr in change["remove"]:
                    if nbr in graphDict[v]["Neighbors"]:
                        graphDict[v]["Neighbors"].pop(nbr)
                for nbr in change["add"]:
                    graphDict[v]["Neighbors"][nbr] = graphDict[v]["Direct Adjacent"][nbr]

        elif arg[0] == "E":
            type1 = True
            rwd = None
            for val in arg[1:]:
                if val in "NSEW":
                    type1 = False
                    break
            mngment = "~"
            vslcs1ST = 1
            if arg[1] in "@+!~*":
                mngment = arg[1]
                vslcs1ST = 2

            if type1:
                if "=" in arg[vslcs1ST:]:
                    connection = "="
                    vslcs1 = arg[vslcs1ST:arg.index("=")]
                    vslcs2ST = arg.index("=") + 1
                if "~" in arg[vslcs1ST:]:
                    connection = "~"
                    vslcs1 = arg[vslcs1ST: vslcs1ST+arg[vslcs1ST:].index("~")]
                    vslcs2ST = vslcs1ST+arg[vslcs1ST:].index("~") + 1

                if "R" in arg:
                    rwd = 12
                    vslcs2 = arg[vslcs2ST:arg.index("R")]
                    while "T" in vslcs2 or not vslcs2[-1] in "1234567890:":
                        vslcs2 = vslcs2[:-1]

                    pos = (arg.index("R") + 1)
                    if pos < len(arg) and arg[pos].isdigit():
                        rwd = int(arg[pos:])
                elif "T" in arg:
                    vslcs2 = arg[vslcs2ST:arg.index("T")]
                    while "R" in vslcs2 or not vslcs2[-1] in "1234567890:":
                        vslcs2 = vslcs2[:-1]
                else: vslcs2 = arg[vslcs2ST:]

                listOfAffected1 = parseVSlices(vslcs1, size)
                listOfAffected2 = parseVSlices(vslcs2, size)
                dictAffected = {v: set() for v in listOfAffected1}
                for idx, val in enumerate(listOfAffected1):
                    dictAffected[val].add(listOfAffected2[idx])

            else: #type 2 for e directive
                directMeaning = {"N": (0,-1), "S": (0,1), "E": (1,0), "W": (-1,0)}
                for idx, val in enumerate(arg[1:]):
                    if val in "NSEW":
                        vslcsEND = idx + 1
                        directST = idx + 1
                        break
                vslcs = arg[vslcs1ST:vslcsEND]
                listOfAffected = parseVSlices(vslcs, size)
                dictAffected = {v: set() for v in listOfAffected}

                if "=" in arg[directST:]:
                    connection = "="
                    directList = arg[directST:arg.index("=")]
                if "~" in arg[directST:]:
                    connection = "~"
                    directList = [*arg[directST: directST+arg[directST:].index("~")]]
                if "R" in arg:
                    rwd = 12
                    pos = (arg.index("R") + 1)
                    if pos < len(arg) and arg[pos].isdigit():
                        rwd = int(arg[pos:])

                for v in listOfAffected:
                    for d in directList:
                        row, col = divmod(v, width)
                        newRow = row + directMeaning[d][1]
                        newCol = col + directMeaning[d][0]
                        if 0 <= newCol < width and 0 <= newRow < height:
                            dictAffected[v].add(newRow * width + newCol)

            edgesToRemove = set()
            for key in dictAffected:
                for val in dictAffected[key]:
                    if val in dictAffected and key in dictAffected[val] and key != val:
                        connection = "="
                        if key < val:
                            edgesToRemove.add((val, key))
                        else:
                            edgesToRemove.add((key, val))
            for edge in edgesToRemove:
                dictAffected.pop(edge[0])

            graphDict, edgeLord = edgeDirectiveHelper(graphDict, dictAffected, connection, mngment, rwd, edgeLord)
        else: continue
    graphDict["edgeLord"] = edgeLord
    return graphDict

def parseVSlices(vslcs, size):
    vslcs = vslcs.split(",")
    listOfVals = [x for x in range(size)]
    listOfAffected = []
    for vslc in vslcs:
        if vslc.count(":") == 0:
            start = vslc
            if start == "": start = None
            else: start = int(start)
            loc = listOfVals[start]
            listOfAffected.append(loc)
        if vslc.count(":") == 1:
            start, end = vslc.split(":")
            if start == "": start = None
            else: start = int(start) 
            if end == "": end = None
            else: end = int(end)
            for x in listOfVals[start:end]:
                listOfAffected.append(x)
        if vslc.count(":") == 2:
            start, end, step = vslc.split(":")
            if start == "": start = None
            else: start = int(start)
            if end == "": end = None
            else: end = int(end)
            if step == "": step = None
            else: step = int(step)
            for x in listOfVals[start:end:step]:
                listOfAffected.append(x)
    return listOfAffected

def edgeDirectiveHelper(graphDict, dictAffected, connection, mngment, rwd, edgeLord):
    for t1 in dictAffected:
        for t2 in dictAffected[t1]:
            if mngment == "~": #toggle - default
                if connection == "=":
                    rep1 = True
                    rep2 = True
                    if t1 in graphDict[t2]["Jumps"]:
                        if (t2,t1) in edgeLord:
                            edgeLord.pop((t2,t1))
                        graphDict[t2]["Jumps"].discard(t1)
                        rep1 = False
                    if t2 in graphDict[t1]["Jumps"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Jumps"].discard(t2)
                        rep2 = False
                    if t1 in graphDict[t2]["Neighbors"]:
                        if (t2,t1) in edgeLord:
                            edgeLord.pop((t2,t1))
                        graphDict[t2]["Neighbors"].pop(t1)
                        rep1 = False
                    if t2 in graphDict[t1]["Neighbors"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Neighbors"].pop(t2)
                        rep2 = False
                    if t1 not in graphDict[t2]["Jumps"] and t1 not in graphDict[t2]["Neighbors"] and rep1:
                        if rwd != None:
                            edgeLord[(t2, t1)] = rwd
                        if t1 in graphDict[t2]["Direct Adjacent"]:
                            graphDict[t2]["Neighbors"][t1] = graphDict[t2]["Direct Adjacent"][t1]
                        else:
                            graphDict[t2]["Jumps"].add(t1)
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"] and rep2:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)
                else:
                    rep = True
                    if t2 in graphDict[t1]["Jumps"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Jumps"].discard(t2)
                        rep = False
                    if t2 in graphDict[t1]["Neighbors"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Neighbors"].pop(t2)
                        rep = False
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"] and rep:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)
            if mngment == "!": #remove any existing edges
                if connection == "=":
                    if t1 in graphDict[t2]["Jumps"]:
                        if (t2,t1) in edgeLord:
                            edgeLord.pop((t2,t1))
                        graphDict[t2]["Jumps"].discard(t1)
                    if t2 in graphDict[t1]["Jumps"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Jumps"].discard(t2)
                    if t1 in graphDict[t2]["Neighbors"]:
                        if (t2,t1) in edgeLord:
                            edgeLord.pop((t2,t1))
                        graphDict[t2]["Neighbors"].pop(t1)
                    if t2 in graphDict[t1]["Neighbors"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Neighbors"].pop(t2)
                else:
                    if t2 in graphDict[t1]["Jumps"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Jumps"].discard(t2)
                    if t2 in graphDict[t1]["Neighbors"]:
                        if (t1,t2) in edgeLord:
                            edgeLord.pop((t1,t2))
                        graphDict[t1]["Neighbors"].pop(t2)

            if mngment == "+": #add new with properties, ignoring existent
                if connection == "=":
                    if t1 not in graphDict[t2]["Jumps"] and t1 not in graphDict[t2]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t2, t1)] = rwd
                        if t1 in graphDict[t2]["Direct Adjacent"]:
                            graphDict[t2]["Neighbors"][t1] = graphDict[t2]["Direct Adjacent"][t1]
                        else:
                            graphDict[t2]["Jumps"].add(t1)
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)
                else:
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)

            if mngment == "*": #add if missing, apply properties to existing and new
                if connection == "=":
                    if t1 in graphDict[t2]["Jumps"] and rwd != None:
                        edgeLord[(t2, t1)] = rwd
                    if t2 in graphDict[t1]["Jumps"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t1 in graphDict[t2]["Neighbors"] and rwd != None:
                        edgeLord[(t2, t1)] = rwd
                    if t2 in graphDict[t1]["Neighbors"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t1 not in graphDict[t2]["Jumps"] and t1 not in graphDict[t2]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t2, t1)] = rwd
                        if t1 in graphDict[t2]["Direct Adjacent"]:
                            graphDict[t2]["Neighbors"][t1] = graphDict[t2]["Direct Adjacent"][t1]
                        else:
                            graphDict[t2]["Jumps"].add(t1)
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)
                else:
                    if t2 in graphDict[t1]["Jumps"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t2 in graphDict[t1]["Neighbors"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t2 not in graphDict[t1]["Jumps"] and t2 not in graphDict[t1]["Neighbors"]:
                        if rwd != None:
                            edgeLord[(t1, t2)] = rwd
                        if t2 in graphDict[t1]["Direct Adjacent"]:
                            graphDict[t1]["Neighbors"][t2] = graphDict[t1]["Direct Adjacent"][t2]
                        else:
                            graphDict[t1]["Jumps"].add(t2)
            if mngment == "@": #apply properties to existing 
                if connection == "=":
                    if t1 in graphDict[t2]["Jumps"] and rwd != None:
                        edgeLord[(t2, t1)] = rwd
                    if t2 in graphDict[t1]["Jumps"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t1 in graphDict[t2]["Neighbors"] and rwd != None:
                        edgeLord[(t2, t1)] = rwd
                    if t2 in graphDict[t1]["Neighbors"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                else:
                    if t2 in graphDict[t1]["Jumps"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
                    if t2 in graphDict[t1]["Neighbors"] and rwd != None:
                        edgeLord[(t1, t2)] = rwd
    return graphDict, edgeLord

def grfSize(graph):
    return len(graph) - 2

def grfNbrs(graph, v):
    list = [*graph[v]["Neighbors"].keys()] + [*graph[v]["Jumps"]]
    return list

def grfGProps(graph):
    toRet = {}
    props = graph["Graph Properties"]
    if props["gridWorld"]:
        toRet["width"] = props["width"]
    toRet["rwd"] = props['rwd']
    return toRet

def grfVProps(graph, v):
    if "Vertex Rwd" not in graph[v]:
        return {}
    else: return {"rwd": graph[v]["Vertex Rwd"]}

def grfEProps(graph, v1, v2):
    edgeLord = graph["edgeLord"]
    if (v1, v2) not in edgeLord:
        return {}
    else: return {"rwd": edgeLord[(v1, v2)]}

def grfStrEdges(graph):
    toRet = ""
    if graph["Graph Properties"]["gridWorld"] and graph["Graph Properties"]["width"] != 0:
        for v in graph:
            if v != "Graph Properties" and v != "edgeLord":
                temp = graph[v]["Neighbors"]
                t = ""
                for v in temp:
                    t += temp[v]
                for key in DirectionDict:
                    if sorted(key) == sorted(t):
                        newT = DirectionDict[key]
                toRet += newT
    jumpList = [(v, Jump) for v in range(grfSize(graph)) for Jump in graph[v]["Jumps"]]
    if len(jumpList) > 0:
        jumpList = formatJumps(jumpList)
        jumpList = str(jumpList)
        toRet = toRet + "\n" + jumpList
    return toRet

def grfStrProps(graph):
    edgeLord = graph["edgeLord"]
    toRet = ""
    props = graph["Graph Properties"]
    if props["gridWorld"]:
        toRet = f"rwd: {props['rwd']}, width: {props['width']}"
    else: toRet = f"rwd: {props['rwd']}"

    for v in range(grfSize(graph)):
        if "Vertex Rwd" in graph[v]:
            toRet += "\n" + f"{v}: rwd: {graph[v]['Vertex Rwd']}"
    for edge in edgeLord:
        toRet += "\n" + f"{edge}: rwd: {edgeLord[edge]}"
    return toRet
        

def print2d(graph, w, edgesStr):
    if graph["Graph Properties"]["gridWorld"]:
        print("\n".join(edgesStr[rs:rs+w] for rs in range(0, len(graph)-2, w)))
        
def formatJumps(jumps):
    formattedJumps = []
    jumps.sort()
    doneJumps = set()
    for jump in jumps:
        if jump in doneJumps:
            continue
        if (jump[1], jump[0]) in jumps:
            formattedJumps.append(f"{jump[0]}={jump[1]}")
            doneJumps.add((jump[1], jump[0]))
        else:
            formattedJumps.append(f"{jump[0]}~{jump[1]}")
        doneJumps.add(jump)
    return ';'.join(formattedJumps)

def pathGenerator(graph):
    paths = {}
    for startVertex in range(grfSize(graph)):
        queue = [(startVertex, [startVertex])]
        visited = {}
        shortestLength = float('inf')
        found_paths = []
        while queue:
            currentVertex, path = queue.pop(0)
            pathLength = len(path)
            if pathLength > shortestLength:
                continue
            if currentVertex in visited and pathLength > visited[currentVertex]:
                continue
            visited[currentVertex] = pathLength
            if grfVProps(graph, currentVertex):
                if pathLength <= shortestLength:
                    found_paths.append(path)
                    shortestLength = pathLength
                continue
            for nbr in grfNbrs(graph, currentVertex):
                new_path = path + [nbr]
                queue.append((nbr, new_path))
                edge_props = grfEProps(graph, currentVertex, nbr)
                if edge_props and pathLength + 1 <= shortestLength:
                    found_paths.append(new_path)
                    shortestLength = pathLength + 1
        paths[startVertex] = found_paths
    return paths

def shortenPath(graph):
    newPaths = {}
    paths = pathGenerator(graph)
    for vertex in paths:
        vSet = set()
        for path in paths[vertex]:
            if len(path) == 1:
                vSet.add("")
            else:
                vSet.add(path[1])
        newPaths[vertex] = vSet
    return newPaths
    

def grfStr(graph):
    width = graph["Graph Properties"]["width"]
    helperDict = {width: "S", -width: "N", 1: "E", -1: "W"}
    jumpsUsed = []
    toRet = ""
    paths = shortenPath(graph)
    for v in paths:
        tempStr = ""
        for nbr in paths[v]:
            if nbr == "":
                tempStr += "*"
            elif nbr-v in helperDict:
                tempStr += helperDict[nbr-v]
            else:
                tempStr += "."
                jumpsUsed.append((v, nbr))
        if "*" in tempStr:
            toRet += "*"
        elif "." in tempStr and len(tempStr) > 1:
            tempStr = tempStr.replace(".", "")
            for key in DirectionDict:
                if sorted(key) == sorted(tempStr):
                    toRet += DirectionDict[key]
        elif "." in tempStr:
            toRet += "."
        else:
            for key in DirectionDict:
                if sorted(key) == sorted(tempStr):
                    toRet += DirectionDict[key]
    return toRet, jumpsUsed


def main():
    grf = grfParse(args)
    edgesStr = grfStrEdges(grf)
    if " " in edgesStr:
        edgesStr = edgesStr[:edgesStr.index("\n")]
    jumpList = [(v, Jump) for v in range(grfSize(grf)) for Jump in grf[v]["Jumps"]]
    propsStr = grfStrProps(grf)
    if grf["Graph Properties"]["gridWorld"] and grf["Graph Properties"]["width"] != 0:
        width = grfGProps(grf)["width"]
        print2d(grf, width, edgesStr)
        if len(jumpList) != 0:
            jumpList = [(v, Jump) for v in range(grfSize(grf)) for Jump in grf[v]["Jumps"]]
            formatted_jumps = formatJumps(jumpList)
            print(f"Jumps: {formatted_jumps}")
    print(propsStr)
    print()
    grfString, jumps = grfStr(grf)
    #path = pathGenerator(grf)
    #print(path)

    print("Policy:")
    print2d(grf, grfGProps(grf)["width"], grfString)
    for jump in jumps:
        print(f"{jump[0]}>{jump[1]}")


if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025