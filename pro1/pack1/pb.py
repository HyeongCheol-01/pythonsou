import sys
import math
a, b, c = map(int,sys.stdin.readline().split())

d = (c-b)/(a-b)


print(math.ceil(d))