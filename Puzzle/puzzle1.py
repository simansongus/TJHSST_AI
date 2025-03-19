import sys; args = sys.argv[1:]
n = int(args[0])
possibilities = [x+1 for x in range(n)]
board = "." * (n**2)

def isInvalid(pzl):
    for x in possibilities:
        for r in range(n):
            row = [pzl[i + r * n] for i in range(n)]
            if row.count(str(x)) > 1:
                return True
        for c in range(n):
            if [val for idx, val in enumerate(pzl) if (idx-c)%n == 0].count(str(x)) > 1:
                return True
        if[pzl[i + i * n] for i in range(n)].count(str(x)) > 1:
            return True
        if [pzl[i + (n - 1 - i) * n] for i in range(n)].count(str(x)) > 1:
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
    for r in range(n):  
        print("".join([solution[i + r * n] for i in range(n)]))
