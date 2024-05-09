"""
----------- TO RUN -----------------
python analysis.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}

note: Before running, run optimalsolutions.py first to generate the inputs and optimal solutions

"""

import sys, os
from ast import literal_eval
sys.path.append('Utils')
from Analysis_Utils import isTreePoset, areTreePosets, isAllConnected, binaryToCover, covered, form_transposition_graph
from TreePoset_Utils_v2 import get_linear_extensions

args = sys.argv

#
with open(f'optsol/trees/{args[1]}treesoptsol.txt', 'r') as optimal_file, open(f'outputs/output_{args[1]}.txt', 'r') as HeuristicOutput_file:
    #Optimal Solution Data
    inputs = []
    optcost = []
    optsol = []
    insert_optsols = 0
    for line in optimal_file:
        if line[:7] == "Input: ":
            inputs.append(literal_eval(line[7:-1]))
        elif line[:23] == "Optimal solution cost: ":
            optcost.append(int(line[23:]))
            insert_optsols = int(line[23:])
        elif line == "\n":
            continue
        else:
            if insert_optsols == optcost[-1] and line[0] == '[': #first poset is added to the list of optimal solutions
                lst = literal_eval(line)
                optsol.append([])
                optsol[-1].append(lst)
                insert_optsols -= 1     #decrement until 0 (all posets are added)
            else:
                #print(insert_optsols)
                lst = literal_eval(line)
                optsol[-1].append(lst) #n + 1 posets are added to the latest group of posets added
                insert_optsols -= 1

    n = len(str(inputs[0][0]))
    #Heuristic data
    heuristicsol = []
    for line in HeuristicOutput_file:
        if line[:7] == "Input: ":
            continue
        elif line[:4] == "P1: ":
            #first poset is added to the list of heuristic solutions
            start = line.index('[')
            lst = literal_eval(line[start:])
            lst = binaryToCover(lst, n)
            heuristicsol.append([])
            heuristicsol[-1].append(lst)
        elif line == "\n":
            continue    
        else:
            start = line.index('[')
            lst = literal_eval(line[start:])
            lst = binaryToCover(lst, n)
            heuristicsol[-1].append(lst)

    #write to a new file <vertex>analysis.py on directory /analysis
    #write analysis per input in this format:
    #Input: [123, 132]
    #Optimal Solution: [[(1, 2), (1, 3)]]
    #Heuristic Solution: [[(1, 2), (1, 3)]]
    #Analysis: FEASIBLE - OPTIMAL
    # ... UNTIL EOF
    #SUMMARY
    #Total Number of Inputs:
    #Total Number of FEASIBLE Heuristic Solutions:
    #Total Number of Optimal Heuristic Solutions:

    if not os.path.exists("analysis/"):
        os.makedirs("analysis/")
    
    output = open(f"analysis/{args[1]}analysis.txt", "w")

    #for summary
    len_inputs = len(inputs)
    Feasible = 0
    optimal = 0
    not_optimal = []
    performanceRatio = 0
    for (input, cost, O_sol, H_sol) in zip(inputs, optcost, optsol, heuristicsol):
        output.write("Input: "+ str(input)+"\n")
        output.write("Optimal Solution: "+ str(O_sol)+"\n")
        output.write("Heuristic Solution: "+ str(H_sol)+"\n")
        if areTreePosets(H_sol) and isAllConnected(H_sol, n) and len(H_sol) == cost and covered(H_sol) == input:
            output.write("Analysis: FEASIBLE - OPTIMAL\n")
            Feasible += 1
            optimal += 1
            performanceRatio +=1
        elif areTreePosets(H_sol) and isAllConnected(H_sol, n) and len(H_sol) > cost and covered(H_sol) == input:
            diff_cost = len(H_sol) - cost
            not_optimal.append(diff_cost)
            Feasible += 1
            performanceRatio += len(H_sol) / cost
            output.write("Analysis: FEASIBLE - NOT OPTIMAL\n")
            output.write("(Optimal) Linear Extensions Covered:\n")

            print("Input: "+ str(input))
            print("(Optimal) Linear Extensions Covered:")
            for sol1 in O_sol:
                output.write(str(sol1)+": "+str(get_linear_extensions(sol1))+"\n")
                print(str(sol1)+": "+str(get_linear_extensions(sol1)))
            output.write("(Heuristic) Linear Extensions Covered:\n")

            print("(Heuristic) Linear Extensions Covered:")
            for sol2 in H_sol:
                output.write(str(sol2)+": "+str(get_linear_extensions(sol2))+"\n")
                print(str(sol2)+": "+str(get_linear_extensions(sol2)))
            #output.write("Heuristic_Cost - Optimal_Cost: "+str(diff_cost)+"\n")
            
            #form_transposition_graph([str(i) for i in input])
        else:
            output.write("Analysis: NOT FEASIBLE - NOT OPTIMAL\n")
            output.write("Output: "+ str(covered(H_sol))+"\n")
            output.write("(Optimal) Linear Extensions Covered:\n")
            for sol1 in O_sol:
                output.write(str(sol1)+": "+str(get_linear_extensions(sol1))+"\n")
            output.write("(Heuristic) Linear Extensions Covered:\n")
            for sol2 in H_sol:
                output.write(str(sol2)+": "+str(get_linear_extensions(sol2))+"\n")
            #form_transposition_graph([str(i) for i in input])
        output.write("\n")

    if len(not_optimal) == 0:
        average_diff_not_optimal = 0
        max_not_optimal = 0
    else:
        average_diff_not_optimal = sum(not_optimal)/len(not_optimal)
        max_not_optimal = max(not_optimal)
    output.write("Summary\n")
    output.write("Total Number of Inputs: "+str(len_inputs)+"\n")
    output.write("Total Number of Feasible Heuristic Solutions: "+str(Feasible)+"\n")
    output.write("Total Number of Optimal Heuristic Solutions: "+str(optimal)+"\n")
    #output.write("Average difference in Heuristic Cost and Optimal Cost: "+str(average_diff_not_optimal)+"\n")
    #output.write("Maximum difference in Heuristic Cost and Optimal Cost: "+str(max_not_optimal)+"\n")
    output.write("Approximation Error: "+str((performanceRatio/len_inputs))+"\n")
    output.close

    print("FINISHED ANALYSING HEURISTIC")