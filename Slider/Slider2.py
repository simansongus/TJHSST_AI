import sys; args = sys.argv[1:]
import math 
puzzles = open(args[0]).read().splitlines()
#puzzles = open("Slider2test.txt").read().splitlines()
solution = puzzles[0]
width = int(math.sqrt((len(solution))))
height = int(len(solution)/width)

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

NBRPOS = nbrs_array(solution) 

def nbrs(pzl):
    upos = pzl.find("_")
    return[swap(pzl, upos, sp) for sp in NBRPOS[upos]]

solutionUPos = solution.find("_")
def inversion(pzl):
    inversions = len([item for sublist in[[k for k in pzl[pzl.find(n) + 1:]if k != '_' and n > k] for n in pzl if n != '_']for item in sublist])
    if width % 2 == 0:
        rowDifference = (pzl.find('_') // width - solutionUPos // width)
        return rowDifference % 2 == inversions % 2
    return inversions % 2 == 0

def pathToGoal(puzzledict, pzl, goal):
    path = []
    temp = goal
    while temp != pzl:
        path = [temp] + path
        temp = puzzledict[temp]
    return moveCalc([pzl] + path)

def h(pzl, goal):
    distance = 0
    for idx, val  in enumerate(pzl):
        if val != "_":
            gI = goal.index(val)
            rp = idx//width
            rg = gI//width
            cp = idx%width 
            cg = gI%width
            distance += abs(rp-rg) + abs(cp-cg)
    return distance

def solve(pzl, goal):
    if not inversion(pzl): return moveCalc([])
    openSet = [[] for i in range(81)]
    openSet[h(pzl,goal)] = [(0, pzl, None)]
    closedSet = {}
    fval = h(pzl,goal)
    while True:
        if openSet[fval]:
            fval = fval
        else:
            fval +=2
        node = openSet[fval].pop()
        if node[1] in closedSet: continue
        closedSet[node[1]] = node[2]
        if node[1] == goal: return pathToGoal(closedSet, pzl, goal)
        for nbr in nbrs(node[1]):
            newF = h(nbr, goal) + node[0]+1
            openSet[newF].append([node[0]+1, nbr, node[1]])

def moveCalc(puzzles):
    if not puzzles: return "X"
    if len(puzzles) == 1: return "G"
    moveLst = []
    for x in range(len(puzzles)-1):
        moveLst.append(puzzles[x].index("_") - puzzles[x+1].index("_"))
    finalStr = ''
    for move in moveLst:
        if move == -1:
            finalStr += "R"
        if move == 1:
            finalStr += "L"
        if move == width:
            finalStr += "U"
        if move == -width:
            finalStr += "D"
    return finalStr

for puzzle in puzzles:
    print(str(puzzle) + " " + str(solve(puzzle, solution)) + "\n")


#Gus Simanson, period 2, 2025