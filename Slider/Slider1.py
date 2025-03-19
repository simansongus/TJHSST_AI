import sys; args = sys.argv[1:]
import math
import time

pzl = args[0]
solution = ""
if len(args) < 2: solution = "12345678_"
else: solution = args[1]

width = int(math.sqrt((len(pzl))))
height = int(len(pzl)/width)
startTime = time.time()

def BFS(start, goal): 
    if not inversion:
        return printer("", -1)
    if start == goal: return printer(start,0)
    parseMe = [(start, 0)]
    dctSeen = {start: None}
    steps = 0
    neighborsOG = nbrs_array(start)
    while parseMe:
        node, steps = parseMe.pop(0)
        empty_index = node.find("_")
        neighbors = neighborsOG[empty_index]
        for neighbor_index in neighbors:
            neighbor = list(node)
            neighbor[empty_index], neighbor[neighbor_index] = neighbor[neighbor_index], neighbor[empty_index]
            neighbor = "".join(neighbor)
            if neighbor == goal:
                dctSeen[neighbor] = node
                return printer(dctSeen, steps + 1)
            if neighbor not in dctSeen:
                dctSeen[neighbor] = node
                parseMe.append((neighbor, steps + 1))

    return printer("", -1)

def printer(puzzledict,steps):
    if steps > 0:
        if steps < 12:
            steps_list = reconstruct_path(puzzledict) 
            for i in range(height):
                row = ""
                for step in steps_list[:-1]:
                    row += step[i * width:(i + 1) * width] + "  "
                print(row)
        else:
            if(steps < 22):
                steps_list = reconstruct_path(puzzledict) 
                for i in range(height):
                    row = ""
                    for step in steps_list[:11]:
                        row += step[i * width:(i + 1) * width] + "  "
                    print(row)
                print("")
                for i in range(height):
                    row = ""
                    for step in steps_list[11:-1]:
                        row += step[i * width:(i + 1) * width] + "  "
                    print(row)
            else:
                steps_list = reconstruct_path(puzzledict) 
                for i in range(height):
                    row = ""
                    for step in steps_list[:11]:
                        row += step[i * width:(i + 1) * width] + "  "
                    print(row)
                print("")
                for i in range(height):
                    row = ""
                    for step in steps_list[11:22]:
                        row += step[i * width:(i + 1) * width] + "  "
                    print(row)
                print("")
                for i in range(height):
                    row = ""
                    for step in steps_list[22:-1]:
                        row += step[i * width:(i + 1) * width] + "  "
                    print(row)
    else:
        for i in range(height):
            print(pzl[i * width:(i + 1) * width] + "  ")
    print("Steps:" + str(steps))
    print("Time:" + str(time.time()-startTime)[:4]+"s")

def inversion():
    inversions = len([item for sublist in[[k for k in pzl[pzl.find(n) + 1:]if k != '_' and n > k] for n in pzl if n != '_']for item in sublist])
    if width % 2 == 0:
        rowDifference = (pzl.find('_') // width - solution.find('_') // width)
        return rowDifference % 2 == inversions % 2
    return inversions % 2 == 0

def reconstruct_path(puzzledict):
    path = []
    path.append(solution)
    current_state = list(puzzledict.keys())[-1]
    while current_state is not None:
        path.append(current_state)
        current_state = puzzledict[current_state]
    path = path[::-1]
    return path

def nbrs_array(pzlr):
    nbrarray = []
    for x in range(len(pzlr)):
        nbrarray.append([])
        if x == 0:
            nbrarray[x] = [1, width]
        elif x == len(pzlr)-1:
            nbrarray[x] = [x-1, x-width]
        elif x == width-1:
            nbrarray[x] = [x-1, x+width]
        elif x == len(pzlr)-width:
            nbrarray[x] = [x-width, x+1]
        elif 0<x<width-1:
            nbrarray[x] = [x-1, x+1, x+width]
        elif len(pzlr)-width<x<len(pzlr)-1:
            nbrarray[x] = [x-1, x+1, x-width]
        elif (x+1) % width == 0:
            nbrarray[x] = [x-1, x+width, x-width]
        elif x%width == 0:
            nbrarray[x] = [x+1, x+width, x-width]
        else:
            nbrarray[x] = [x+1, x-1, x-width, x+width]
    return nbrarray


result = BFS(pzl, solution)
if result is not None:
    print(result)

#Gus Simanson, period 2, 2025

