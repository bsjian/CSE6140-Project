import networkx as nx
import sys
import math
import heapq
import time

def MST(filePath):
	def distance(start, end):
		x_distance = abs(start[1] - end[1])
		y_distance = abs(start[2] - end[2])
		return round(math.sqrt(pow(x_distance, 2) + pow(y_distance, 2)))

	def distance_GEO(start, end):
		def convertRadiant(x):
			PI = 3.141592
			deg = int(x)
			minimum = x - deg
			rad = PI * (deg + 5.0 * minimum/ 3.0) / 180.0
			return rad
		RRR = 6378.388
		q1 = math.cos(convertRadiant(start[2]) - convertRadiant(end[2]))
		q2 = math.cos(convertRadiant(start[1]) - convertRadiant(end[1]))
		q3 = math.cos(convertRadiant(start[1]) + convertRadiant(end[1]))
		return (RRR*math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)

	def read_graph(filePath):
		#make sure to add to filename the directory where it is located and the extension .txt
		G = nx.MultiGraph()
		currentFile = filePath
		Nodes = []
		Nodes_meo = {}
		with open(currentFile, 'r') as f:
			typee = "U"
			for line in f:
				if line.find("GEO")!=-1:
					typee = "GEO"
				if len(line.strip(" ").split(" "))!=3 or line.find(":")>=0:
					continue
				nums = list(map(lambda x: float(x), line.strip(" ").split(" ")))
				nums[0] = int(nums[0])
				Nodes.append(nums)
				Nodes_meo[nums[0]] = nums
				print(nums)
		for i in range(len(Nodes)):
			for j in range(i+1, len(Nodes)):
				if typee =="U":
					G.add_edge(Nodes[i][0], Nodes[j][0], weight = distance(Nodes[i], Nodes[j]))
				else:
					G.add_edge(Nodes[i][0], Nodes[j][0], weight = distance_GEO(Nodes[i], Nodes[j]))
		return G, Nodes_meo, typee

	def computeMST(G):
		a = {}            # a[v] Shortest edge between v and a node in explored set S
		myheap = []
		for n in G.nodes:
			a[n] = [sys.maxsize, -1]                # a[v] = [weight, node_to_S]
			heapq.heappush(myheap, (a[n], n))       # ([weight, node_to_S], v) in heap
		visited = set()
		MST = nx.Graph()
		res = 0
		i = 0
		while myheap:
			cur = heapq.heappop(myheap)             # cur = ([weight, node_to_S], v)
			if cur[0][1] == -10:                    # cur[0][1] = node_to_S
				continue
			# print('---------------Processing Node ', cur[1])
			if i != 0:
				res += a[cur[1]][0]
				# print("---res = ", res)
				MST.add_edge(a[cur[1]][1], cur[1], weight=a[cur[1]][0])
			visited.add(cur[1])
			i += 1
			for m in G.adj[cur[1]]:   # every m is a node connected to cur[1]
				if m not in visited:
					min_weight = sys.maxsize
					for e in G[cur[1]][m]:   # every e is an edge id for node m to node cur[1]
						min_weight = min(min_weight, G[cur[1]][m][e]['weight'])
					if m in a:
						if min_weight < a[m][0]:
							remove = a.pop(m)
							remove[1] = -10
							a[m] = [min_weight, cur[1]]
							heapq.heappush(myheap, (a[m], m))
					else:
						a[m] = [min_weight, cur[1]]
						heapq.heappush(myheap, (a[m], m))
		return res, MST


	time_start=time.time()

	G, Nodes_meo, typee = read_graph(filePath)
	MSTweight, MST = computeMST(G)

	fileName = filePath.split('/')[-1].strip(" ").strip(".tsp")
	visit = set()

	head = list(MST.nodes)[0]
	begin_node = head
	sumWeight = 0
	finalPath = [head]
	visit.add(head)
	stack = list(MST.adj[head])
	pre = head
	while stack:
		cur = stack.pop()
		finalPath.append(cur)
		visit.add(cur)
		if typee == "U":
			sumWeight += distance(Nodes_meo[pre], Nodes_meo[cur])
		else:
			sumWeight += distance_GEO(Nodes_meo[pre], Nodes_meo[cur])
		for n in list(MST.adj[cur]):
			if n not in visit:
				stack.append(n)
				visit.add(n)
		pre = cur
	if typee == "U":
		sumWeight += distance(Nodes_meo[pre], Nodes_meo[begin_node])
	else:
		sumWeight += distance_GEO(Nodes_meo[pre], Nodes_meo[begin_node])
	finalPath.append(begin_node)
	sumWeight = round(sumWeight)

	time_end=time.time()
	time_total = time_end-time_start

	print("Total Weight: ", sumWeight)
	print(finalPath)
	return sumWeight, finalPath, time_total


def writeToFile(sumWeight, finalPath, time_total, fileName, foldname, cutoff, seed):
	if foldname[-1]!="/": foldname+="/"
	writeFile = foldname + fileName +"_Approx_"+str(cutoff)+"_"+ str(seed)+".sol"
	with open(writeFile, 'w') as wf:
		wf.write(str(sumWeight)+"\n")
		wf.write(str(finalPath).strip("[").strip("]"))


	writeFile2 = foldname + fileName +"_Approx_"+str(cutoff)+"_"+ str(seed)+".trace"
	with open(writeFile2, 'w') as wf:
		wf.write('%.2f'%round(time_total,2)+", "+str(sumWeight))



