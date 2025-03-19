import sys; args = sys.argv[1:]
import time; startTime = time.time()
newargs = []
for arg in args:
    if "x" in arg:
        parts = arg.split("x")
        for part in parts:
            newargs.append(int(part))
    elif "X" in arg:
        parts = arg.split("X")
        for part in parts:
            newargs.append(int(part))
    else: newargs.append(int(arg))

container = newargs[0], newargs[1] #h*w
singleBlocks = [("..AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"[x],(newargs[x], newargs[x+1])) for x in range(2, len(newargs), 2)] #h*w
sumblocksize = sum([block[1][0] * block[1][1] for block in singleBlocks])

blocks = sorted(singleBlocks + [("..AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"[x], (newargs[x+1], newargs[x])) for x in range(2, len(newargs), 2)], key=lambda b: b[1][0] * b[1][1], reverse=True) #h*w
holeSize = (container[0] * container[1]) - sumblocksize
baseBoard = "".join(["." for x in range(container[0] * container [1])])

print(str(holeSize))

if (container[0] * container[1]) < sumblocksize:
    print("No solution")
    exit()

if container == blocks[0][1] or container == blocks[1][1]:
    print(f"Decomposition: {container[0]}x{container[1]}")
    exit()

def isInvalid(board, posBlocks, holes):
    emptySpaces = board.count('.')
    for block in posBlocks:
        blockSize = block[1][0] * block[1][1]
        if blockSize <= emptySpaces:
            for idx in range(len(board)):
                if board[idx] == '.' and isPlaceable(board, idx, block):
                    return False
    if holes <= emptySpaces:
        for holeDimension in possibleBlanks(holes):
            for idx in range(len(board)):
                if board[idx] == '.' and isPlaceable(board, idx, ("0", holeDimension)):
                    return False
    return True

def placeBlock(board, idx, block):
    newBoard = list(board)  # Convert board to a list
    for x in range(block[1][0]):
        for y in range(block[1][1]):
            if 0 <= idx + x * container[1] + y < len(board):
                newBoard[idx + x * container[1] + y] = block[0]
            else: return board
    return ''.join(newBoard)

def possibleBlanks(holeSize):
    posBlanks = []
    for height in range(1, holeSize + 1):
        for width in range(1, holeSize + 1):
            if height * width <= holeSize:
                posBlanks.append((height, width))
    posBlanks.sort(reverse = True)
    return posBlanks

def isPlaceable(board, index, block):
    relativeW = index % container[1]
    relativeH = index // container[1]
    # Check if the block fits within the board's width and height
    if relativeW + block[1][1] > container[1] or relativeH + block[1][0] > container[0]:
        return False
    # Check for overlaps with existing blocks
    for x in range(block[1][0]):
        for y in range(block[1][1]):
            if board[index + x * container[1] + y] != ".":
                return False
    return True

def decompose(board, placedBlocks):
    for i in range(0, len(board), container[1]):
        print(board[i:i + container[1]])
    found = set()
    final = ''
    for char in board:
        if char not in found and char != "0":
            found.add(char)
            final += f" {placedBlocks[char][0]}x{placedBlocks[char][1]}"
        elif char == "0":
            final += " 1x1"
    return "Decomposition: " + final[1:]

def bruteForce(board, posBlocks, placedBlocks, holeSize):
    #for i in range(0, len(board), container[1]): #FOR DEBUGGING, VERY DANGEROUS !!!!!!!
        #print(board[i:i + container[1]]) #FOR DEBUGGING, VERY DANGEROUS !!!!!!!
    if "." not in board: return decompose(board, placedBlocks)
    if isInvalid(board, posBlocks, holeSize): return ""
    idx = board.index(".")
    for block in posBlocks:
        if isPlaceable(board, idx, block):
            newBoard = placeBlock(board, idx, block)
            newPlaced = placedBlocks.copy()
            newPlaced[block[0]] = block[1]
            newBlocks = [b for b in posBlocks if b != block and b[1] != (block[1][1], block[1][0])]
            solution = bruteForce(newBoard, newBlocks, newPlaced, holeSize)
            if solution:
                return solution
    for hole in possibleBlanks(holeSize):
        if isPlaceable(board, idx, ("0", hole)):
            newBoard = placeBlock(board, idx, ("0", hole))
            newPlaced = placedBlocks.copy()
            newPlaced["0"] = hole
            newHoleSize = holeSize - (hole[0] * hole[1])
            solution = bruteForce(newBoard, posBlocks, newPlaced, newHoleSize)
            if solution:
                return solution
    return ""

answer = bruteForce(baseBoard, blocks, {}, holeSize)
if answer == "":
    print("No solution")
print(answer)
print(str(time.time()-startTime)[:4] + " seconds")


#Gus Simanson, period 2, 2025