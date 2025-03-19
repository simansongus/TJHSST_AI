import sys; args = sys.argv[1:]

def setGlobals(args):
    global wordList; wordList = open(args[0]).read().splitlines()
    global dictWord; dictWord = {}
    global dictWordLength; dictWordLength = {}

    for word in wordList:
        if len(word) < 3:
            continue
        dictWord[word] = {word}

        for i in range(1, 2 ** len(word)):
            key = ''.join([word[j] if i & (1 << j) else '_' for j in range(len(word))])
            if key in dictWord:
                dictWord[key].add(word)
            else:
                dictWord[key] = {word}

        if len(word) not in dictWordLength: 
            dictWordLength[len(word)] = {word}
        else: 
            dictWordLength[len(word)].add(word)

    global height; height = int(args[1][:args[1].index("x")])
    global width; width = int(args[1][args[1].index("x")+1:])
    numBlocks = int(args[2])
    placeList = []
    for arg in args[3:]:
        direction = arg[0]

        location = arg[1:6]
        if not location[-1].isdigit():
            location = location[:-1]
        if not location[-1].isdigit():
            location = location[:-1]
        location = (int(location[:location.index("x")])*width) + int(location[location.index("x")+1:]) #location is (x,y) going from top left is 0,0

        word = arg[4:]
        if any(not c.isdigit() for c in word):
            if word[0].isdigit():
                word = word[1:]
            if word[0].isdigit():
                word = word[1:]
        else: word = "#"
        placeList.append((direction, location, word)) #Direction (vertical/horizontal), Where its placed (x,y), word
    return numBlocks, placeList

def bruteForce(pzl,numBlocks, lastIdx):
    invalidResponse = isInvalidCached(pzl, numBlocks, lastIdx)
    if invalidResponse[0]:
        return ""
    else: pzl, numBlocks = invalidResponse[1], invalidResponse[2]
    if numBlocks == 0:
        if isContinuous(pzl):
            return pzl
        return ""
    
    pos = posMovesCached(pzl)
    
    for idx in pos:
        subPzl, subNumBlocks = placeBlockCached(pzl, idx, numBlocks)  # Get the updated puzzle and block count
        bF = bruteForce(subPzl, subNumBlocks, idx)  # Pass the updated state
        if bF:
            return bF
    return ""

VALIDCACHE = {}
def isInvalidCached(puzzle, numBlocks, lastIdx):
    key = (puzzle, numBlocks, lastIdx)
    if key in VALIDCACHE:
        return VALIDCACHE[key]
    else:
        temp = isInvalid(puzzle, numBlocks, lastIdx)
        VALIDCACHE[key] = temp
        return temp
    
def isInvalid(puzzle, numBlocks, lastIdx): 
    tooSmall = findTooSmall(puzzle, lastIdx)

    if not isContinuous(puzzle):
        return True, puzzle, numBlocks
    
    if len(tooSmall) == 0:
        return False, puzzle, numBlocks
    elif len(tooSmall) > numBlocks:
        return True, puzzle, numBlocks
    else:
        for x in tooSmall:
            if x not in basicposMovesCached(puzzle):
                return True, puzzle, numBlocks
            puzzle, numBlocks = placeBlockCached(puzzle, x, numBlocks)
            if numBlocks < 0:
                return True, puzzle, numBlocks
        return isInvalidCached(puzzle, numBlocks, None)

BASICPOSCACHE = {}
def basicposMovesCached(pzl):
    key = (pzl)
    if key in BASICPOSCACHE:
        return BASICPOSCACHE[key]
    else:
        temp = basicposMoves(pzl)
        BASICPOSCACHE[key] = temp
        return temp
    
def basicposMoves(pzl):
    pos = []
    for idx, val in enumerate(pzl):
        if val == "-" and pzl[(len(pzl)-1-idx)] in "-#":
            row, col = divmod(idx, width)
            dedge = min(row, height - row - 1, col, width - col - 1)
            score = dedge
            pos.append((idx, score))
    pos.sort()
    return [idx for idx, _ in pos]

POSCACHE = {}
def posMovesCached(pzl):
    key = (pzl)
    if key in POSCACHE:
        return POSCACHE[key]
    else:
        temp = posMoves(pzl)
        POSCACHE[key] = temp
        return temp

def posMoves(puzzle):
    pos = []
    corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
    for idx, val in enumerate(puzzle[:len(puzzle)//2+2]):
        if val == "-" and puzzle[len(puzzle)-1-idx] == "-":
            row, col = divmod(idx, width)
            nextTo = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1), (row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]
            count = 0
            for r, c in nextTo:
                if 0 <= r < height and 0 <= c < width and puzzle[r * width + c] == '#':
                    count += 10
            
            dcorner = min([abs(row - cr) + abs(col - cc) for cr, cc in corners])
            dcenter = abs(row - height//2) + abs(col - width//2)
            dedge = min(row, height - row - 1, col, width - col - 1)
            score = (count*100) - dcenter - dcorner - dedge

            pos.append((score, idx))
    pos.sort()
    return [idx for _, idx in pos]


def isContinuous(puzzle):
    grid = [list(puzzle[i*width:(i+1)*width]) for i in range(height)] #2d list
    start = None
    for i in range(height):
        for j in range(width):
            if grid[i][j] != '#': 
                start = (i, j)
                break
    if not start:
        return True
    
    visited = set()
    queue = [start]
    ptr = 0
    while ptr < len(queue):
        x, y = queue[ptr]
        ptr += 1
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right down left up
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] != '#' and (nx, ny) not in visited:
                queue.append((nx, ny))
    
    if (len(puzzle) - puzzle.count("#")) != len(visited):
        return False
    return True

def findTooSmall(pzl, lastIdx):
    badList = []
    temp = [list(pzl[i*width:(i+1)*width]) for i in range(height)]

    def checkSquare(r, c): #checks if square is in a too small group
        if temp[r][c]== '#':
            return
        h = 1
        for x in [-1, 1]:
            newC = c + x
            while 0 <= newC < width and temp[r][newC] != '#':
                h += 1
                newC += x if x == 1 else -1
        v = 1
        for y in [-1, 1]:
            newR = r + y
            while 0 <= newR < height and temp[newR][c] != '#':
                v += 1
                newR += y if y == 1 else -1
        if h < 3 or v < 3:
            badList.append(r * width + c)

    if lastIdx is not None:
        r = lastIdx // width
        c = lastIdx % width
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 2), (2, 0), (0, -2), (-2, 0), (0, 3), (3, 0), (0, -3), (-3, 0)]:
            nx, ny = r + dx, c + dy
            if 0 <= nx < height and 0 <= ny < width:
                checkSquare(nx, ny)
    else:
        for r in range(height):
            for c in range(width):
                checkSquare(r, c)
    return badList

PBCACHE = {}
def placeBlockCached(puzzle, index, numBlocks):
    key = (puzzle, index, numBlocks)
    if key in PBCACHE:
        return PBCACHE[key]
    else:
        temp = placeBlock(puzzle, index, numBlocks)
        PBCACHE[key] = temp
        return temp
    
def placeBlock(puzzle, index, numBlocks): #location being placed is row*column **implement three block thing
    if index == len(puzzle)//2:
        temp = [*puzzle]
        if temp[index] != "#":
            temp[index] = "#"
            numBlocks = numBlocks - 1
        puzzle = "".join(temp)
    else:
        temp = [*puzzle]
        if temp[index] != "#":
            temp[index] = "#"
            numBlocks -= 1
        if temp[len(puzzle)-1-index] != "#":
            temp[len(puzzle)-1-index] = "#"
            numBlocks -= 1
        puzzle = "".join(temp)
    return puzzle, numBlocks

def placeWord(puzzle, location, word, direction, numBlocks):
    temp = [*puzzle]
    if direction.lower() == "v":
        for idx, val in enumerate(word):
            if val == "#":
                temp = "".join(temp)
                temp, numBlocks = placeBlockCached(temp, location + (width*idx), numBlocks)
                temp = [*temp]
            elif temp[location + (width*idx)].lower()  == val.lower(): 
                continue
            elif temp[location + (width*idx)].lower() == "-": 
                temp[location + (width*idx)] = val
            else: return puzzle, numBlocks

    if direction.lower() == "h":
        for idx, val in enumerate(word):
            if val == "#":
                temp = "".join(temp)
                temp, numBlocks = placeBlockCached(temp, location + idx, numBlocks)
                temp = [*temp]
            elif temp[location + idx].lower() == val.lower():
                continue
            elif temp[location + idx].lower()  == "-":
                temp[location + idx] = val
            else: return puzzle, numBlocks

    return ''.join(temp), numBlocks

FILLCACHE = {}
def fillDiscontinuousAreasCached(puzzle, numBlocks):
    key = (puzzle, numBlocks)
    if key in FILLCACHE:
        return FILLCACHE[key]
    else:
        temp = fillDiscontinuousAreas(puzzle, numBlocks)
        FILLCACHE[key] = temp
        return temp
    
def fillDiscontinuousAreas(puzzle, numBlocks):
    visited = set()
    areas = []  # List to hold tuples of (area size, start coordinate)

    def floodFill(x, y):
        if x < 0 or x >= height or y < 0 or y >= width or (x, y) in visited or puzzle[x * width + y] == '#':
            return 0
        visited.add((x, y))
        area = 1
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            area += floodFill(x + dx, y + dy)
        return area

    # Identify all continuous empty areas and their sizes
    for i in range(height):
        for j in range(width):
            if (i, j) not in visited and puzzle[i * width + j] == '-':
                areaSize = floodFill(i, j)
                if areaSize <= numBlocks:
                    areas.append((areaSize, (i, j)))

    # Sort areas by size (smallest to largest)

    # Attempt to fill smaller areas first, if numBlocks is sufficient
    for areaSize, (start_x, start_y) in areas:
        if numBlocks >= areaSize:
            stack = [(start_x, start_y)]
            while stack:
                x, y = stack.pop()
                if 0 <= x < height and 0 <= y < width and puzzle[x * width + y] == '-':
                    puzzle = puzzle[:x * width + y] + '#' + puzzle[x * width + y + 1:]
                    numBlocks -= 1
                    stack.extend([(x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]])
        else:
            break

    return puzzle, numBlocks

def findStarts(puzzle):
    global startList; startList = []
    global vstartList; vstartList = []
    global hstartList; hstartList = []
    temp = [list(puzzle[i*width:(i+1)*width]) for i in range(height)]
    starts = []

    for r in range(height):
        for c in range(width):
            if temp[r][c] != "#":
                if (c ==0 or temp[r][c-1] == "#"):
                    h= 1
                    newC = c + 1
                    while newC < width and temp[r][newC] != '#':
                        h += 1
                        newC += 1
                    startList.append(((r * width + c), h, "h"))
                    hstartList.append(((r * width + c), h, "h"))

                if (r == 0 or temp[r-1][c] == "#"):     
                    v = 1
                    newR = r + 1
                    while newR < height and temp[newR][c] != '#':
                        v += 1
                        newR += 1
                    startList.append(((r * width + c), v, "v"))
                    vstartList.append(((r * width + c), v, "v"))

def findStartCs():
    global startToIdxsDictionary; startToIdxsDictionary = {}
    global idxToStartDictionary; idxToStartDictionary = {}
    for start in startList:
        idxList = []
        if start[2] == "v":
            for x in range(start[1]):
                idx = start[0] + (x*width)
                idxList.append(idx)
                if idx in idxToStartDictionary:
                    idxToStartDictionary[idx].append(start)
                else: idxToStartDictionary[idx] = [start]
        if start[2] == "h":
            for x in range(start[1]):
                idx = start[0] + x
                idxList.append(idx)
                if idx in idxToStartDictionary:
                    idxToStartDictionary[idx].append(start)
                else: idxToStartDictionary[idx] = [start]
        startToIdxsDictionary[start] = idxList

def findContainedStarts():
    global startToStartsDictionary; startToStartsDictionary = {}

    for start in startList:
        containedStarts = []
        for idx in startToIdxsDictionary[start]:
            for otherStart in idxToStartDictionary[idx]:
                if otherStart[2] != start[2]:
                    if otherStart not in containedStarts:
                        containedStarts.append(otherStart)
        startToStartsDictionary[start] = containedStarts

def simpleSolve(puzzle, numBlocks):
    placedWords = set()
    tempstarts = [*hstartList] #+ [vstartList[0]]
    for start in tempstarts:
        idxList = startToIdxsDictionary[start]
        section = "".join([puzzle[idx] for idx in idxList])
        contraList = [(idx, val.lower()) for idx, val in enumerate(section) if val != "-"]
        if len(contraList) == 0:
            posWords = [word for word in dictWordLength[start[1]] if word not in placedWords]
        else:
            posWords = dictWord[(start[1], contraList[0][0], contraList[0][1])]
            for x in contraList[1:]:
                posWords = posWords.intersection(dictWord[start[1], x[0], x[1]])
        word = [*posWords][0]
        puzzle = placeWord(puzzle, start[0], word, start[2], numBlocks)[0]
        placedWords.add(word)
    return puzzle

def isPlacedInvalid(pzl, placedWords, startIdx):
    if startIdx == 0:
        return False
    start = startList[startIdx-1]
    containedStarts = startToStartsDictionary[start]
    for st in containedStarts:
        idxList = startToIdxsDictionary[st]
        section = "".join([pzl[idx] for idx in idxList])
        if section not in dictWord:
            return True
    return False

def solvePuzzle(pzl, numBlocks, startIdx, placedWords):
    if isPlacedInvalid(pzl, placedWords, startIdx): 
        return ""

    if "-" not in pzl:
        return pzl
    
    start = startList[startIdx]
    idxList = startToIdxsDictionary[start]
    section = "".join([pzl[idx] for idx in idxList])

    if section in dictWord:
        pWords = dictWord[section]
    else: return ""

    if not pWords:
        return ""
    for word in pWords[1]:
        subPzl = placeWord(pzl, start[0], word, start[2], numBlocks)[0]
        newPlacedWords = placedWords.copy()
        newPlacedWords.add(word)
        bF = solvePuzzle(subPzl, numBlocks, startIdx+1, newPlacedWords)
        if bF: return bF
    return ""


def print2d(puzzle):
    for r in range(height):  
        print("".join([puzzle[i + r * width] for i in range(width)]))

def main():
    numBlocks, placeList = setGlobals(args)
    puzzle = "-" * (height * width)
    for place in placeList:
        if not place[2]:
            continue
        else:
            puzzle, numBlocks = placeWord(puzzle, place[1], place[2], place[0], numBlocks)

    if numBlocks == height * width:
        puzzle = "#" * (height*width)
        print2d(puzzle)
        exit()

    if numBlocks % 2 == 1: #if off amount of blocks, one must be place in middle of cross word puzzle
        puzzle, numBlocks = placeBlockCached(puzzle, len(puzzle)//2, numBlocks)

    """print("Input Structure:")
    print2d(puzzle)
    print()"""
    
    puzzle, numBlocks = isInvalidCached(puzzle, numBlocks, None)[1:]
    puzzle, numBlocks = fillDiscontinuousAreasCached(puzzle, numBlocks)
        
    print("Initial Structure:")
    print2d(puzzle)
    print()
    puzzle = bruteForce(puzzle, numBlocks, None)

    print("Structure:")
    if puzzle:
        print2d(puzzle)
    else:
        print("no solution")
    print()

    findStarts(puzzle)
    findStartCs()
    findContainedStarts()

    print("Simple solution:")
    simp = simpleSolve(puzzle, numBlocks)
    print2d(simp)
    print()
    #print(dictWord)
    #print(dictWordLength)
    #print(startList)
    #print(startToIdxsDictionary)
    #print(idxToStartDictionary)
    #print(startToStartsDictionary)
    global bestSoFar; bestSoFar = (width * height)
    print("Solved:")
    puzzle = solvePuzzle(puzzle, numBlocks, 0, set())
    
    if puzzle:
        print2d(puzzle)
    else:
        print("no solution")

if __name__ == "__main__": main()