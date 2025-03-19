import sys; args = sys.argv[1:]
import time; startTime = time.time()
import math
puzzle = ""
puzzles = []
if ".txt" not in args[0]:
    puzzle = args[0]
else:
    puzzles = open(args[0]).read().splitlines()


def setGlobals(puzzle):
    global n
    n = int(math.sqrt(len(puzzle)))
    global subW 
    global subH
    subH = int(math.sqrt(n)) #blocks per row also
    subW = int(n/subH) #blocks per column also
    global SYMSET 
    SYMSET = "123456789abcdefghijk"[:n]
    global constraintSet
    rows = [{n*j + i for i in range(n)} for j in range(n)]
    columns = [{n*i + j for i in range(n)} for j in range(n)]
    squares = [{((subH*c+b*n)+(d*n*subW+a)) for a in range(subW) for b in range(subH)} for c in range(subW) for d in range(subH)]
    constraintSet = rows + columns + squares
    global nbrTable
    nbrTable = [{value for constraint in constraintSet if x in constraint for value in constraint if value != x} for x in range(len(puzzle))]

def isInvalid(pzl,lastIdx):
    if lastIdx == 500:
        for x in constraintSet:
            for i in x:
                for j in x:
                    if (i != j) and (pzl[i] == pzl[j]) and "." != pzl[i]:
                        return True
    else:
         for x in nbrTable[lastIdx]:
            if pzl[lastIdx] == pzl[x]: return True
    return False

def bruteForce(pzl,lastIdx):
    if isInvalid(pzl,lastIdx): return ""
    if "." not in pzl: return pzl
    for x in SYMSET:
        idx = pzl.index(".")
        subPzl = pzl[:idx] + str(x) + pzl[idx+1:]
        bF = bruteForce(subPzl,idx)
        if bF: return bF
    return ""

def checkSum(pzl):
    asc = [ord(x) for x in pzl]
    return sum(y-min(asc) for y in asc)

if len(puzzle) > 0:
    setGlobals(puzzle)
    print(puzzle + "\n")
    answer = bruteForce(puzzle,100)
    for r in range(n):  
        print("".join([answer[i + r * n] for i in range(n)]))
    print(f"{checkSum(answer)} {str(time.time()-startTime)[:4]}s")
else:
    ctr = 1
    for pzl in puzzles:
        pzlTime = time.time()
        setGlobals(pzl)
        answer = bruteForce(pzl,500)
        if ctr < 10:
            print(f"{ctr}: {pzl}")
            print(f"   {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1
        elif ctr < 100:
            print(f"{ctr}: {pzl}")
            print(f"    {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1
        else:
            print(f"{ctr}: {pzl}")
            print(f"    {answer} {checkSum(answer)} {str(time.time()-pzlTime)[:3]}s")
            ctr += 1

print(str(time.time()-startTime)[:3])
#Gus Simanson, period 2, 2025