import sys; args = sys.argv[1:]
import time; startTime = time.time()

def setGlobals(args):
    board = ""
    tokenToPlay = ""
    for arg in args:
        if len(arg) == 64:
            board = arg.lower()
        if arg in "xXoO":
            tokenToPlay = arg.lower()
    if not board: board = "...........................ox......xo..........................."
    if not tokenToPlay: 
        if (board.count("x") + board.count("o")) % 2 == 0:
            tokenToPlay = "x"
        else: 
            tokenToPlay = "o"

    global rows; rows = [[8*x + i for i in range(8)] for x in range(8)]
    global columns; columns = [[8*i + x for i in range(8)] for x in range(8)]
    global leftDiagonals; leftDiagonals =  [[40, 49, 58], [32, 41, 50, 59], [24, 33, 42, 51, 60], [16, 25, 34, 43, 52, 61], [8, 17, 26, 35, 44, 53, 62], [0, 9, 18, 27, 36, 45, 54, 63], [1, 10, 19, 28, 37, 46, 55], [2, 11, 20, 29, 38, 47], [3, 12, 21, 30, 39], [4, 13, 22, 31], [5, 14, 23]]
    global rightDiagonals; rightDiagonals = [[2, 9, 16], [3, 10, 17, 24], [4, 11, 18, 25, 32], [5, 12, 19, 26, 33, 40], [6, 13, 20, 27, 34, 41, 48], [7, 14, 21, 28, 35, 42, 49, 56], [15, 22, 29, 36, 43, 50, 57], [23, 30, 37, 44, 51, 58], [31, 38, 45, 52, 59], [39, 46, 53, 60], [47, 54, 61]]
    return board, tokenToPlay


def display(board, tokenToPlay):
    pos = posMoves(board, tokenToPlay)
    newBoard = [*board]
    if pos:
        for x in pos:
            newBoard[x] = "*"
    newBoard = "".join(newBoard)
    for r in range(8):  
        print("".join([newBoard[i + r * 8] for i in range(8)]))
    if pos:
        print(pos)
    else: print("No moves possible")
    
def posMoves(board, tokenToPlay):
    posMoves = set()
    oppToken = "xo".replace(tokenToPlay, "")
    for idx, val in enumerate(board):
        if val == tokenToPlay:
            for row in rows:
                if idx in row:
                    x1 = row.index(idx) - 1
                    x2 = row.index(idx) + 1
                    #look left
                    if idx != row[0] and board[idx - 1] == oppToken:
                        while x1 >= 0 and board[row[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 >= 0 and board[row[x1]] == ".": posMoves.add(row[x1])
                    # look right
                    if idx != row[7] and board[idx + 1] == oppToken:
                        while x2 < len(row) and board[row[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(row) and board[row[x2]] == ".": posMoves.add(row[x2])

            for column in columns:
                if idx in column:
                    x1 = column.index(idx) - 1
                    x2 = column.index(idx) + 1
                    # look up
                    if idx != column[0] and board[idx - 8] == oppToken:
                        while x1 >= 0 and board[column[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 >= 0 and board[column[x1]] == ".": posMoves.add(column[x1])
                    # look down
                    if idx != column[7] and board[idx + 8] == oppToken:
                        while x2 < len(column) and board[column[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(column) and board[column[x2]] == ".": posMoves.add(column[x2])

            for diag1 in rightDiagonals:
                if idx in diag1:
                    x1 = diag1.index(idx) - 1
                    x2 = diag1.index(idx) + 1
                    # look up diagonal
                    if idx != diag1[0] and board[idx - 7] == oppToken:
                        while x1 > 0 and board[diag1[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 > -1 and board[diag1[x1]] == ".": posMoves.add(diag1[x1])
                    # look down diagonal
                    if idx != max(diag1) and board[idx + 7] == oppToken:
                        while x2 < len(diag1) and board[diag1[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(diag1) and board[diag1[x2]] == ".": posMoves.add(diag1[x2])

            for diag2 in leftDiagonals:
                if idx in diag2:
                    x1 = diag2.index(idx) - 1
                    x2 = diag2.index(idx) + 1
                    # look up diagonal
                    if idx != diag2[0] and board[idx - 9] == oppToken:
                        while x1 > 0 and board[diag2[x1]] == oppToken:
                            x1 = x1 - 1
                        if x1 > -1 and board[diag2[x1]] == ".": posMoves.add(diag2[x1])
                    # look down diagonal
                    if idx != max(diag2) and board[idx + 9] == oppToken:
                        while x2 < len(diag2) and board[diag2[x2]] == oppToken:
                            x2 = x2 + 1
                        if x2 < len(diag2) and board[diag2[x2]] == ".": posMoves.add(diag2[x2])
    return posMoves
                
board, tokenToPlay = setGlobals(args)
display(board, tokenToPlay)
exit()

#Gus Simanson, period 2, 2025


