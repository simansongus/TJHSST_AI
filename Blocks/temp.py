import sys; args = sys.argv[1:]
import re

NUMBLOCKS = 0
HEIGHT = 0
WIDTH = 0
SEEDS = []
BLOCKCHAR = "#"
OPENCHAR = "-"
CROSSWORD = ""
ROWS_COLS = {}
INDEXES = {}
ROTATE_DCT = {}
WORD_DICT = set()
WORD_LIST = ""
VERTICAL_WORDS = set()
HORIZONTAL_WORDS = set()
ALL_WORDS = set()
LENGTH_TO_WORD = {}
CS_POSSIBLE_WORDS = {}
IDX_VERTICAL = {}
IDX_HORIZONTAL = {}

def setGlobals(args):
    global NUMBLOCKS
    global HEIGHT
    global WIDTH
    global CROSSWORD
    global SEEDS
    global ROWS_COLS
    global INDEXES
    global ROTATE_DCT
    global WORD_DICT
    global LENGTH_TO_WORD
    global WORD_LIST
    with open(args[0]) as infile:
        for line in infile:
            line = line.strip().lower()
            if len(line) >= 3:
                word = re.search("^[a-z]+$", line)
                if word:
                    word = word.group(0)
                    key = len(word)
                    if key not in LENGTH_TO_WORD:
                        LENGTH_TO_WORD[key] = [word]
                    else:
                        LENGTH_TO_WORD[key].append(word)
                    WORD_DICT.add(word)
    for arg in args:
        if ".txt" in arg or ".dct" in arg:
            continue
        elif arg[0] in "1234567890" and "x" in arg.lower(): #dimensions
            HEIGHT = int(arg[:arg.lower().index("x")])
            WIDTH = int(arg[arg.lower().index("x")+1:])
        elif arg[0] in "1234567890" and "x" not in arg.lower():
            NUMBLOCKS = int(arg)
        elif arg[0].upper() == "V" or arg[0].upper() == "H":
            SEEDS.append(arg)
    CROSSWORD = OPENCHAR * (HEIGHT*WIDTH)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            INDEXES[(r,c)] = r*WIDTH + c
            ROWS_COLS[r*WIDTH + c] = (r,c)
    ROTATE_DCT = {i: abs(i-(WIDTH*HEIGHT)+1) for i in range(WIDTH*HEIGHT)}
    WORD_LIST = "\n".join([*WORD_DICT])

########################################
def placeSeeds(board, seeds):
    new_board = list(board)
    for seed in seeds:
        orientation = seed[0].upper()
        row = int(seed[1:seed.lower().index('x')])
        col = int("".join(seed[i] for i in range(seed.lower().index('x')+1, len(seed)) if seed[i] in '1234567890'))
        word = "".join(seed[i] for i in range(seed.lower().index('x')+2, len(seed)) if seed[i] not in '1234567890')
        if word == "":
            word = "#"
        idx = INDEXES[(row, col)]
        if orientation == "V":
            cur_row = row
            for i,v in enumerate(word):
                if cur_row < HEIGHT:
                    new_board[idx] = v
                    idx += WIDTH
                    cur_row += 1
        elif orientation == "H":
            cur_col = col
            for i,v in enumerate(word):
                if cur_col < WIDTH:
                    new_board[idx] = v
                    idx += 1
                    cur_col += 1
    return "".join(new_board)
def makeSymmetric(board):
    newBoard = list(board)
    for i,v in enumerate(board):
        if v == BLOCKCHAR:
            rotate_idx = ROTATE_DCT[i]
            newBoard[rotate_idx] = BLOCKCHAR
    return "".join(newBoard)

def fillConnected(board):
    newBoard = list(board)
    connected, start, end = isConnected(board)
    if not connected:
        r1, c1 = ROWS_COLS[start]
        r2, c2 = ROWS_COLS[end]
        for i in range(r1, r2):
            for j in range(c1, c2):
                idx = INDEXES[(i, j)]
                rotate_idx = ROTATE_DCT[idx]
                if newBoard[idx] == OPENCHAR:
                    newBoard[idx] = BLOCKCHAR
                    newBoard[rotate_idx] = BLOCKCHAR
    return "".join(newBoard)

def autofill(board):
    newBoard = list(board)
    for i,v in enumerate(board):
        if v == OPENCHAR:
            good = False
            row, col = ROWS_COLS[i]
            up1 = False
            up2 = False
            down1 = False
            down2 = False
            # up 1
            if row-1 >= 0 and board[INDEXES[(row-1, col)]] != BLOCKCHAR:
                up1 = True
            # up 2
            if row-2 >= 0 and board[INDEXES[(row-2, col)]] != BLOCKCHAR:
                up2 = True
            # down 1
            if row+1 < HEIGHT and board[INDEXES[(row+1, col)]] != BLOCKCHAR:
                down1 = True
            # down 2
            if row+2 < HEIGHT and board[INDEXES[(row+2, col)]] != BLOCKCHAR:
                down2 = True
            if (up2 and up1) or (up1 and down1) or (down1 and down2):
                good = True
            else:
                if newBoard[ROTATE_DCT[i]] == OPENCHAR:
                    newBoard[i] = BLOCKCHAR
                    rotate_idx = ROTATE_DCT[i]
                    newBoard[rotate_idx] = BLOCKCHAR
            left1 = False
            left2 = False
            right1 = False
            right2 = False
            # left 1
            if col-1 >= 0 and board[INDEXES[(row, col-1)]] != BLOCKCHAR:
                left1 = True
            # left 2
            if col-2 >= 0 and board[INDEXES[(row, col-2)]] != BLOCKCHAR:
                left2 = True
            # right 1
            if col+1 < WIDTH and board[INDEXES[(row, col+1)]] != BLOCKCHAR:
                right1 = True
            # right 2
            if col+2 < WIDTH and board[INDEXES[(row, col+2)]] != BLOCKCHAR:
                right2 = True
            if (left2 and left1) or (left1 and right1) or (right1 and right2):
                good = True
            else:
                if newBoard[ROTATE_DCT[i]] == OPENCHAR:
                    newBoard[i] = BLOCKCHAR
                    rotate_idx = ROTATE_DCT[i]
                    newBoard[rotate_idx] = BLOCKCHAR
    connected, dr, idx = checkConnected(newBoard)
    r,c = ROWS_COLS[idx]
    if not connected:
        if dr == "UL":
            for i in range(0, r):
                for j in range(0, c):
                    idx = INDEXES[(i, j)]
                    if newBoard[idx] == OPENCHAR:
                        newBoard[idx] = BLOCKCHAR
                        rotate_idx = ROTATE_DCT[idx]
                        newBoard[rotate_idx] = BLOCKCHAR
        elif dr == "UR":
            for i in range(0, r):
                for j in range(c, WIDTH):
                    idx = INDEXES[(i, j)]
                    if newBoard[idx] == OPENCHAR:
                        newBoard[idx] = BLOCKCHAR
                        rotate_idx = ROTATE_DCT[idx]
                        newBoard[rotate_idx] = BLOCKCHAR
        elif dr == "DL":
            for i in range(r, HEIGHT):
                for j in range(0, c):
                    idx = INDEXES[(i, j)]
                    if newBoard[idx] == OPENCHAR:
                        newBoard[idx] = BLOCKCHAR
                        rotate_idx = ROTATE_DCT[idx]
                        newBoard[rotate_idx] = BLOCKCHAR
        elif dr == "DR":
            for i in range(r, HEIGHT):
                for j in range(c, WIDTH):
                    idx = INDEXES[(i, j)]
                    if newBoard[idx] == OPENCHAR:
                        newBoard[idx] = BLOCKCHAR
                        rotate_idx = ROTATE_DCT[idx]
                        newBoard[rotate_idx] = BLOCKCHAR
    return "".join(newBoard)


def print2d(board):
    for i in range(HEIGHT):
        row = ""
        for j in range(WIDTH):
            row += board[WIDTH*i + j]
        print(row)
def checkConnected(board):
    idx = -1
    for i,v in enumerate(board):
        if v == BLOCKCHAR:
            idx = i
            r,c = ROWS_COLS[idx]
            up = True
            temp_row = r
            while temp_row >= 0:
                if board[INDEXES[(temp_row), c]] != BLOCKCHAR:
                    up = False
                    break
                temp_row -= 1
            down = True
            temp_row = r
            while temp_row < HEIGHT:
                if board[INDEXES[(temp_row), c]] != BLOCKCHAR:
                    down = False
                    break
                temp_row += 1
            left = True
            temp_col = c
            while temp_col >= 0:
                if board[INDEXES[(r, temp_col)]] != BLOCKCHAR:
                    left = False
                    break
                temp_col -= 1
            right = True
            temp_col = c
            while temp_col < WIDTH:
                if board[INDEXES[(r, temp_col)]] != BLOCKCHAR:
                    right = False
                    break
                temp_col += 1
            if up:
                if left:
                    return (False, 'UL', idx)
                if right:
                    return (False, 'UR', idx)
            if down:
                if left:
                    return (False, 'DL', idx)
                if right:
                    return (False, 'DR', idx)
    return (True, True, True)

def rotate(oldRect):
    global HEIGHT
    global WIDTH
    newRect = "".join([oldRect[rowStart-offset] for rowStart in range(WIDTH*HEIGHT-WIDTH, WIDTH*HEIGHT) for offset in range(0, WIDTH*HEIGHT, WIDTH)])
    temp = HEIGHT
    HEIGHT = WIDTH
    WIDTH = temp
    return newRect
def isConnected(board): #TODO
    for i in range(len(board)//2):
        v = board[i]
        if v == OPENCHAR:
            r,c = ROWS_COLS[i]
            if (r==0 or (r-1 >=0 and board[INDEXES[(r-1, c)]] == BLOCKCHAR)) and (c==0 or (c-1 >= 0 and board[INDEXES[(r, c-1)]] == BLOCKCHAR)):
                # Down
                edgeUp = False
                edgeDown = False
                edgeLeft = False
                edgeRight = False
                down = False
                dright = False
                idx = i
                while idx < len(board) and board[idx] != BLOCKCHAR:
                    if c == 0:
                        edgeLeft = True
                    elif board[idx-1] != BLOCKCHAR:
                        down = True # Safe
                    idx += WIDTH
                idx -= WIDTH
                tempR, tempc = ROWS_COLS[idx]
                while tempc < WIDTH and board[idx] != BLOCKCHAR:
                    if tempR + 1 == HEIGHT:
                        edgeDown = True
                    elif board[idx+WIDTH] != BLOCKCHAR:
                        dright = True
                    idx += 1
                    tempc += 1
                # Right
                right = False
                rdown = False
                idx = i
                tempc = c
                while tempc < WIDTH and board[idx] != BLOCKCHAR:
                    if r == 0:
                        edgeUp = True
                    elif board[idx-WIDTH] != BLOCKCHAR:
                        right = True # Safe
                    idx += 1
                    tempc += 1
                idx -= 1
                b, tempc = ROWS_COLS[idx]
                while idx < len(board) and board[idx] != BLOCKCHAR:
                    if tempc+1 == WIDTH:
                        edgeRight = True
                    elif board[idx+1] != BLOCKCHAR:
                        rdown = True
                    idx += WIDTH
                idx -= WIDTH
                if edgeUp and edgeDown and edgeLeft and edgeRight:
                    return (True, True, True)
                r1, c1 = ROWS_COLS[i]
                r2, c2 = ROWS_COLS[idx]
                if (r2+1-r1)*(c2+1-c1) < len(board)-board.count(BLOCKCHAR):
                    if edgeUp:
                        if edgeRight and not down and not dright:
                            return (False, i, idx)
                        if edgeLeft and not dright and not rdown:
                            return (False, i, idx)
                        if not down and not dright and not rdown:
                            return (False, i, idx)
                    if edgeDown:
                        if edgeLeft and not right and not rdown:
                            return (False, i, idx)
                        if edgeRight and not right and not down:
                            return (False, i, idx)
                        if not down and not right and not rdown:
                            return (False, i, idx)
                    if not (down or right or dright or rdown):
                        return (False, i, idx)
                
    return (True, True, True)
def isValid(board):
    # Block positions must be symmetric with respect to 180 degree rotation about the center. DONE
    # All letters must be in both a horizontal and vertical word. DONE
    # All words must be at least three letters. DONE
    # All non-block entries should be connected.
    # No duplicate words in the crossword.
    for i,v in enumerate(board):
        if v != BLOCKCHAR:
            good = False
            row, col = ROWS_COLS[i]
            up1 = False
            up2 = False
            down1 = False
            down2 = False
            # up 1
            if row-1 >= 0 and board[INDEXES[(row-1, col)]] != BLOCKCHAR:
                up1 = True
            # up 2
            if row-2 >= 0 and board[INDEXES[(row-2, col)]] != BLOCKCHAR:
                up2 = True
            # down 1
            if row+1 < HEIGHT and board[INDEXES[(row+1, col)]] != BLOCKCHAR:
                down1 = True
            # down 2
            if row+2 < HEIGHT and board[INDEXES[(row+2, col)]] != BLOCKCHAR:
                down2 = True
            if (up2 and up1) or (up1 and down1) or (down1 and down2):
                good = True
            else:
                return False
            left1 = False
            left2 = False
            right1 = False
            right2 = False
            # left 1
            if col-1 >= 0 and board[INDEXES[(row, col-1)]] != BLOCKCHAR:
                left1 = True
            # left 2
            if col-2 >= 0 and board[INDEXES[(row, col-2)]] != BLOCKCHAR:
                left2 = True
            # right 1
            if col+1 < WIDTH and board[INDEXES[(row, col+1)]] != BLOCKCHAR:
                right1 = True
            # right 2
            if col+2 < WIDTH and board[INDEXES[(row, col+2)]] != BLOCKCHAR:
                right2 = True
            if (left2 and left1) or (left1 and right1) or (right1 and right2):
                good = True
            else:
                return False 
    # a,b,c = checkConnected(board)
    # return a
    return isConnected(board)[0]
    
def getNeighbors(board):
    neighbors = []
    for i,v in enumerate(board):
        if v == OPENCHAR:
            rotate_idx = ROTATE_DCT[i]
            if board[rotate_idx] != OPENCHAR:
                continue
            else:
                newBoard = list(board)
                newBoard[i] = BLOCKCHAR
                newBoard[rotate_idx] = BLOCKCHAR
                neighbors.append("".join(newBoard))
    return neighbors
def bruteForce(board):
    board = fillConnected(board)
    if board.count(OPENCHAR) + board.count(BLOCKCHAR) == len(board):
        board = autofill(board)
    # if board.count("#") > NUMBLOCKS:
    #     return ""
    if not isValid(board):
        return ""
    if board.count("#") == NUMBLOCKS:
        return board
    neighbors = getNeighbors(board)
    for choice in neighbors:
        sub_board = choice
        bf = bruteForce(sub_board)
        if bf:
            return bf
    return ""

def placeWord(board, word, pos, orientation):
    newBoard = list(board)
    idx = pos
    if orientation == "V":
        for i in range(len(word)):
            if newBoard[idx].lower() == word[i] or newBoard[idx] == OPENCHAR:
                newBoard[idx] = word[i]
                idx += WIDTH
            else:
                return ""
    else:
        for i in range(len(word)):
            if newBoard[idx].lower() == word[i] or newBoard[idx] == OPENCHAR:
                newBoard[idx] = word[i]
                idx += 1
            else:
                return ""
    return "".join(newBoard)
    
def getWordConstraints(board):
    global VERTICAL_WORDS
    global HORIZONTAL_WORDS
    global ALL_WORDS
    global IDX_VERTICAL
    global IDX_HORIZONTAL

    for i,v in enumerate(board):
        r,c = ROWS_COLS[i]
        # Find locations of all horizontal words
        if v != BLOCKCHAR and (c == 0 or board[INDEXES[(r, c-1)]] == BLOCKCHAR):
            temp = i
            temp_c = 0
            wordIndexes = []
            while temp < len(board) and ROWS_COLS[temp][1] >= temp_c and board[temp] != BLOCKCHAR:
                wordIndexes.append(temp)
                temp_c = ROWS_COLS[temp][1]
                temp += 1
            HORIZONTAL_WORDS.add(tuple(wordIndexes))
        # Find location of all vertical words
        if v != BLOCKCHAR and (r==0 or board[INDEXES[(r-1, c)]] == BLOCKCHAR):
            temp = i
            temp_r = 0
            wordIndexes = []
            while temp < len(board) and ROWS_COLS[temp][0] >= temp_r and board[temp] != BLOCKCHAR:
                wordIndexes.append(temp)
                temp_r = ROWS_COLS[temp][0]
                temp += WIDTH
            VERTICAL_WORDS.add(tuple(wordIndexes))
    ALL_WORDS = VERTICAL_WORDS | HORIZONTAL_WORDS
    for cs in VERTICAL_WORDS:
        for idx in cs:
            IDX_VERTICAL[idx] = cs
    for cs in HORIZONTAL_WORDS:
        for idx in cs:
            IDX_HORIZONTAL[idx] = cs

def isValid2(board): #Speed this up
    global CS_POSSIBLE_WORDS
    repeatWords = set()
    best_possible = WORD_DICT
    best_cs = ()
    for cs in ALL_WORDS:
        word = "".join([board[idx] for idx in cs])
        if word.count(OPENCHAR) == 0:
            if word not in WORD_DICT:
                return (False, 0)
            if word not in repeatWords:
                repeatWords.add(word)
                continue
            else:
                return (False, 0)
        if word not in CS_POSSIBLE_WORDS:
            if word.count(OPENCHAR) == len(word):
                possible_words = LENGTH_TO_WORD[len(cs)]
            else:
                regex = "^"
                for i,v in enumerate(cs):
                    if board[v] == OPENCHAR:
                        regex += "[a-z]"
                    else:
                        regex += board[v]
                regex += "$"
                to_search = "\n".join(LENGTH_TO_WORD[len(cs)])
                possible_words = re.findall(regex, to_search, re.IGNORECASE | re.MULTILINE)
                if len(possible_words) == 0:
                    return (False, 0)
                CS_POSSIBLE_WORDS[word] = possible_words
        else:
            possible_words = CS_POSSIBLE_WORDS[word]
        if len(possible_words) < len(best_possible):
            best_possible = possible_words
            best_cs = cs
    return (True, best_possible, best_cs)

def getNeighbors2(board, best_possible, best_cs, usedWords):
    global CS_POSSIBLE_WORDS
    neighbors = []
    # Fill the "best" constraint set first. So choose the constraint set with the least number of possibilities
    # For each word that can fit in the constraint set, fill it.
    # If at any point, there is a constraint set that can't be filled, the board is invalid. Dont add to list of boards
    # return the list of boards
    direction = "V"
    if best_cs in HORIZONTAL_WORDS:
        direction = "H"
    for word in best_possible:
        if word not in usedWords:
            newBoard = placeWord(board, word, best_cs[0], direction)
            neighbors.append((newBoard, word))
    return neighbors

def bruteForce2(board, usedWords):
    global CROSSWORD
    valid = isValid2(board)
    if not valid[0]:
        return ""
    if board.count(OPENCHAR) == 0:
        return board
    bestPossible = valid[1]
    bestCs = valid[2]
    neighbors = getNeighbors2(board, bestPossible, bestCs, usedWords)
    for choice in neighbors:
        subBoard = choice[0]
        word = choice[1]
        newWords = usedWords | {word}
        bF = bruteForce2(subBoard, newWords)
        if bF:
            return bF
    return ""
def unfilledRow(board, idx):
    a = 0
    while idx < len(board) and ROWS_COLS[idx][1] >= a:
        a = ROWS_COLS[idx][1]
        if board[idx] == OPENCHAR:
            return True
        idx += 1
    return False
def getNeighbors3(board, usedWords):
    boardList = []
    idx = 0
    if board[0] != OPENCHAR:
        for i in range(len(board)):
            r,c = ROWS_COLS[i]
            if (c == 0 or board[INDEXES[r,c-1]] == BLOCKCHAR) and (board[i] == OPENCHAR or (WIDTH < 7 and board[i] != BLOCKCHAR and unfilledRow(board, i))):
                idx = i
                break
    temp = idx
    word_length = 0
    a = 0
    while temp < len(board) and ROWS_COLS[temp][1] >= a and board[temp] != BLOCKCHAR:
        a = ROWS_COLS[temp][1]
        word_length += 1
        temp += 1
    for word in WORD_DICT:
        if len(word) == word_length and word not in usedWords:
            new_b = placeWord(board, word, idx, "H")
            if new_b:
                boardList.append((new_b, word))
    return boardList

# Use constraint sets. Each constraint set should correspond to where a word can go
# Fill out constraint sets with the most letters first
# Possibly have a dictionary mapping a constraint set to possible words
# Select constraint sets that have the least possible words
# Put in words that match the length of the constraint set
def bruteForceWords(board, usedWords):
    if board.count(OPENCHAR) == 0:
        return board
    # if inValid2(board):
    #     return ""
    neighbors = getNeighbors3(board, usedWords)
    for choice in neighbors:
        sub_board = choice[0]
        word = choice[1]
        newWords = usedWords | {word}
        bF = bruteForceWords(sub_board, newWords)
        if bF:
            return bF
    return ""
#########################################
def main():
    global CROSSWORD
    test = ["dct20k.txt", "15x15", "37", "V12x7", "v5x2#", "H2x13E", "V13x6T"]
    setGlobals(test)
    CROSSWORD = placeSeeds(CROSSWORD, SEEDS)
    if NUMBLOCKS % 2 == 1:
        mid_row = HEIGHT//2
        mid_col = WIDTH//2
        new_board = list(CROSSWORD)
        new_board[INDEXES[(mid_row, mid_col)]] = BLOCKCHAR
        CROSSWORD = "".join(new_board)
    CROSSWORD = makeSymmetric(CROSSWORD)
    CROSSWORD = autofill(CROSSWORD)
    if not isValid(CROSSWORD):
        CROSSWORD = autofill(CROSSWORD)
    if NUMBLOCKS == len(CROSSWORD):
        sol = BLOCKCHAR * len(CROSSWORD)
    else:
        sol = bruteForce(CROSSWORD)
    CROSSWORD = sol
    print2d(sol)
    getWordConstraints(sol)
    solutionTemp = bruteForceWords(sol, set())
    CROSSWORD = solutionTemp
    print2d(solutionTemp)
    solution2 = bruteForce2(sol, set())
    print()
    print2d(solution2)
#########################################
if __name__ == "__main__": main()