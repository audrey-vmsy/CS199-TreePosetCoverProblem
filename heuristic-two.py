"""
----------- TO RUN -----------------
python TreePoset.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}

"""
import sys, os
sys.path.append('Utils')
from TreePoset_Utils_v2 import VERIFY, get_linear_extensions, rankInverse, group_linearOrders_by_its_root, form_transposition_graph

args = sys.argv

if not os.path.exists("outputs/"):
    os.makedirs("outputs/")

def TreePoset(upsilon):
    Ptree = []
    
    while len(upsilon) > 0:
        
        m = len(upsilon)     # number of linear orders
        n = len(upsilon[0])     # number of vertices
        for h in range(m, 0, -1):       # in descending order from the greatest number of linear orders 
            #print("\nNum. of LEs to be covered (h) = ", h)
            #print("LEs to be covered = ", upsilon[:h])
            minRank = [0 for i in range(n)]     # 0s for each vertex (i.e. each position in the list is a vertex, minRank[0] -> vertex 1 etc.)
            numCoverRelation = 0
            coverRelationP = []
            for i in range(1,n): # for each vertex position... (starting at 1 since the checking of indices is as pairs 1, 1-1 / 2, 2-1 etc)
                for j in range(h):  # in each linear order...
                    #print("Current linear order: ", upsilon[j])
                    v2 = rankInverse(i, upsilon[j]) # get the element in index i of the linear order
                    #print("Element v2 =", v2, " has the rank ", i)
                    if minRank[int(v2)-1] == 0:  # if the minRank of the element isn't set yet
                        v1 = rankInverse(i-1, upsilon[j]) # get the element preceding our current vertex (based on the linear extension's ordering)
                        #print("Element v1 =", v1, " precedes v2 =", v2, " with the rank ", i-1)
                        coverRelationP.append((int(v1),int(v2))) # add a cover relation from the preceding vertex to the current one
                        #print("New cover relation: ",(int(v1),int(v2)))
                        minRank[int(v2)-1] = i # set the new min ranks 
                        minRank[int(v1)-1] = i-1
                        numCoverRelation +=1

                if numCoverRelation == n-1: # if the number of cover relations reaches its maximum (one for each succeeding pair of vertices)
                    break
            P = get_linear_extensions(coverRelationP) # get all possible linear extensions of the found cover relations
            if VERIFY(P, upsilon[:h]): # verify if the yielded poset is equal to the input linear orders
                #print("Cover relations found: ", coverRelationP)
                #print("Linear extensions of found cover relations: ", P)
                #print("Input:",upsilon[:h])
                #print("VALID")
                Ptree.append(coverRelationP) 
                upsilon = upsilon[h:] # continue the process for the remaining number of linear orders (if any)
                break
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
            group = form_transposition_graph(group)
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




