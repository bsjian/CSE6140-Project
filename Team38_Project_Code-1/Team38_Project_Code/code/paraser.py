import argparse
from BnB import *
from anneal import *
from MSTforTSP import *
from tabu import *
from util import *

parser = argparse.ArgumentParser(description='CSE6140 Project for Team 38')

# Instance file argument
parser.add_argument('-inst', type=str, help='Instance File')

# Algorithm argument
parser.add_argument('-alg', type=str, help='Algorithm')

# cutoff time
parser.add_argument('-time', type=str, help='Cutoff Time')

# Seed
parser.add_argument('-seed', type=int, help='Random Seed')

# -inst <filename>
# -alg [BnB | Approx | LS1 | LS2]
# -time <cutoff_in_seconds>
# -seed <random_seed>

args = parser.parse_args()

input_file = args.inst
alg = args.alg
Cutoff_Time = args.time
seed = args.seed

instance = input_file.split("/")[-1].split(".")[0]
output_path = "./output/"

if alg == "BnB" or alg == "bnb":
	distance = read(input_file)
	newBnB = BnB(distance)
	newBnB.solve()
	outfile_sol_name = instance + "_" + alg + "_" + Cutoff_Time +"_"+ str(seed)+ ".sol"
	outfile_trace_name = instance + "_" + alg + "_" + Cutoff_Time +"_"+ str(seed)+ ".trace"

	outfolder = os.path.join(output_path, alg)
	if not os.path.exists(output_path):
			os.mkdir(output_path)
	if not os.path.exists(outfolder):
			os.mkdir(outfolder)
	solution(os.path.join(output_path, alg, outfile_sol_name), newBnB.best_cost, newBnB.best_path)
	solution_trace(os.path.join(output_path, alg, outfile_trace_name), newBnB.cost_history[1:])

elif alg == "Approx":
	umWeight, finalPath, time_total = MST(input_file)
	outfolder = os.path.join(output_path, alg)
	if not os.path.exists(output_path):
			os.mkdir(output_path)
	if not os.path.exists(outfolder):
			os.mkdir(outfolder)
	writeToFile(umWeight, finalPath, time_total, instance, outfolder, Cutoff_Time, str(seed))

elif alg == "LS1":
	distance = read(input_file)
	start_time = time.time()
	print("seed:", seed)
	random.seed(seed)
	sa = Simulated_annealing(distance, limited_time = int(Cutoff_Time))
	sa.batch_anneal(times = 100)
	outfile_sol_name = instance + "_" + alg + "_" + Cutoff_Time +"_"+ str(seed) +".sol"
	outfile_trace_name = instance + "_" + alg + "_" + Cutoff_Time +"_"+ str(seed) +".trace"
	outfolder = os.path.join(output_path, alg)
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	if not os.path.exists(outfolder):
			os.mkdir(outfolder)
	solution(os.path.join(output_path, alg, outfile_sol_name), sa.best_cost, sa.best_tour)
	solution_trace(os.path.join(output_path, alg, outfile_trace_name), sa.cost_history[1:])



elif alg == "LS2":
	distance = read(input_file)
	tabu = Tabu(distance, limited_time = int(Cutoff_Time))
	tabu.set_seed(seed)
	print("Seed", seed)
	tabu.batch_tabu(times = 50)

	outfile_sol_name = instance + "_" + alg + "_" + Cutoff_Time+"_"+ str(seed) + ".sol"
	outfile_trace_name = instance + "_" + alg + "_" + Cutoff_Time +"_"+ str(seed)+ ".trace"
	outfolder = os.path.join(output_path, alg)
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	if not os.path.exists(outfolder):
			os.mkdir(outfolder)
	solution(os.path.join(output_path, alg, outfile_sol_name), tabu.best_cost, tabu.best_tour)
	solution_trace(os.path.join(output_path, alg, outfile_trace_name), tabu.cost_history[1:])

