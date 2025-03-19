import sys; args = sys.argv[1:]
#import time; startTime = time.time()

def setGlobals(args):
    board = ""
    tokenToPlay = ""
    moves = []
    global verbose; verbose = False
    global HLLIM; HLLIM = 8
    global posRatings; posRatings = [7, 2, 5, 4, 4, 5, 2, 7,
                                    2, 1, 3, 3, 3, 3, 1, 2,
                                    5, 3, 6, 5, 5, 6, 3, 5,
                                    4, 3, 5, 6, 6, 5, 3, 4,
                                    4, 3, 5, 6, 6, 5, 3, 4,
                                    5, 3, 6, 5, 5, 6, 3, 5,
                                    2, 1, 3, 3, 3, 3, 1, 2,
                                    7, 2, 5, 4, 4, 5, 2, 7]
    for arg in args:
        if len(arg) == 64 and ("x" in arg or "o" in arg):
            board = arg.lower()
        elif arg in "xXoO":
            tokenToPlay = arg.lower()
        elif arg == "-1":
            continue
        elif arg[:2] == "HL":
            HLLIM = int(arg[2:])
        elif str.isdigit(arg) and len(arg) < 3:
            moves.append(int(arg))
        elif len(arg) == 2 and arg[0].lower() in "abcdefgh":
            column = ord(arg[0].upper()) - ord('A')
            row = int(arg[1:]) - 1
            moves.append(column + row * 8)
        elif arg.lower() == "v":
            verbose = True
        else:
            for i in range(0, len(arg), 2):
                move = arg[i: i+2]
                if move[0] == '_':
                    moves.append(int(move[1]))
                elif move[0] == "-":
                    continue
                else: moves.append(int(move))

    if not board: board = "...........................ox......xo..........................."
    if not tokenToPlay: 
        if (board.count('x') + board.count('o')) % 2 == 0:
            tokenToPlay = "x"
        else: 
            tokenToPlay = "o"

    rows = [[8*x + i for i in range(8)] for x in range(8)]
    columns = [[8*i + x for i in range(8)] for x in range(8)]
    leftDiagonals =  [[40, 49, 58], [32, 41, 50, 59], [24, 33, 42, 51, 60], [16, 25, 34, 43, 52, 61], [8, 17, 26, 35, 44, 53, 62], [0, 9, 18, 27, 36, 45, 54, 63], [1, 10, 19, 28, 37, 46, 55], [2, 11, 20, 29, 38, 47], [3, 12, 21, 30, 39], [4, 13, 22, 31], [5, 14, 23]]
    rightDiagonals = [[2, 9, 16], [3, 10, 17, 24], [4, 11, 18, 25, 32], [5, 12, 19, 26, 33, 40], [6, 13, 20, 27, 34, 41, 48], [7, 14, 21, 28, 35, 42, 49, 56], [15, 22, 29, 36, 43, 50, 57], [23, 30, 37, 44, 51, 58], [31, 38, 45, 52, 59], [39, 46, 53, 60], [47, 54, 61]]
    global nbrTable; nbrTable = [([val for row in rows for val in row if x in row], [val for column in columns for val in column if x in column], [val for diag1 in rightDiagonals for val in diag1 if x in diag1], [val for diag2 in leftDiagonals for val in diag2 if x in diag2]) for x in range(64)]
    return board, tokenToPlay, moves

def display(board, tokenToPlay, move, nextT):
    print(f"\n{tokenToPlay} plays to {str(move)}")
    newBoard = [*board]
    pos = posMovesCached(board.lower(), nextT)
    if pos:
        for x in pos:
            newBoard[int(x)] = "*"
    newBoard = "".join(newBoard)
    print2d(newBoard)
    print(f"\n{board.lower()} {board.lower().count('x')}/{board.lower().count('o')}")
    if pos:
        print(f"Possible moves for {nextT}: {', '.join([str(p) for p in pos])}")
    else:
        print("No moves possible")
        exit()

def print2d(board):
    for r in range(8):  
        print("".join([board[i + r * 8] for i in range(8)]))
    
def posMoves(board, tokenToPlay):
    posMoves = set()
    oppToken = "xo".replace(tokenToPlay, "")
    for idx, val in enumerate(board):
        if val == tokenToPlay:
            row = nbrTable[idx][0]
            #look left
            if row.index(idx) != 0:
                x1 = row.index(idx) - 1
                if board[idx - 1] == oppToken:
                    while x1 >= 0 and board[row[x1]] == oppToken:
                        x1 = x1 - 1
                    if x1 >= 0 and board[row[x1]] == ".": posMoves.add(row[x1])
            # look right
            if row.index(idx) != 7:
                x2 = row.index(idx) + 1
                if board[idx + 1] == oppToken:
                    while x2 < len(row) and board[row[x2]] == oppToken:
                        x2 = x2 + 1
                    if x2 < len(row) and board[row[x2]] == ".": posMoves.add(row[x2])

            column = nbrTable[idx][1]
            # look up
            if column.index(idx) != 0:
                x1 = column.index(idx) - 1
                if board[idx - 8] == oppToken:
                    while x1 >= 0 and board[column[x1]] == oppToken:
                        x1 = x1 - 1
                    if x1 >= 0 and board[column[x1]] == ".": posMoves.add(column[x1])
            # look down
            if column.index(idx) != 7:
                x2 = column.index(idx) + 1
                if board[idx + 8] == oppToken:
                    while x2 < len(column) and board[column[x2]] == oppToken:
                        x2 = x2 + 1
                    if x2 < len(column) and board[column[x2]] == ".": posMoves.add(column[x2])

            diag1 = nbrTable[idx][2]
            if diag1:
                # look up diagonal
                if diag1.index(idx) != 0:
                    x1 = diag1.index(idx) - 1
                    if board[idx - 7] == oppToken:
                        while x1 > 0 and board[diag1[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 > -1 and board[diag1[x1]] == ".": posMoves.add(diag1[x1])
                # look down diagonal
                if diag1.index(idx) != len(diag1)-1:
                    x2 = diag1.index(idx) + 1
                    if board[idx + 7] == oppToken:
                        while x2 < len(diag1) and board[diag1[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(diag1) and board[diag1[x2]] == ".": posMoves.add(diag1[x2])

            diag2 = nbrTable[idx][3]
            if diag2:
                # look up diagonal
                if diag2.index(idx) != 0:
                    x1 = diag2.index(idx) - 1
                    if board[idx - 9] == oppToken:
                        while x1 > 0 and board[diag2[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 > -1 and board[diag2[x1]] == ".": posMoves.add(diag2[x1])
                # look down diagonal
                if diag2.index(idx) != len(diag2)-1:
                    x2 = diag2.index(idx) + 1
                    if board[idx + 9] == oppToken:
                        while x2 < len(diag2) and board[diag2[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(diag2) and board[diag2[x2]] == ".": posMoves.add(diag2[x2])
    return posMoves

POSMOVESCACHE = {}
def posMovesCached(brd, token):
    key = (brd.lower(), token)
    if key in POSMOVESCACHE:
        return POSMOVESCACHE[key]
    else:
        pos = posMoves(brd.lower(), token)
        POSMOVESCACHE[key] = pos
        return pos

def placeMove(board, move, tokenToPlay):
    oppToken = "xo".replace(tokenToPlay, "")
    temp = [*board]
    row = nbrTable[move][0]
    col = nbrTable[move][1]
    diagR = nbrTable[move][2]
    diagL = nbrTable[move][3]
    # Check and flip tokens in the row
    if row.index(move) != 0:
        RL = row.index(move) - 1
        while RL >= 0 and board[row[RL]] == oppToken:
            RL -= 1
        if RL >= 0 and board[row[RL]] == tokenToPlay:
            for i in range(row[RL], move):
                temp[i] = tokenToPlay
    if row.index(move) != 7:
        RR = row.index(move) + 1
        while RR < len(row) and board[row[RR]] == oppToken:
            RR += 1
        if RR < len(row) and board[row[RR]] == tokenToPlay:
            for i in range(move, row[RR]):
                temp[i] = tokenToPlay

    # Check and flip tokens up and down in the column
    if col.index(move) != 0:
        CU = col.index(move) - 1
        while CU >= 0 and board[col[CU]] == oppToken:
            CU -= 1
        if CU >= 0 and board[col[CU]] == tokenToPlay:
            for i in range(col[CU], move, 8):
                temp[i] = tokenToPlay
    if col.index(move) != 7:
        CD = col.index(move) + 1
        while CD < len(col) and board[col[CD]] == oppToken:
            CD += 1
        if CD < len(col) and board[col[CD]] == tokenToPlay:
            for i in range(move + 8, col[CD], 8):
                temp[i] = tokenToPlay

    # Check and flip tokens in the left diagonal
    if diagL:
        if diagL.index(move) != 0:
            DL = diagL.index(move) - 1
            while DL >= 0 and board[diagL[DL]] == oppToken:
                DL -= 1
            if DL >= 0 and board[diagL[DL]] == tokenToPlay:
                for i in range(diagL[DL], move, 9):
                    temp[i] = tokenToPlay
        if diagL.index(move) != len(diagL)-1:
            DR = diagL.index(move) + 1
            while DR < len(diagL) and board[diagL[DR]] == oppToken:
                DR += 1
            if DR < len(diagL) and board[diagL[DR]] == tokenToPlay:
                for i in range(move, diagL[DR], 9):
                    temp[i] = tokenToPlay

    # Check and flip tokens in the right diagonal
    if diagR:
        if diagR.index(move) != 0:
            UR = diagR.index(move) - 1
            while UR >= 0 and board[diagR[UR]] == oppToken:
                UR -= 1
            if UR >= 0 and board[diagR[UR]] == tokenToPlay:
                for i in range(diagR[UR], move, 7):
                    temp[i] = tokenToPlay
        if diagR.index(move) != len(diagR)-1:
            UL = diagR.index(move) + 1
            while UL < len(diagR) and board[diagR[UL]] == oppToken:
                UL += 1
            if UL < len(diagR) and board[diagR[UL]] == tokenToPlay:
                for i in range(move, diagR[UL], 7):
                    temp[i] = tokenToPlay
    temp[move] = tokenToPlay.upper()
    temp = "".join(temp)
    return temp

PLACEMOVECACHE = {}
def placeMoveCached(board, move, tokenToPlay):
    key = (board.lower(), move, tokenToPlay)
    if key in PLACEMOVECACHE:
        return PLACEMOVECACHE[key]
    else:
        bd = placeMove(board.lower(), move, tokenToPlay)
        PLACEMOVECACHE[key] = bd
        return bd

def getNextToken(board, tokenToPlay):
    if posMovesCached(board, "xo".replace(tokenToPlay, "")):
        return "xo".replace(tokenToPlay, "")
    else: return tokenToPlay

def quickMove(brd, token):
    if not brd: global HLLIM; HLLIM = token; return
    if brd.count(".") <= HLLIM: return alphabeta(brd, token, -65, 65)[-1]
    return ruleOfThumb(brd, token)
    
def ruleOfThumb(brd, token):
    pos = posMovesCached(brd, token)
    tempPos = [mv for mv in pos]

    for p in pos: #avoid corners
        if p in [1, 8] and brd[0] != token:
            tempPos.remove(p)
            continue
        if p in [6, 14] and brd[7] != token:
            tempPos.remove(p)
            continue
        if p in [48, 57] and brd[56] != token:
            tempPos.remove(p)
            continue
        if p in [62, 55] and brd[63] != token:
            tempPos.remove(p)
            continue
    
    if len(tempPos) > 0:
        pos = tempPos
    else: pos = pos
    best = 64, 0 
    for p in pos:
        if p in [0, 7, 56, 63]: 
            return p
        if p in [8,16,24,32,40,48,15,23,31,39,47,55,1,2,3,4,5,6,57,58,59,60,61,62] and canBeRecap(brd, p, token) == False:
            return p
        else: 
            oppMoves = len(posMovesCached(placeMoveCached(brd, p, token), "xo".replace(token, "")))
            if oppMoves < best[0]:
                best = oppMoves, p
                continue
    return best[1]

def canBeRecap(brd, move, token):
    newb = placeMoveCached(brd, move, token)
    oppToken = "xo".replace(token, "")
    oppMoves = posMovesCached(newb, oppToken)
    for m in oppMoves:
        tempB = placeMoveCached(newb, m, oppToken)
        if tempB[move] == oppToken:
            return True
        continue
    return False

def getMoveValue(move):
    return posRatings[move]

def alphabeta(brd, tkn, lowerBnd, upperBnd):
    #returns a list of best possible score than can be achieved alongside optimal reversed move sequence that gets tkn there
    brd = brd.lower()
    eTkn = "xo".replace(tkn, "")
    moves = posMovesCached(brd, tkn)
    moves = [*moves]
    moves.sort(reverse=True, key=getMoveValue)
    eMoves = posMovesCached(brd, eTkn)

    if len(moves) == 0 and len(eMoves) == 0: return [brd.count(tkn)-brd.count(eTkn)] #game over
    if len(moves) == 0 and len(eMoves) > 0: #token cant move but eToken can
        ab = alphabeta(brd, eTkn, -upperBnd, -lowerBnd)
        return [-ab[0]] + ab[1:] + [-1]
    
    best = [lowerBnd-1]
    for move in moves:
        newBrd = placeMoveCached(brd, move, tkn)
        ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd)
        score = -ab[0]
        if score < lowerBnd: continue
        if score > upperBnd: return [score]
        best = [-ab[0]] + ab[1:] + [move]
        lowerBnd = score + 1
    return best

moveListMem = []
def main():
    board, tokenToPlay, moves = setGlobals(args)
    pos = posMovesCached(board, tokenToPlay)
    if not pos:
        tokenToPlay = "xo".replace(tokenToPlay, "")
        pos = posMovesCached(board, tokenToPlay)
    newBoard = [*board]
    if pos:
        for x in pos:
            newBoard[int(x)] = "*"
    newBoard = "".join(newBoard)
    print2d(newBoard)
    print(f"\n{board} {board.count('x')}/{board.count('o')}")
    if pos:
        print(f"Possible moves for {tokenToPlay}: {', '.join([str(p) for p in pos])}")
    else:
        print("No moves possible")
        exit()
    for move in moves:
        board = board.lower()
        board = placeMoveCached(board, move, tokenToPlay)
        nextToken = getNextToken(board, tokenToPlay)
        if verbose:
            display(board, tokenToPlay, move, nextToken)
        moveListMem.append((move, tokenToPlay))
        tokenToPlay = nextToken
    if not verbose and len(moves) > 0:
        display(board, moveListMem[-1][1], moveListMem[-1][0], nextToken)
    if "." in board:
        prefMove = quickMove(board.lower(), tokenToPlay)
        print(f"my preffered move is: {str(prefMove)}")
        if board.count('.') <= HLLIM:
            nm = alphabeta(board.lower(), tokenToPlay, -65, 65)
            print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")

board, tokenToPlay, moves = setGlobals(args)

if __name__ == "__main__": main()
#Gus Simanson, period 2, 2025