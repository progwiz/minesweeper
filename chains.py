import global_vars as g
import networkx as nx
import numpy as np
import algorithm
import minefield_generator as mg
import matplotlib.pyplot as plt
import os
os.environ["PATH"] += os.pathsep + 'C:/ProgramData/Anaconda2/envs/python36/Library/bin/graphviz'

def manhattan(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return (abs(x1-x2)+abs(y1-y2))

if __name__=="__main__":

    dim=8
    max_spatial_dist=0
    max_chain_length=0
    max_chain_lens=[]
    for p in np.arange(0.1,0.8,0.05):
        max_chain_len=[]
        for i in np.arange(100):
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
                    locs=[g.actual_index(index) for index in np.arange(g.dim1*g.dim2)]
                    G=nx.DiGraph()
                    G.add_nodes_from(locs)
                    for child, parent_list in g.parent_dict.items():
                        for parent in parent_list:
                            G.add_edge(parent,child)
                    
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
    plt.plot([6,9,12,15,18],max_chain_lens)
    plt.xlabel("Number of mines")
    plt.ylabel("Avg maximum length of chain")
    plt.title("Maximum lengths of chains of influence on 8x8 board.")
    plt.savefig("chain length graph.png")
    