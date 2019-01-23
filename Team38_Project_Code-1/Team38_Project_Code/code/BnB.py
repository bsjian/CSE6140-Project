import time
import queue as Q
import gc
import random
import math
import sys
import copy
from util import *
class Node:
    def __init__(self, distance, path, level, i, j):
        
        self.path = copy.deepcopy(path)
        self.cost = 0
        self.curCost = 0
        self.level = level
        if level != 0:
            self.path.append(j)
        self.rm = copy.deepcopy(distance)
        self.curloc = j

        for k in range(len(distance)):
            if level == 0:
                break
            else:
                self.rm[i][k] = float("inf")
                self.rm[k][j] = float("inf")
        self.rm[j][0] = float("inf")

    def __lt__(self, other):
        return other.cost < self.cost

    def __ge__(self, other):
        return other.cost > self.cost


class BnB:
    def __init__(self, distance, limited_time = 600, visited= None, prioq= None, best_path= None):
        self.distance = distance
        self.N = len(distance)
        self.start_time = time.time()
        self.limited_time = limited_time
        self.nodes = [i for i in range(self.N)]
        self.best_tour = None
        self.best_cost = float("Inf")
        self.cost_history = []

        self.best_path, self.best_cost = greedy(self)
        self.prioq = None  
        
        print("greedy cost is", self.best_cost)
        self.cost_history.append((round(time.time() - self.start_time, 2), self.best_cost))
        
    
    def solve(self):
    
        length = len(self.distance)
        curr_path = [0]
        curMaxDepth = 0
        root = Node(self.distance, curr_path, 0, 0, 0)
        q = Q.PriorityQueue()
        q.put(root)

        while not q.empty() and time.time() - self.start_time < self.limited_time:
            node_tmp = q.get() 
            i = node_tmp.curloc
            if node_tmp.level > curMaxDepth:
                curMaxDepth = node_tmp.level
                print("current depth is ", curMaxDepth)
            if node_tmp.cost > self.best_cost:
                continue
            if node_tmp.level == length - 1:
                node_tmp.path.append(0)
                if node_tmp.cost < self.best_cost:  
                    self.best_cost = node_tmp.cost
                    self.best_path = node_tmp.path.copy()
                    self.cost_history.append((round(time.time() - self.start_time, 2), self.best_cost))
                    print("current best cost is", self.best_cost)

            for j in range(length):
                if node_tmp.rm[i][j] != float("inf") and node_tmp.level < length - 1:
                    # print("child branching from node", j)
                    child = Node(node_tmp.rm, node_tmp.path, node_tmp.level + 1, i, j)

                    childCost = node_tmp.cost + node_tmp.rm[i][j]
                    if childCost > self.best_cost:
                        continue
                    childCost += self.calculateCost(child.rm)
                    if childCost > self.best_cost:
                        continue
                    child.cost = childCost
                    child.curCost = node_tmp.rm[i][j]
                    q.put(child)
            gc.collect()
        if q.empty():
            print("-------------Went through everything! [Solution guaranteed optimal]-------------")
        else:
            print("-------------[Failed due to time limit]-------------")

    def calculateCost(self, rm):
        if rm == None:
            return 0
        cost = 0
        length = len(rm)
        row = []
        col = []
        self.rowReduction(rm, row)
        self.colReduction(rm, col)

        for i in range(length):
            cost += row[i] if (row[i] != float("inf")) else 0
            cost += col[i] if (col[i] != float("inf")) else 0
        return cost

    def rowReduction(self, rm, row):
        length = len(rm)
        for i in range(length):
            row.append(float("inf"))
        for i in range(length):
            for j in range(length):
                if rm[i][j] < row[i]:
                    row[i] = rm[i][j]
        for i in range(length):
            for j in range(length):
                if rm[i][j] != float("inf") and row[i] != float("inf"):
                    rm[i][j] -= row[i]

    def colReduction(self, rm, col):
        length = len(rm)
        for i in range(length):
            col.append(float("inf"))
        for i in range(length):
            for j in range(length):
                if rm[i][j] < col[j]:
                    col[j] = rm[i][j]
        for i in range(length):
            for j in range(length):
                if rm[i][j] != float("inf") and col[j] != float("inf"):
                    rm[i][j] -= col[j]


if __name__ == "__main__":
    input_file = sys.argv[1]
    distance = read(input_file)
    
    newBnB = BnB(distance)
    newBnB.solve()
    print("best cost", newBnB.best_cost)
    print("best_path", newBnB.best_path)
    print(newBnB.cost_history)