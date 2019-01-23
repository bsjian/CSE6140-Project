import random
import math
import time
from itertools import combinations
from util import *
import sys

class Tabu:
    def __init__(self, distance, seed = 0, limited_time = 600):
        # distance input: node_id, x, y
        self.distance = distance
        self.N = len(self.distance)
        self.best_tour = None 
        self.best_cost = float("inf") 
        self.seed = seed
        self.limited_time = limited_time 
        self.nodes = [i for i in range(self.N)]
        self.cost_history = []

    def set_seed(self, seed):
        self.seed = seed

    def tabu(self, curr_tour = None, stopping_criteria = 30):
        '''
        Keep tabu list: keep track of recent searches and include 
        them into tabu list in order for the algorithm to 'explore'
        different possibilities.

        Steps:
            1. choose a random initial state
            2. enters in a loop checking if a condition to break given
            by the user is met(lower bound)
            3. creates an empty candidate list. Each of the candidates 
            in a given neighbor which does not contain a tabu element
            are added to this empty candidate list
            4. It finds the best candidate on this list and if it's cost 
            is better than the current best it's marked as a solution.
            5. If the number of tabus on the tabu list have reached the 
            maximum number of tabus ( you are defining the number ) a tabu
            expires. The tabus on the list expires in the order they have 
            been entered .. first in first out.
        '''
        N = len(self.distance)
        tabu_list = []
        tabu_list_limit = N*50

        # initialization
        sol_cost = get_total_dist(self, curr_tour)
        neighbor_swap = list(combinations(list(range(N)), 2))

        stop_criterion = 0
        changed = 0
        while time.time() - self.start_time < self.limited_time:
            best_tour, best_cost = [], float("inf")
            # get best solution in the neighbor
            random.shuffle(neighbor_swap)
            for neighbor in neighbor_swap[ : len(neighbor_swap) // 3]:
                i, j = neighbor
                # define a neighbor tour
                new_tour = curr_tour.copy()
                new_tour[i: (i + j)] = reversed(new_tour[i: (i + j)])

                new_cost = get_total_dist(self, new_tour)
                if new_cost <= best_cost and new_tour not in tabu_list:
                    best_tour = new_tour
                    best_cost = new_cost
            
            # stopping criterion:
            if stop_criterion > stopping_criteria and changed <= 10:
                changed += 1
                curr_tour, _ = greedy(self)
            
            if stop_criterion > stopping_criteria and changed > 10:
                break 


            if len(tabu_list) == tabu_list_limit:
                tabu_list.pop()
            
            if not best_tour:
                best_tour = new_tour # accpet some worse solution to escape the local maximum
                stop_criterion += 1
            
            tabu_list.append(best_tour)

            if best_cost < sol_cost:
                curr_tour = best_tour.copy()
                sol_cost = best_cost
                
        if self.best_cost > sol_cost:
            self.best_cost = sol_cost
            self.best_tour = curr_tour
            self.cost_history.append((round(time.time() - self.start_time, 2), self.best_cost))

    def batch_tabu(self, times = 100, stopping_criteria = 10):
        self.start_time = time.time()
        for i in range(1, times + 1):
            if time.time() - self.start_time < self.limited_time:
                print(f"Iteration {i}/{times} -------------------------------")
                greedy_tour, _ = greedy(self)
                self.tabu(curr_tour = greedy_tour, stopping_criteria = stopping_criteria)
                print("Best cost obtained: ", self.best_cost)
                print("Best tour", self.best_tour)
                

    # def vis_tour(self, tour):
    #     N = len(self.distance)
    #     fig, ax = plt.subplots(1, 1)
    #     ax.plot([self.distance[tour[i % N]][1] for i in range(N+1)], [self.distance[tour[i % N]][2] for i in range(N+1)], 'xb-')
    #     fig.savefig("../img/curr_tour.png")

    # def vis_cost(self, cost):
    #     fig, ax = plt.subplots(1, 1, figsize = (15, 9))
    #     ax.plot(cost, "*")
    #     ax.tick_params(axis='both', labelsize=20)
    #     ax.set_xlabel("Iteration steps", fontsize = 20)
    #     ax.set_ylabel("Cost", fontsize = 20)
    #     fig.savefig("../img/hist_cost2.png")


if __name__ == "__main__":

    input_file = sys.argv[1]
    distance = read(input_file)
    tabu = Tabu(distance)

    for seed_i in range(20, 30, 1):
        tabu.set_seed(seed_i)
        print("Seed", seed_i)
        tabu.batch_tabu(times = 200)
        print("Best solution", tabu.best_cost)



