import math
pzl = "123_45687"
width = int(math.sqrt((len(pzl))))
height = int(len(pzl)/width)

def swap(pzl, p1, p2):
    pzlLst = [*pzl]
    pzlLst[p1], pzlLst[p2] = pzlLst[p2], pzlLst[p1]
    return "".join(pzlLst)

def nbrs_array(pzlr):
    nbrarray = []
    for x in range(len(pzlr)):
        nbrarray.append([])
        if x == 0:
            nbrarray[x] = [1, width]
        elif x == len(pzlr)-1:
            nbrarray[x] = [x-1, x-width]
        elif x == width-1:
            nbrarray[x] = [x-1, x+width]
        elif x == len(pzlr)-width:
            nbrarray[x] = [x-width, x+1]
        elif 0<x<width-1:
            nbrarray[x] = [x-1, x+1, x+width]
        elif len(pzlr)-width<x<len(pzlr)-1:
            nbrarray[x] = [x-1, x+1, x-width]
        elif (x+1) % width == 0:
            nbrarray[x] = [x-1, x+width, x-width]
        elif x%width == 0:
            nbrarray[x] = [x+1, x+width, x-width]
        else:
            nbrarray[x] = [x+1, x-1, x-width, x+width]
    return nbrarray

NBRPOS = nbrs_array(pzl) 

def nbrs(pzl):
    upos = pzl.find("_")
    return[swap(pzl, upos, sp) for sp in NBRPOS[upos]]

def getLevel(puzzledict, pzl1):
    ctr = 0
    temp = pzl1
    while temp != pzl:
        ctr +=1
        temp = puzzledict[temp]
    return ctr

def BFS(start):
    parseMe = [start]
    bannedList = []
    dctSeen = {start:None}
    SumPerLevel = [[] for i in range(31)]
    while parseMe:

        node = parseMe.pop()
        ctr = 0
        for nbr in nbrs(node):
            if ctr > 1:
                bannedList.append(node)
                break
            if getLevel(dctSeen, nbr) == getLevel(dctSeen, node) + 1:
                ctr +=1

        for nbr in nbrs(node):
            if nbr not in dctSeen and node not in bannedList:
                parseMe.append(nbr)
                SumPerLevel[getLevel(dctSeen, node)] += 1 
                dctSeen[nbr] = node
    return SumPerLevel

for idx, val in enumerate(BFS(pzl)):
    print(f"Level: {idx} Unique Vals: {val} \n")
