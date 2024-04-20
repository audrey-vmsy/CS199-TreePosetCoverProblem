"""
----------- TO RUN -----------------
python TreePoset.py <vertex count*> 

where <vertex count*> = {3, 4, 5, 6}

"""
import sys, os
sys.path.append('Utils')
from TreePoset_Utils_v2 import binaryRelation, combinePosetv2, get_linear_extensions, gen_tree_poset

args = sys.argv

if not os.path.exists("outputs/"):
    os.makedirs("outputs/")

def TreePoset(upsilon, inputLinearOrders):
    Pstar = gen_tree_poset(inputLinearOrders)
    if Pstar != None:
        return [Pstar]

    Pstar = upsilon
    Ptree = []
    isCombined = True
    
    while isCombined:
        isCombined = False

        while len(Pstar) > 0:
            poset1 = Pstar[0]
            Pstar.pop(0)
            hasPair = False
            for i in range(len(Pstar)):
                combinedposet = combinePosetv2(poset1, Pstar[i])
                if combinedposet != None and set(get_linear_extensions(combinedposet)) == set(get_linear_extensions(poset1)).union(set(get_linear_extensions(Pstar[i]))):
                    Ptree.append(combinedposet) 
                    Pstar.pop(i)
                    hasPair = True
                    isCombined = True
                    break
            
            if not hasPair:
                Ptree.append(poset1)
            
        Pstar = Ptree.copy()
        Ptree = []

    return Pstar

#with open(f'inputs/{args[1]}.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
with open(f'optsol/inputs/{args[1]}treesinput.txt', 'r') as input_file, open(f'outputs/output_{args[1]}.txt', 'w') as output_file:
    for line in input_file:
        inputLinearOrders = [int(x) for x in line.strip('[]\n').split(',')]
        inputLinearOrders.sort()
        inputLinearOrders = [str(item) for item in inputLinearOrders]

        Pstar = binaryRelation(inputLinearOrders)
        posets = TreePoset(Pstar, inputLinearOrders)

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


# # input_linear_order = [1234, 1243, 1324, 1342, 1423, 1432]
# input_linear_order = [1234, 1243, 1324, 1342, 1423]

# # # 
# # # input_linear_order = [1234, 1324, 1423, 1432]       # returns a hammock poset (P1)
# # # input_linear_order = [1243, 1423, 1432, 4123, 4132] # haven't considered inputs with different roots
# # # input_linear_order = ['12345', '12354', '12435', '13245', '13254', '13524', '14253', '14523', '14532', '15342', '15423', '15432']     # outputs 4 posets (optimal solution: 2 posets only)

# # # current test case
# # # input_linear_order = ['12345', '12354', '12435', '13245', '13254', '13524', '14253', '14523', '14532', '15342', '15423', '15432']
# # # input_linear_order = ['12345', '12354', '12435', '13245', '13254', '13524']


# input_linear_order = [str(item) for item in input_linear_order]
# input_linear_order.sort()
# Pstar = binaryRelation(input_linear_order)

# # run TreePoset
# result = TreePoset(Pstar)

# for i in range(len(result)):
#     print(f"P{str(i+1)}: {result[i]}")

