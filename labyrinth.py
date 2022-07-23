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

def searchTarget(target, map):
    action = "LEFT" if target == "T" else "RIGHT"
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
    print(searchTarget(target, map))
