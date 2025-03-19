import sys; args = sys.argv[1:]
possibilities = [x+1 for x in range(6)]
if len(args) > 0:
    board = args[0] 
else:
    board = "." * 24

def isInvalid(pzl):
    for x in possibilities:
        if (pzl[0:3] + pzl[6:9]).count(str(x)) > 1:
                return True
        if (pzl[2:5] + pzl[8:11]).count(str(x)) > 1:
                return True
        if (pzl[5:8] + pzl[12:15]).count(str(x)) > 1:
                return True
        if (pzl[7:10] + pzl[14:17]).count(str(x)) > 1:
                return True
        if (pzl[9:12] + pzl[16:19]).count(str(x)) > 1:
                return True
        if (pzl[13:16] + pzl[19:22]).count(str(x)) > 1:
                return True
        if (pzl[15:18] + pzl[22:]).count(str(x)) > 1:
                return True     
    return False

def bruteForce(pzl):
    if isInvalid(pzl): return ""
    if "." not in pzl: return pzl
    for x in possibilities:
        idx = pzl.index(".")
        subPzl = pzl[:idx] + str(x) + pzl[idx+1:]
        bF = bruteForce(subPzl)
        if bF: return bF
    return ""
            
solution = bruteForce(board)

if solution == "":
    print("No Solution :(")
else:
    print(" " + "".join(solution[:5]))
    print("".join(solution[5:12]))
    print("".join(solution[12:19]))
    print(" " + "".join(solution[19:]))