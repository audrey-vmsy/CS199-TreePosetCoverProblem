import networkx as nx
import pylab as p

def get_linear_extensions(cover_relation):
    # Create a directed graph from the cover relation
    G = nx.DiGraph()
    for a, b in cover_relation:
        G.add_edge(a, b)
    
    # Compute all possible topological sortings (i.e., linear extensions) of the graph
    sortings = list(nx.all_topological_sorts(G))
    
    # Convert each sorting to a string and return the list of all sortings
    return sorted([''.join(map(str, sorting)) for sorting in sortings])
 
def VERIFY(P, Y):
    if sorted(P) == sorted(Y):
        return True
    return False

def rankInverse(index, linearOrder): # where rank gives the position of an element, inverse gives the element in a position
    # sample input: index = 3; linearOrder = 1234; 
    return linearOrder[index]       # output: 4

def group_linearOrders_by_its_root(upsilon):
    grouped_upsilon = {}
    for linearOrder in upsilon:
        root = linearOrder[0]
        if root in grouped_upsilon:
            grouped_upsilon[root].append(linearOrder)
        else:
            grouped_upsilon[root] = [linearOrder]
    
    return list(grouped_upsilon.values())


def form_transposition_graph(upsilon):
    G = nx.Graph()
    l = len(upsilon)
    nodes = upsilon
    Neighbors = dict([])
    for a in range(l):
        G.add_node(upsilon[a])
        for b in range(a+1, l):
            pairs = [upsilon[a][i:i+2] for i in range(len(upsilon[a])) if "".join(reversed(upsilon[a][i:i+2])) in upsilon[b] and 
                     upsilon[a][0:i]+upsilon[a][i+2:len(upsilon[a])] == upsilon[b][0:i]+upsilon[b][i+2:len(upsilon[b])]]
            if len(pairs)>0:
                G.add_edge(upsilon[a], upsilon[b], label=str(sorted([pairs[0][0],pairs[0][1]])))
                #print("Nodes", upsilon[a], upsilon[b])
                #print("Added edge/s", pairs)

    for n in list(G.nodes):
        #print(n,"-", list(G.neighbors(n)))
        Neighbors[n]=list(G.neighbors(n))
    #print("Nodes:", list(G.nodes))

    # For drawing the transposition graphs
    #pos = nx.spring_layout(G)
    #nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

    if len(Neighbors)>0:
        numNeighbors = [[len(Neighbors[l]),l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key = lambda l: l[0])
        #print(numNeighbors)

        edges = nx.bfs_edges(G, numNeighbors[0][1])
        nodes = [numNeighbors[0][1]] + [v for u, v in edges]
        nodes += [l for l in upsilon if l not in nodes]
        #print(nodes)

    #p.show()
    return nodes
  
