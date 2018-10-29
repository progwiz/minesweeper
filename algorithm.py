import numpy as np
import itertools
import global_vars as g

def combine_combinations(new_locs,set1,current_locs,set2):
    common_locs=list(set(current_locs) & set(new_locs))
    final_locs=list(set(current_locs).union(set(new_locs)))
    new_set=[]
    for c1 in set1:
        c1_common_locs=[loc for loc in c1 if loc in common_locs]
        for c2 in set2:
            c2_common_locs=[loc for loc in c2 if loc in common_locs]
            if set(c1_common_locs) == set(c2_common_locs):
                new_set.append(list(set(c1).union(set(c2))))
    return final_locs,new_set

def manhattan(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return (abs(x1-x2)+abs(y1-y2))

# returns location of neighbors of a node.
def get_neighbors(loc):
    x,y = loc
    nbrs=[]
    for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        if -1<x+dx<g.dim1 and -1<y+dy<g.dim2:
            nbrs.append((x+dx,y+dy))
    return nbrs

def fetch_next(adaptive=False,debug=True, chains=False):
    
    prev_loc=g.next_loc
    #print(g.field[prev_loc], prev_loc)
    # if mine revealed, game over
    if g.field[prev_loc]==-1:
        g.next_loc=(0,0)
        return
    
    # make probability of releaved cell 0
    g.probs[prev_loc]=0
    
    # add revealed cell to explored, remove from fringe, seen_nbrs
    g.explored.append(g.flat_index(prev_loc))
    g.fringe.remove(g.flat_index(prev_loc))
    g.clear=list(set(g.clear).union(set([g.flat_index(prev_loc)])))
    if g.flat_index(prev_loc) in g.seen_nbrs:
        g.seen_nbrs.remove(g.flat_index(prev_loc))

    # update set of combinations and locations used to make the combinations.
    if g.flat_index(prev_loc) in g.locs:
        g.locs.remove(g.flat_index(prev_loc))
    g.combs=[c for c in g.combs if g.flat_index(prev_loc) not in c]
    

    # get set of unexplored neighbors
    nbrs=get_neighbors(prev_loc)
    unexplored_nbrs=[g.flat_index(nbr) for nbr in nbrs if g.flat_index(nbr) not in g.explored]
    """
    if chains:
        undecided_nbrs=[g.actual_index(nbr) for nbr in unexplored_nbrs if 0<g.probs[g.actual_index(nbr)]<1]
        decided_nbrs=[nbr for nbr in nbrs if g.probs[nbr] in (0,1)]
        decided_mines=[nbr for nbr in decided_nbrs if g.probs[nbr]==1]
        decided_clear=[nbr for nbr in decided_nbrs if g.probs[nbr]==0]
        if g.field[prev_loc]==len(decided_mines):
            decided_nbrs=[nbr for nbr in decided_nbrs if nbr not in decided_clear]
        elif g.field[prev_loc]==8-len(decided_clear):
            decided_nbrs=[nbr for nbr in decided_nbrs if nbr not in decided_mines]
        for nbr in undecided_nbrs:
            g.parent_dict[nbr]=list(set(g.parent_dict[nbr]).union(set([prev_loc])))
        for nbr1 in decided_nbrs:
            for nbr2 in undecided_nbrs:
                g.parent_dict[nbr2]=list(set(g.parent_dict[nbr2]).union(set([nbr1])))
    """    
    # add unexplored neighbors to seen nbrs and fringe
    g.seen_nbrs=set(g.seen_nbrs).union(set(unexplored_nbrs))
    g.fringe=set(g.fringe).union(set(unexplored_nbrs))
    
    # add neighbors of unexplored neighbors to fringe
    for nbr in unexplored_nbrs:
        nbr_nbrs=[g.flat_index(n) for n in get_neighbors(g.actual_index(nbr)) if g.flat_index(n) not in g.explored]
        g.fringe=set(g.fringe).union(set(nbr_nbrs))
    
    # this condition is used while solving for special case
    if g.field[prev_loc]!=-2:
        
        # get combinations of unexplored neighbors
        new_combinations=list(itertools.combinations(unexplored_nbrs,g.field[prev_loc]))
        """
        print("new combinations:")
        for c in new_combinations:
            if 12 in c and 7 in c:
                print(c)
        """
        
        # combine old and new set of combinations
        g.locs,g.combs=combine_combinations(unexplored_nbrs,new_combinations,g.locs,g.combs)
        
        # update probabilities of all nodes
        for loc in g.locs:
            loc_1_count=len([c for c in g.combs if loc in c])
            try:
                g.probs[g.actual_index(loc)]=loc_1_count/len(g.combs)
            except:
                g.probs[g.actual_index(loc)]=0
                
    if chains:
        new_mcs=[g.actual_index(node) for node in np.arange(g.dim1*g.dim2) if g.probs[g.actual_index(node)] in [1,0] and node not in g.mines+g.clear]
        for new_mc in new_mcs:
            parent_sets=[]
            new_mc_nbrs=sorted(get_neighbors(new_mc), key=lambda x:manhattan(x,prev_loc))
            for new_mc_nbr in new_mc_nbrs:
                if g.flat_index(new_mc_nbr) in g.explored:
                    nbr_val=g.field[new_mc_nbr]
                    if g.probs[new_mc]==1:
                        req_size=8-nbr_val
                    else:
                        req_size=nbr_val
                    useful_nbrs=[nbr for nbr in get_neighbors(new_mc_nbr) if g.probs[nbr]==1-g.probs[new_mc]]
                    if len(useful_nbrs)==req_size:
                        parent_sets.append([new_mc_nbr]+useful_nbrs)
                        #g.parent_dict[new_mc]=list(set(g.parent_dict[new_mc]).union(set([new_mc_nbr])))
                        #for useful_nbr in useful_nbrs:
                        #g.parent_dict[new_mc]=list(set(g.parent_dict[new_mc]).union(set(useful_nbrs)))
                        #break
            g.parent_dict[new_mc]=parent_sets
                        
            if g.probs[new_mc]==1:
                g.mines=list(set(g.mines).union(set([g.flat_index(new_mc)])))
            else:
                g.clear=list(set(g.clear).union(set([g.flat_index(new_mc)])))
            #print(new_mc, g.parent_dict[new_mc])
        
        
        """
        new_determined_nodes=[g.actual_index(node) for node in np.arange(g.dim1*g.dim2) if node not in g.mines+g.clear and g.probs[g.actual_index(node)] in [0,1]]
        #print("\n\n ", new_determined_nodes)
        for node in new_determined_nodes:
            for parent in get_neighbors(node):
                if parent in g.explored:
                    nbrs=[nbr for nbr in get_neighbors(parent) if 0<g.probs[nbr]<1]
                    for nbr in nbrs:
                        g.parent_dict[nbr]= list(set(g.parent_dict[nbr]).union(set([node])))
        """
    #find node with minimum probability of being a mine, definite mines, definite clear cells
    minimum=1.1
    minimum_set=[]
    for flat_loc in g.fringe:
        actual_loc=g.actual_index(flat_loc)
        p=g.probs[actual_loc]
        """
        if p==1:
            g.mines=list(set(g.mines).union(set([flat_loc])))
        if p==0:
            g.clear=list(set(g.clear).union(set([flat_loc])))
        """
        if p<minimum:
            minimum=p
            minimum_set=[flat_loc]
        elif p==minimum:
            minimum_set.append(flat_loc)
        
    # select the item wpith minimum prob which has the max number of seen neighbors
    # if 2 ore more such nodes exist, select one with the least number of unknown neighbors (happens only on boundaries of the field.)
    if len(minimum_set):
        max_nbr_count=-1
        max_item=minimum_set[0]
        min_count=9 
        for item in minimum_set:
            item_nbrs=get_neighbors(g.actual_index(item))
            nbrs_intersection_size=len(list(set(item_nbrs).union(set(g.fringe))))
            nbrs_disjoint_size=len(item_nbrs)-nbrs_intersection_size
            if nbrs_intersection_size>max_nbr_count:
                max_nbr_count=nbrs_intersection_size
                max_item=item
                min_count=nbrs_disjoint_size
            elif nbrs_intersection_size==max_nbr_count:
                if nbrs_disjoint_size<=min_count:
                    min_count=nbrs_disjoint_size
                    max_item=item
    
    if adaptive:
        if len(g.explored)>=3:
            expected_mine_count=np.mean([len(c) for c in g.combs])/len(g.combs)
            explored_cell_count=len(g.explored)+len(g.seen_nbrs)
            mine_probability=expected_mine_count/explored_cell_count
            for loc in np.arange(g.dim1*g.dim2):
                if loc not in g.explored and loc not in g.seen_nbrs:
                    g.probs[g.actual_index(loc)]=mine_probability
    

    
    # if the minimum encountered probability is 1, then only mines remain unrevealed.
    if minimum==1:
        #print("-------------------\nMaze successfully solved!!! \n All unexplored cells are expected to be mines.")
        g.next_loc=(-1,-1)
    else:
        g.next_loc=(g.actual_index(max_item)[0], g.actual_index(max_item)[1])

    
    
    