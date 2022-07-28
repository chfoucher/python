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

def getTargetPosition(status, map, target):
    for row in range(status['nbRows']):
        for column in range(status['nbColumns']):
            if map[row][column] == target: return { 'row': row, 'column': column }
    return { 'row': 0, 'column': 0 }

def getTeleport(status, map):
    return getTargetPosition(status, map, "T")

def getControl(map):
    return getTargetPosition(status, map, "C")

def getNeighbours(status, map, row, column):
    result = []
    if row != 0: result.append({ 'row': row - 1, 'column': column })
    if row != status['nbRows'] - 1: result.append({ 'row': row + 1, 'column': column })
    if column != 0: result.append({ 'row': row, 'column': column - 1 })
    if column != status['nbColumns'] - 1: result.append({ 'row': row, 'column': column + 1 })
    return result

def getReachableUnknown(status, map):
    distances = []
    for row in range(status['nbRows']):
        distances.append([-1] * status['nbColumns'])
    stack = []
    distances[status['kr']][status['kc']] = 0
    stack.append({ 'row': status['kr'], 'column': status['kc'] })
    while len(stack) > 0:
        cell = stack.pop(0)
        d = distances[cell['row']][cell['column']]
        for neighbour in getNeighbours(status, map, cell['row'], cell['column']):
            if map[neighbour['row']][neighbour['column']] == "?":
                return neighbour
            elif map[neighbour['row']][neighbour['column']] != "#":
                if distances[neighbour['row']][neighbour['column']] == -1:
                    distances[neighbour['row']][neighbour['column']] = d + 1
                    stack.append(neighbour)
    return { 'row': -1, 'column': -1 }

def computeDistances(status, map, target):
    distances = []
    for row in range(status['nbRows']):
        distances.append([-1] * status['nbColumns'])
    stack = []
    distances[target['row']][target['column']] = 0
    stack.append(target)
    while len(stack) > 0:
        cell = stack.pop(0)
        d = distances[cell['row']][cell['column']]
        log(cell)
        for neighbour in getNeighbours(status, map, cell['row'], cell['column']):
            log(neighbour)
            if map[neighbour['row']][neighbour['column']] != "#":
                if distances[neighbour['row']][neighbour['column']] == -1:
                    distances[neighbour['row']][neighbour['column']] = d + 1
                    stack.append(neighbour)
    return distances

def positionsToAction(current, target):
    if current['row'] == target['row']:
        if current['column'] > target['column']:
            return "LEFT"
        else:
            return "RIGHT"
    else:
        if current['row'] > target['row']:
            return "UP"
        else:
            return "DOWN"

def selectClosestNeighbour(status, map, distances):
    distance = -1
    closest = { 'row': -1, 'column': -1}
    for neighbour in getNeighbours(status, map, status['kr'], status['kc']):
        if (distance == -1) or (distance > distances[neighbour['row']][neighbour['column']]):
            distance = distances[neighbour['row']][neighbour['column']]
            closest = { 'row': neighbour['row'], 'column': neighbour['column']}
    return closest

def getAction(status, map):
    if (status['controlReached']):
        target = getTeleport(map)
    elif (status['controlReachable']):
        target = getControl(map)
    else:
        target = getReachableUnknown(status, map)
    distances = computeDistances(status, map, target)
    newPosition = selectClosestNeighbour(status, map, distances)
    return positionsToAction({ 'row': status['kr'], 'column': status['kc'] }, newPosition)
    
# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
log("r = {0}, c = {1}".format(r, c))
status = { 'nbRows': r, 'nbColumns': c, 'controlReached': False, 'controlReachable': False, 'timeLeft': a }

# game loop
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    status['kr'], status['kc'] = [int(i) for i in input().split()]
    map = getMap(status['nbRows'])
    if map[status['kr']][status['kc']] == "C":
        status['controlReached'] = True
        log("Command center reached!")

    # Rick's next move (UP DOWN LEFT or RIGHT).
    print(getAction(status, map))
