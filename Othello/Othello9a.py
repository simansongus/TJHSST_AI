import sys; args = sys.argv[1:]
import math

global width;
global height;
BOARDCACHE = set()

width = 0

for arg in args:
    if str.isdigit(arg) and len(arg) < 3:
        width = int(arg)
    else:
        board = arg

if not width:   
    width = int(math.sqrt(len(board)))
height = len(board) // width

def makeStr(brd):
    return "".join(str(c) for row in brd for c in row)

def makeArray(brd, w, h):
    return [list(brd[i*w:(i+1)*w]) for i in range(h)]

BOARDCACHE.add(board)

def rotRight(brd, w, h):
    TwoDVersion = list(zip(*makeArray(brd, w, h)[::-1]))
    final = makeStr(TwoDVersion)
    BOARDCACHE.add(final)
    return final
    

def rotLeft(brd, w, h):
    doubleRot = list(zip(*makeArray(brd, w, h)))[::-1]
    final = makeStr(doubleRot)
    BOARDCACHE.add(final)
    return final

def rotTwice(brd, w, h):
    ninetydeg = rotRight(brd, w, h)
    twice = rotRight(ninetydeg, h, w)
    BOARDCACHE.add(twice)
    return twice


def flipHorizontally(brd, w, h):
    horizFlip = makeArray(brd, w, h)[::-1]
    final = makeStr(horizFlip)
    BOARDCACHE.add(final)
    return final

def flipVertically(brd, w, h):
    vertFlip = [row[::-1] for row in makeArray(brd, w, h)]
    final = makeStr(vertFlip)
    BOARDCACHE.add(final)
    return final

def flipLeftDiag(brd, w, h):
    initial = makeArray(brd, w, h)
    leftDiag = list(zip(*initial))
    final = makeStr(leftDiag)
    BOARDCACHE.add(final)
    return final

def flipRightDiag(brd, w, h):
    initial = [row[::-1] for row in makeArray(brd, w, h)[::-1]]
    rightDiag = list(zip(*initial))
    final = makeStr(rightDiag)
    BOARDCACHE.add(final)
    return final



rotRight(board, width, height)
rotLeft(board, width, height)
rotTwice(board, width, height)
flipHorizontally(board, width, height)
flipVertically(board, width, height)
flipLeftDiag(board, width, height)
flipRightDiag(board, width, height)

for rect in BOARDCACHE:
    print(rect)

#Gus Simanson, Ani Chinthakindi, Period 2, 2025