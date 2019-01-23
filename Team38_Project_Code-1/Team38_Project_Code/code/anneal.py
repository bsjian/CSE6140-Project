import time 
import os
import math
import random
from util import *

class Simulated_annealing:
    def __init__(self, distance, limited_time = 600, T=-1,  cooling_rate=-1, stopping_T=-1):
        self.distance = distance
        self.N = len(distance)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.T_save = self.T  
        self.cooling_rate = 0.9995 if cooling_rate == -1 else cooling_rate
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        self.start_time = None
        self.limited_time = limited_time
        self.cur_total_dis = float("inf")
        self.nodes = [i for i in range(self.N)]

        self.best_tour = None
        self.best_cost = float("Inf")
        self.cost_history = []

    def p_accept(self, candidate_cost):
        return math.exp(-abs(candidate_cost - self.cur_total_dis) / self.T)

    def accept(self, tour):
        tour_cost = get_total_dist(self, tour)
        if tour_cost < self.cur_total_dis:
            self.cur_total_dis, self.cur_tour = tour_cost, tour
            if tour_cost < self.best_cost:
                self.best_cost, self.best_tour = tour_cost, tour
        else:
            if random.random() < self.p_accept(tour_cost):
                self.cur_total_dis, self.cur_tour = tour_cost, tour

    def anneal(self):
        print("Starting annealing.")
        while self.T >= self.stopping_temperature:
            next_tour = list(self.cur_tour)
            [i, l] = random.sample(range(self.N), 2)
            next_tour[i : (i + l)] = reversed(next_tour[i : (i + l)])
            self.accept(next_tour)
            self.T *= self.cooling_rate

        self.cost_history.append((round(time.time() - self.start_time, 2), self.best_cost))
        print("Best cost obtained: ", self.best_cost)
        print("best tour", self.best_tour)
        improvement = 100 * (self.cost_history[1][1] - self.best_cost) / (self.cost_history[1][1])
        print(f"Improvement over greedy heuristic: {improvement : .2f}%")

    def batch_anneal(self, times = 100):
        self.start_time = time.time()
        for i in range(1, times + 1):
            if time.time() - self.start_time < self.limited_time:
                print(f"Iteration {i}/{times} -------------------------------")
                self.T = self.T_save
                self.cur_tour, self.cur_total_dis = greedy(self)
                # self.cost_history.append((round(time.time() - self.start_time, 2), self.cur_total_dis))
                self.anneal()

    # def visualize_routes(self):
    #     visualize_tsp.plotTSP([self.best_tour], self.distance)

   


if __name__ == "__main__":
    input_file = sys.argv[1]
    distance = read(input_file)

    for i in range(14, 50, 1):
        start_time = time.time()
        print("seed:", i)
        random.seed(i)
        sa = Simulated_annealing(distance)
        sa.batch_anneal(times = 100)
        print("Best solution:", sa.best_tour)
        sa.write_result(input_file.split("/")[-1].split(".")[0] + ".txt")
