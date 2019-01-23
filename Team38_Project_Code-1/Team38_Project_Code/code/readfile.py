import os 
import sys
import time

# there are two types of input file to be dealt with
# 1. tsp; 2. GEO

def read_data(input_name):

    '''
    e.g: data = read_data(input data file)
    args: input data file
    Return: Nx3 matrix: 
            N is the number of node
            each row: [node_id, x, y]
    '''
    data = []
    with open(input_name, "r") as file:
        lines = file.readlines()
        
        for i in range(len(lines)):
            # deal with different input
            
            if lines[i][0].isdigit():
                node_id, x, y = lines[i].split(" ")
                data.append([int(node_id), 
                             float(x),
                             float(y)])
    return data