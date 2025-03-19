finalBoards = set()
global k; k = 3
global boardCt; boardCt = 0

def posMoves(brd):
    return [idx for idx, val in enumerate(brd) if val == "."]
       
def placeMove(brd, tkn, move):
    temp = [*brd]
    temp[move] = tkn
    return "".join(temp)

def tictactoeCt(brd, token):
    BSDF = [(0,1),(0,k),(3,1),(1,k),(6,1),(3,k),(0,k+1),(k-1,k-1)]
    triples = [brd[bs:bs+3*df:df] for bs,df in BSDF]
    return triples.count(token*3)

def score(brd):
    return (tictactoeCt(brd,"x")>0) - (tictactoeCt(brd, "o") > 0)

def isOver(brd):
    return True if "." not in brd else False
    
def runGames(brd, token):
    global boardCt
    for move in posMoves(brd):
        boardCt += 1
        brd = placeMove(brd, token, move)
        if tictactoeCt(brd, token) > 0:
            boardCt+=1
            finalBoards.add(brd)
        else:
            runGames(brd, "xo".replace(token, ""))

runGames(".........", "x")
print(len(finalBoards))
print((boardCt))
    