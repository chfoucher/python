import sys
import math

def getMap(r):
    map = []
    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        map.append(row)
    #logMap(map)
    return map

def log(message):
    print(message, file=sys.stderr, flush=True)

def logMap(map):
    for row in map:
        log(row)

directions = ["UP", "DOWN", "LEFT", "RIGHT"]
moves = {
    "UP": [0, -1],
    "DOWN": [0, 1],
    "LEFT": [-1, 0],
    "RIGHT": [1, 0],
}

def computeCostMap(target, map, kr, kc):
    costMap = {}
    #log("{0}{1}{2}".format(map[kr-1][kc-1],map[kr-1][kc],map[kr-1][kc+1]))
    for dir in directions:
        log(moves[dir])
        destination = map[kr + moves[dir][1]][kc + moves[dir][0]]
        log("dir: {0}, type {1}".format(dir, destination))
        if destination == target:
            costMap[dir] = 0
        elif destination == "?":
            costMap[dir] = 1
        elif destination == ".":
            costMap[dir] = 2
        else:
            costMap[dir] = 10
    return costMap

def searchTarget(target, map, kr, kc):
    log("kr = {0}, kc = {1}".format(kr, kc))
    action = directions[0]
    costMap = computeCostMap(target, map, kr, kc)
    log(costMap)
    minCost = costMap[action]
    for dir in directions[1:]:
        if minCost > costMap[dir]:
            minCost = costMap[dir]
            action = dir
    return action
    
# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
log("r = {0}, c = {1}".format(r, c))
target = "C"

# game loop
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    kr, kc = [int(i) for i in input().split()]
    map = getMap(r)
    if map[kr][kc] == "C":
        target = "T"
        log("Command center reached!")

    # Rick's next move (UP DOWN LEFT or RIGHT).
    print(searchTarget(target, map, kr, kc))
