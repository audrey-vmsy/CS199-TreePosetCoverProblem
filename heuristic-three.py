"""
----------- TO RUN -----------------
python TreePoset.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}

"""
import sys, os
import networkx as nx
import pylab as p
from collections import defaultdict, OrderedDict
sys.path.append('Utils')
from TreePoset_Utils_v2 import VERIFY, get_linear_extensions, rankInverse, group_linearOrders_by_its_root, binaryToCover, isTreePoset, binaryRelation

args = sys.argv

if not os.path.exists("outputs/"):
    os.makedirs("outputs/")

def TreePoset(upsilon):
    Ptree = []
    
    # Generate Transposition Graph
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Edges = dict([])
    for u in upsilon:
        Edges[u] = []
    
    for a in range(l):
        G.add_node(upsilon[a])
        for b in range(a+1, l):
            pairs = [upsilon[a][i:i+2] for i in range(len(upsilon[a])) if "".join(reversed(upsilon[a][i:i+2])) in upsilon[b] and 
                     upsilon[a][0:i]+upsilon[a][i+2:len(upsilon[a])] == upsilon[b][0:i]+upsilon[b][i+2:len(upsilon[b])]]
            if len(pairs)>0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0],pairs[0][1]])))
                Edges[upsilon[a]].append([tuple(sorted((pairs[0][0],pairs[0][1]))), upsilon[b]])
                Edges[upsilon[b]].append([tuple(sorted((pairs[0][0],pairs[0][1]))), upsilon[a]])
                #print("Nodes", upsilon[a], upsilon[b])
                #print("Added edge/s", pairs)

    # Form Tree Posets
    while len(nodes)>0:
        #print("G nodes =", G.nodes)
        # Create list of neighbor nodes
        Neighbors = dict([])
        for n in list(G.nodes):
            #print(n,"-", list(G.neighbors(n)))
            Neighbors[n]=list(G.neighbors(n))
        
        #print(Neighbors)

        # Obtain starting node
        numNeighbors = [[len(Neighbors[l]),l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key = lambda l: l[0])
        startNode = numNeighbors[0][1]

        # Initialize start values
        curLE = [startNode]
        curP = binaryRelation([startNode])
        remEdges = []

        #print("startNode =",startNode)

        cond = 1
        while(cond):
            #print("curLE = ", curLE)
            #print("curP = ", curP)
            # Obtain all edges connected to members of curLE and their connected nodes
            potentialPairs = []
            potentialNodes = dict([])
            for node in curLE:
                potentialPairs += [Edges[node][n] for n in range(len(Edges[node])) 
                                if Edges[node][n][1] in nodes]
                for pair in potentialPairs:
                    #print("pair =", pair)
                    id = tuple(sorted([int(p) for p in pair[0]]))
                    if potentialNodes.get(id)==None:
                        potentialNodes[id] = [pair[1]]
                    elif pair[1] not in potentialNodes[id]:
                        potentialNodes[id] += [pair[1]]

            # Sort potential extensions by frequency  
            potentialNodes = sorted(potentialNodes.items(), key=lambda x: len(x[1]), reverse=True)
            #print("sorted potential nodes =", potentialNodes)

            i = 1
            for potentials in potentialNodes:
                tempNodes = [n for n in list(set(curP + binaryRelation(potentials[1]))) if n not in remEdges+[potentials[0], (potentials[0][1], potentials[0][0])]]
                #print("tempNodes =", tempNodes)
                #print("edge to extend from =", potentials[0])
                #print("new nodes =", potentials[1])

                P = get_linear_extensions(binaryToCover(tempNodes,len(upsilon[0])))
                #print("P =",P)
                #print("Potential new curLE =",curLE+[p for p in potentials[1] if p not in curLE])
                if isTreePoset(tempNodes) and VERIFY(P, curLE+[p for p in potentials[1] if p not in curLE]):
                    #print("ACCEPTED")
                    curP = tempNodes
                    curLE += [p for p in potentials[1] if p not in curLE]
                    nodes = [n for n in nodes if n not in curLE]
                    remEdges += [potentials[0], (potentials[0][1], potentials[0][0])]
                    break
                elif i>=len(potentialNodes):
                    #print("END OF LOOP")
                    cond = 0
                #else:
                    #print("REJECTED")
                    #print("P =",P)
                    #print("Potential new curLE =",curLE+[p for p in potentials[1] if p not in curLE])
                    #print(input())
                i += 1
            #print("OUT OF FOR LOOP")

            if len(potentialNodes)==0:
                cond=0

        #print("nodes =", nodes)
        #print("curLE = ", curLE)
        #print("G nodes =",G.nodes)

        '''
        # For drawing the transposition graphs
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

        p.show()'''
        nodes = [n for n in nodes if n not in curLE]

        for le in curLE:
            G.remove_node(le)

        Ptree.append(curP)

    #print("Ptree =", Ptree)
    
    return Ptree

count = 1
#with open(f'inputs/{args[1]}.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
with open(f'optsol/inputs/{args[1]}treesinput.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
    for line in input_file: # work on each test case
        print(count)
        count+=1
        inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]

        inputLinearOrders.sort()
        inputLinearOrders = [str(item) for item in inputLinearOrders]

        #print("Input: ", inputLinearOrders)
        
        posets = []
        # group linear orders according to their root
        groupings = group_linearOrders_by_its_root(inputLinearOrders)

        #print("Groupings: ", groupings)

        # for each group, there is a set of posets
        # append each poset to the list posets
        
        for group in groupings:
            poset_group = TreePoset(group)
            for poset in poset_group:
                posets.append(poset)
        
        if posets != None:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            for i in range(len(posets)):
                output_file.write(f"P{str(i+1)}: {posets[i]}\n")
            output_file.write("\n")

        else:
            output_file.write(f"Input: {[int(x) for x in inputLinearOrders]}\n")
            output_file.write("None!!!!!\n\n")

if posets != None:
    print(f"Generated all output of input linear order sets with {args[1]} vertices")
    print("Check 'output' directory")
else:
    print("Generated nothing")




