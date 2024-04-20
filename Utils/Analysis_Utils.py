import networkx as nx
from TreePoset_Utils_v2 import get_linear_extensions
import pylab as p

def isTreePoset(cover_relations):
    n = len(cover_relations)+1
    check_vertices = [False for x in range(n)] #array that checks if all vertices are included
    parent = [0 for x in range(n)] #array of number of parents of a vertex
    for (a,b) in cover_relations:
        check_vertices[a-1] = True
        check_vertices[b-1] = True
        parent[b-1] += 1
        
    #Check if the valid poset permutation is a tree poset
    for v in parent:
        if (v > 1) or (0 not in parent):
            return False

    #check if all edges are connected
    if False not in check_vertices and nx.is_directed_acyclic_graph(nx.DiGraph(cover_relations)):
        return True
    else:
        return False

def areTreePosets(group_posets):
    flag = True
    for poset in group_posets:
        if not isTreePoset(poset):
            flag = False
            return flag
    return flag

def isAllConnected(P,n):
    for p in P:
        check_vertices = [False for x in range(n)] #array that checks if all vertices are included
        for (a,b) in p:
            check_vertices[a-1] = True
            check_vertices[b-1] = True
        if False not in check_vertices and nx.is_directed_acyclic_graph(nx.DiGraph(p)):
            continue
        else:
            return False
    return True

def binaryToCover(P,n):
    coverRelations = []
    for (u,v) in P:
        if (u,v) in coverRelations:
            continue
        if len(coverRelations) == n - 1:
            break
        transitive = False
        for w in range(1, n+1):
            if w == u or w == v:
                continue
            else:
                if (u,w) in P and (w,v) in P:
                    transitive = True
                    break
        if not transitive:
            coverRelations.append((u,v))
    return sorted(coverRelations)

def covered(group_posets):
    coveredlinearorders = []
    for poset in group_posets:
        coveredlinearorders += get_linear_extensions(poset)
    coveredlinearorders = [int(x) for x in list(set(coveredlinearorders))]
    return sorted(coveredlinearorders)

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
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True,font_size=10, node_size=500, node_color='#9CE5FF')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

    if len(Neighbors)>0:
        numNeighbors = [[len(Neighbors[l]),l] for l in Neighbors]
        numNeighbors = sorted(numNeighbors, key = lambda l: l[0])
        #print(numNeighbors)

        edges = nx.bfs_edges(G, numNeighbors[0][1])
        nodes = [numNeighbors[0][1]] + [v for u, v in edges]
        nodes += [l for l in upsilon if l not in nodes]
        #print(nodes)

    p.show()
    return nodes