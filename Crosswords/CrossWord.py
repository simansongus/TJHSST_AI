import sys; args = sys.argv[1:]

def setGlobals(args):   
    global height; height = int(args[0][:args[0].index("x")])
    global width; width = int(args[0][args[0].index("x")+1:])
    numBlocks = int(args[1])
    placeList = []
    for arg in args[2:]:
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
    #print2d(pzl)
    if invalidResponse[0]:
        return ""
    pzl, numBlocks = invalidResponse[1], invalidResponse[2]

    if numBlocks == 0:
        if isContinuous(pzl):
            return pzl
        return ""

    for idx in posMovesCached(pzl):
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
    
    if len(tooSmall) == 0:
        return False, puzzle, numBlocks
    elif len(tooSmall) > numBlocks:
        return True, puzzle, numBlocks
    else:
        for x in tooSmall:
            if x in posMovesCached(puzzle):
                puzzle, numBlocks = placeBlockCached(puzzle, x, numBlocks)
                if numBlocks < 0:
                    return True, puzzle, numBlocks
            else:
                return True, puzzle, numBlocks
        return isInvalidCached(puzzle, numBlocks, None)

POSCACHE = {}
def posMovesCached(pzl):
    key = (pzl)
    if key in POSCACHE:
        return POSCACHE[key]
    else:
        temp = posMoves(pzl)
        POSCACHE[key] = temp
        return temp
    
def posMoves(pzl):
    pos = []
    for idx, val in enumerate(pzl[:len(pzl)//2 + 2]):
        if val == "-" and pzl[(len(pzl)-1-idx)] == "-":
            pos.append(idx)
    return pos


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
            nx = r + dx
            ny = c + dy
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
        temp = "".join(temp)
    else:
        temp = [*puzzle]
        if temp[index] != "#":
            temp[index] = "#"
            numBlocks -= 1
        if temp[len(puzzle)-1-index] != "#":
            temp[len(puzzle)-1-index] = "#"
            numBlocks -= 1
        temp = "".join(temp)
    return temp, numBlocks

def placeWord(puzzle, location, word, direction, numBlocks):
    temp = [*puzzle]
    if direction.lower() == "v":
        for idx, val  in enumerate(word):
            if val == "#":
                temp = "".join(temp)
                temp, numBlocks = placeBlockCached(temp, location + (width*idx), numBlocks)
                temp = [*temp]
            else: temp[location + (width*idx)] = val

    if direction.lower() == "h":
        for idx, val in enumerate(word):
            if val == "#":
                temp = "".join(temp)
                temp, numBlocks = placeBlockCached(temp, location + idx, numBlocks)
                temp = [*temp]
            temp[location + idx] = val

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


    puzzle, numBlocks = isInvalidCached(puzzle, numBlocks, None)[1:]
    puzzle, numBlocks = fillDiscontinuousAreasCached(puzzle, numBlocks)

    if numBlocks == 0:
        print2d(puzzle)
        exit()

    print2d(puzzle)
    print(numBlocks)
    
    puzzle = bruteForce(puzzle, numBlocks, None)
    if puzzle:
        print2d(puzzle)
    else:
        print("no solution")

if __name__ == "__main__": main()

#Gus Simanson, period 2, 2025