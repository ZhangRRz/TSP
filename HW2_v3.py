import csv
from itertools import permutations
from numpy.linalg import norm
import math
import matplotlib.pyplot as plt
import time
import multiprocessing
from collections import defaultdict
import copy
# Find TSP using brute-force
# Getting the data
data = []
toOriginalNum = dict()
numToVector = dict()
pointNametoVec = dict()
distanceMartix = defaultdict(lambda: defaultdict(int))
with open('readfile.txt', 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        n = int(row[0].split(" ")[0])
        x = int(row[0].split(" ")[1])
        y = int(row[0].split(" ")[2])
        toOriginalNum[i] = n  # Converting Index back to city num
        pointNametoVec[n] = (x, y)  # Using city's number to get vector.
        numToVector[i] = (x, y)  # Using index to get city's vector
        # Storing the point as this: [(x1,y1), (x2,y2), ...]
        data.append((x, y))


def eudis(v1, v2):
    dist = [(a - b)**2 for a, b in zip(v1, v2)]
    dist = math.sqrt(sum(dist))
    return dist


n = len(data)

for i in range(n):
    for j in range(n):
        distanceMartix[i][j] = distanceMartix[j][i] = eudis(
            numToVector[i], numToVector[j])

# Answer table of a problem with starting point and a set to be traversaled.
pointAndSetAns = {}

p = []  # Store next step and remaining cities


def TSP(point: int, s: tuple):
    if(point, s) in pointAndSetAns:
        return pointAndSetAns[point, s]  # DP part

    val = []
    c_list = []
    for j in s:
        subProbSet = copy.deepcopy(list(s))
        subProbSet.remove(j)
        # A local list for current point and remaining cities.
        c_list.append([j, tuple(subProbSet)])
        result = TSP(j, tuple(subProbSet))  # Global resualt
        # The answers of current problem
        val.append(distanceMartix[point][j] + result)
    # Finding the min dist among all of answers
    pointAndSetAns[point, s] = min(val)
    # Creating answer table
    p.append(((point, s), c_list[val.index(pointAndSetAns[point, s])]))
    return pointAndSetAns[point, s]


for x in range(1, n):
    # Base case for recursive function call.
    pointAndSetAns[x, ()] = distanceMartix[x][0]

init_set = []
for i in range(1, n):
    init_set.append(i)
init_set = tuple(init_set)

TSP(0, init_set)

solution = p.pop()  # Getting the first answer
for i in p:
    print(i)
# print(solution)
finalList = [0]
finalList.append(solution[1][0])
for x in range(n - 2):  # Skipping point zero and point one.
    for new_solution in p:
        if tuple(solution[1]) == new_solution[0]:
            solution = new_solution
            finalList.append(solution[1][0])
            break
for i, j in enumerate(finalList):
    finalList[i] = toOriginalNum[j]

print(finalList)

for i in finalList:
    print(pointNametoVec[i])
