width = 2
solution = "ABCDEFGHIJKLMNO_"

def h(pzl, goal):
    distance = 0
    for i,v in enumerate(pzl):
        if v != "_":
            k = goal.index(v)
            r1, c1 = i//width, i%width
            r2,c2 = k//width, k%width
            distance += abs(r1-r2) + abs(c1-c2)
    return distance

for m in ["BCA_", "B_AC", "_BAC", "AB_C", "ABC_"]:
    print(str(h(m,solution)))

