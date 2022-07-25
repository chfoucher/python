import sys
import math

def debug(message):
    print(message, file=sys.stderr, flush=True)

t = input()
parts = t.split()

def buildPart(part):
    result = " "
    return result

answer = ""
for part in parts:
    answer += buildPart(part)

print(answer)
