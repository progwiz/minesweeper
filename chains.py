import global_vars as g
import networkx as nx
import numpy as np
import algorithm
import minefield_generator as mg
import matplotlib.pyplot as plt
import sys
import os
os.environ["PATH"] += os.pathsep + 'C:/ProgramData/Anaconda2/envs/python36/Library/bin/graphviz'

def manhattan(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return (abs(x1-x2)+abs(y1-y2))

def get_chain(loc,chain_points,chain_edges):
    for parent in g.parent_dict[loc]:
        if (loc,parent) not in chain_edges:
            chain_edges=list(set(chain_edges).union(set([(parent,loc)])))
        if parent not in chain_points:
            chain_points=list(set(chain_points).union(set([parent])))
            chain_points,chain_edges=get_chain(parent,chain_points,chain_edges)
    return chain_points,chain_edges
        
def graph_combinations(n,combi,final_combinations):
    if n==len(g.parent_dict.keys())-1:
        if len(g.parent_dict[g.actual_index(n)]):
            for parent_combination in g.parent_dict[g.actual_index(n)]:
                combi[g.actual_index(n)]=parent_combination
                final_combinations.append(combi)
        else: final_combinations.append(combi)
    else:
        if len(g.parent_dict[g.actual_index(n)]):
            for parent_combination in g.parent_dict[g.actual_index(n)]:
                combi[g.actual_index(n)]=parent_combination
                final_combinations = graph_combinations(n+1,combi, final_combinations)
        else: final_combinations = graph_combinations(n+1, combi, final_combinations)
    return final_combinations

if __name__=="__main__":

    dim=10
    max_spatial_dist=0
    max_chain_length=0
    max_chain_lens=[]
    ps=np.arange(0.1,0.36,0.05)
    for p in ps:
        max_chain_len=[]
        for i in np.arange(20):
            while True:
                #field=np.array([[1,2,3,2],[2,-1,-1,-1],[3,-1,8,-1],[2,-1,-1,-1]])
                field=mg.generate_random_field(dim,dim,p,display=False)
                g.initialize_vals(dim,dim)
                g.generate_field(dim,dim)
                g.field[g.next_loc]=field[g.next_loc]
                while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                    algorithm.fetch_next(adaptive=False, chains=True)
                    g.field[g.next_loc]=field[g.next_loc]
                
                if np.array_equal(g.next_loc,(-1,-1)):
                    product=1
                    for index in np.arange(g.dim1*g.dim2):
                        product=product*max([len(g.parent_dict[g.actual_index(index)]),1])
                    combis=graph_combinations(0,{},[])
                    #print(product, len(combis))
                    for no,combi in enumerate(combis):
                        sys.stdout.write("\r dim: "+str(dim)+" p: "+str(p)+" iteration: "+str(i)+" combi: "+str(no)+" of "+str(len(combis))+"             ")
                        """
                        locs,edges=get_chain(g.actual_index(index),[g.actual_index(index)],[])
                        G=nx.DiGraph()
                        G.add_nodes_from(locs)
                        for edge in edges:
                            G.add_edge(edge[0],edge[1])
                        """
                        locs=[g.actual_index(index) for index in np.arange(g.dim1*g.dim2)]
                        G=nx.DiGraph()
                        G.add_nodes_from(locs)
                        for child, parent_list in combi.items():
                            for parent in parent_list:
                                G.add_edge(parent,child)
                        
                        try:
                            longest_path=nx.dag_longest_path(G)
                            longest_path_length=len(longest_path)
                            if longest_path_length>max_chain_length:
                                max_chain_length=longest_path_length
                                max_chain_field=field
                                max_chain_chain=longest_path
                                max_chain_graph=G
                            for loc in locs:
                                for descendant in nx.descendants(G,loc):
                                    spatial_dist=manhattan(loc,descendant)
                                    if spatial_dist>max_spatial_dist:
                                        max_spatial_dist=spatial_dist
                                        max_spatial_field=field
                                        max_spatial_pair=(loc,descendant)
                                        max_spatial_graph=G
                            max_chain_len.append(nx.dag_longest_path_length(G))
                            #flag=1
                            break
                        except: 
                            pass
                            
                    break
        max_chain_lens.append(np.mean(max_chain_len))
                
    
    print("Max spatial distance pair: ",max_spatial_pair)
    print("max spatial distance : ", max_spatial_dist)
    
    print("\n\nLongest path : ")
    str_chain=""
    for node in max_chain_chain:
        str_chain+=str(node)+" -> "
    print(str_chain)
    print("Longest path length: ", max_chain_length)
    
    p=nx.drawing.nx_pydot.to_pydot(max_chain_graph)
    p.write_png('longest path graph.png')
    p=nx.drawing.nx_pydot.to_pydot(max_spatial_graph)
    p.write_png('longest influence chain.png')
    g.display_field(max_spatial_field,dim,dim,"max spatial field.png")
    g.display_field(max_chain_field,dim,dim,"max chain field.png")
    plt.figure()
    plt.plot([int(dim*dim*p) for p in ps],max_chain_lens)
    plt.xlabel("Number of mines")
    plt.ylabel("Avg maximum length of chain")
    plt.title("Maximum lengths of chains of influence on 8x8 board.")
    plt.savefig("chain length graph.png")
    