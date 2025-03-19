
def moveCalc(puzzles):
    width = int(len(puzzles[0]) ** .5)
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

print(moveCalc(["BCA_", "B_AC", "_BAC", "AB_C", "ABC_"]))

