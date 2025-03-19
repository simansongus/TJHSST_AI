import sys; args = sys.argv[1:]
import time; startTime = time.time()
import math
STATS = {}
puzzle = ""
puzzles = []
if ".txt" not in args[0]:
    puzzle = args[0]
else:
    puzzles = open(args[0]).read().splitlines()

def setGlobals(puzzle):
    global n; n = int(math.sqrt(len(puzzle)))
    global subH; subH = int(n  ** .5)
    global subW; subW = n//subH
    global SYMSET ; SYMSET = set(puzzle) - {"."}
    if len(SYMSET) < n:
        possibles = set("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") - SYMSET
        to_add = list(possibles)[:n - len(SYMSET)]
        SYMSET.update(to_add)
    global constraintSet
    rows = [{n*x + i for i in range(n)} for x in range(n)]
    columns = [{n*i + x for i in range(n)} for x in range(n)]
    squares = [{x + y + i * n + j for i in range(subH) for j in range(subW)} for x in range(0, len(puzzle), subH * n) for y in range(0, n, subW)]
    constraintSet = rows + columns + squares
    global nbrTable; nbrTable = [{value for constraint in constraintSet if x in constraint for value in constraint if value != x} for x in range(len(puzzle))]
    global possibleValueTable; possibleValueTable = {i:SYMSET - nbrValues(puzzle,i) for i, x in enumerate(puzzle) if  x == '.'}

def isInvalid(pzl,lastIdx):
    if lastIdx == 500:
        for x in constraintSet:
            for i in x:
                for j in x:
                    if (i != j) and (pzl[i] == pzl[j]) and "." != pzl[i]:
                        updateStats("II True")
                        return True
    else:
        for x in nbrTable[lastIdx]:
            if pzl[lastIdx] == pzl[x]: return True
    return False

def bestIndexCalc(possibilities):
    bestPos = (SYMSET, 0)
    for i in possibilities:
        temp = (possibilities[i], i)
        if len(temp[0]) == 1: 
            bestPos = temp
            break
        if len(temp[0]) < len(bestPos[0]): 
            bestPos = temp
    return bestPos

def bestSymbolCalc(possibles):
    for sym in SYMSET:
        posIdx = None
        symCount = 0 
        for cs in constraintSet:  
            tempLst = [idx for idx in cs if idx in possibles and sym in possibles[idx]]
            if len(tempLst) == 1:
                if symCount == 0 or len(tempLst) < symCount:
                    posIdx = tempLst[0]
                    symCount = 1
                elif len(tempLst) > 1:
                    break
        if symCount == 1:
            return {sym}, posIdx
    return None

def nakedPairs(possibles):
    newPsbl = possibles.copy()
    for cs in constraintSet:
        for pos in cs:
            for pos2 in cs:
                if pos in newPsbl and pos2 in newPsbl and pos2 != pos:
                    if len(newPsbl[pos]) == 2 and (newPsbl[pos] == newPsbl[pos2]):
                        commonSyms = newPsbl[pos]
                        for pos3 in cs:
                            if pos3 in possibles and pos3 != pos and pos3 != pos2:
                                for sym in commonSyms:
                                    if sym in possibles[pos3]:
                                        updateStats("nakedPair")
                                        newPsbl[pos3] = newPsbl[pos3] - {sym}
    return newPsbl


def nbrValues(pzl, idx):
    return {pzl[x] for x in nbrTable[idx] if pzl[x] != '.'}

def bruteForce(pzl,lastIdx, possibles):
    if isInvalid(pzl, lastIdx): return ""
    updateStats("II False")
    if "." not in pzl: return pzl
    choices, bestIdx = bestIndexCalc(possibles)

    if len(choices) > 1:
        temp = bestSymbolCalc(possibles)
        if temp:
            choices, bestIdx = temp

    updateStats(str(len(choices)))
    for val in choices:
        subPzl = pzl[:bestIdx] + str(val) + pzl[bestIdx + 1:]
        newPsbl = possibles.copy()
        for i in nbrTable[bestIdx]:
            if i in newPsbl:
                if val in newPsbl[i]:
                    newPsbl[i] = newPsbl[i] - {val}
        if bestIdx in newPsbl:
            newPsbl.pop(bestIdx)
        #newPsbl = nakedPairs(newPsbl)
        bF = bruteForce(subPzl, bestIdx, newPsbl)
        if bF: return bF
    return ""

def updateStats(keyPhrase):
    if keyPhrase not in STATS: STATS[keyPhrase] = 1
    else: STATS[keyPhrase] += 1

def checkSum(pzl):
    if not pzl:
        return ""
    asc = [ord(x) for x in pzl]
    return sum(y-min(asc) for y in asc)


if len(puzzle) > 0:
    setGlobals(puzzle)
    print(puzzle + "\n")
    answer = bruteForce(puzzle, 500, possibleValueTable)
    for r in range(n):  
        print("".join([answer[i + r * n] for i in range(n)]))
    print(f"{checkSum(answer)} {str(time.time()-startTime)[:4]}s")
else:
    ctr = 1
    for pzl in puzzles:
        pzlTime = time.time()
        print(f"{ctr}: {pzl}")
        setGlobals(pzl)
        answer = bruteForce(pzl,500, possibleValueTable)
        if ctr < 10:
            print(f"   {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1
        elif ctr < 100:
            print(f"    {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1
        else:
            print(f"     {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1
            
print(str(time.time()-startTime)[:3] + "s")

print("1 Possibility Occuring: " + str(STATS["1"]))
print("2 Possibilities Occuring: " + str(STATS["2"]))
print("IIFALSE: " + str(STATS["II False"]))
#print("nakeds: " + str(STATS["nakedPair"]))
                    
#Gus Simanson, period 2, 2025

