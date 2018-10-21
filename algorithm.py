# this file defines the basic algorithm which is used to find the next node which should be revealed.

# all lists and other data structures are stored in file global_vars 
# all data needed by both the UI and the algorithm are in global_vars
import global_vars as g
import itertools


# this function combines the sets of possible combinations that decides if a vertex can be a mine
def intersect_combinations(combination_set1,combination_set2):
    # locs are the set of nodes that effect the probability of a node being a mine
    # c1, c2 are the combinations of these nodes that can all be mines.
    locs1,c1=combination_set1
    locs2,c2=combination_set2
    locs_inter = list(set(locs1) & set(locs2))
    final_locs = list(set(locs1).union(set(locs2)))
    final_combinations = []
    flag=0
    # find common nodes between the two sets and combine the combinations that contain these nodes.
    for i in range(len(locs_inter),0,-1):
        combinations_i=[]
        locs_inter_combinations=itertools.combinations(locs_inter,i)
        for locs_inter_combination in locs_inter_combinations:
            first_set=[]
            second_set=[]
            c1_temp=[]
            c2_temp=[]
            for combination_no,combination in enumerate(c1):
                if len(list(set(combination) & set(locs_inter_combination))) == i:
                    first_set.append(combination)
                else:
                    c1_temp.append(combination)
            for combination_no,combination in enumerate(c2):
                if len(list(set(combination) & set(locs_inter_combination))) == i:
                    second_set.append(combination)
                else:
                    c2_temp.append(combination)
            for j in first_set:
                for k in second_set:
                    flag=1
                    combinations_i.append(list(set(j).union(set(k))))
            c1=c1_temp
            c2=c2_temp
        final_combinations+=combinations_i
        
    # if flag is 0, the two sets have no combinations with same set of nodes that effect them.
    if not(flag):
        if len(c1)==0: c1=[[]]
        if len(c2)==0: c2=[[]]
    for i in c1:
            for j in c2:
                    union=list(set(i).union(set(j)))
                    if len(union):  final_combinations.append(union)
    return [final_locs, final_combinations]
    
# returns the manhattan distance 
# the distance helps in propogating the changes to probabilities radially outward from the revealed node.
def manhattan_dist(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

# returns location of neighbors of a node.
def get_neighbors(x,y):
    nbrs=[]
    for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        if -1<x+dx<g.dim1 and -1<y+dy<g.dim2:
            nbrs.append((x+dx,y+dy))
    return nbrs

# This function is used to compute the index of the next cell that is to be revealed
# The field itself is stored in g.field variable
# The next location should be updated to g.next_loc
def fetch_next(debug=True):
    prev_loc=g.next_loc
    
    # if the revelaed cell is a mine, game over
    if g.field[prev_loc]==-1:
        return (0,0)

    # change probability of revealed cell being a mine to 0.
    g.probs[prev_loc]=0
    
    # change this value to the node which is not being updated as expected to debug.
    invalid_node=5
    
    # add the revealed cell to list of explored nodes and remove from fringe list, seen neighbors list
    g.explored.append(g.flat_index(prev_loc))
    g.fringe.remove(g.flat_index(prev_loc))
    if g.flat_index(prev_loc) in g.seen_nbrs:
        g.seen_nbrs.remove(g.flat_index(prev_loc))
        
    # update all elements whose combinations depended on the revealed cell
    for location, combination_set in g.combinations.items():
        if g.flat_index(prev_loc) in combination_set[0]:
            combination_set[0].remove(g.flat_index(prev_loc))
            g.combinations[location]=[combination_set[0],[combination for combination in combination_set[1] if g.flat_index(prev_loc) not in combination]]
            location_event_count=len([c for c in g.combinations[location][1] if location in c])
            try:
                g.probs[g.actual_index(location)]=location_event_count/len(combination_set[1])
            except: g.probs[g.actual_index(location)]=0
    
    # get set of unexplored neighbors
    nbrs=get_neighbors(prev_loc[0],prev_loc[1])
    unexplored_nbrs=[g.flat_index(nbr) for nbr in nbrs if g.flat_index(nbr) not in g.explored]

    # add unexplored neighbors to seen and fringe
    g.seen_nbrs= list(set(g.seen_nbrs).union(set(unexplored_nbrs)))
    g.fringe=list(set(g.fringe).union(set(unexplored_nbrs)))
    
    # sort the seen neighbors radially outward.
    g.seen_nbrs=sorted(g.seen_nbrs, key=lambda x:manhattan_dist(prev_loc,g.actual_index(x)))
    
    # add neighbors of neighbors to fringe
    for nbr in unexplored_nbrs:
        nbrs_nbr=get_neighbors(g.actual_index(nbr)[0],g.actual_index(nbr)[1])
        nbrs_nbr=[g.flat_index(n) for n in nbrs_nbr if g.flat_index(n) not in g.explored]
        g.fringe=list(set(g.fringe).union(set(nbrs_nbr)))
    
    #update allowed combinations for neighbors based on the revealed node.
    if debug:   print("currently exploring:", prev_loc)
    new_combination_set=[unexplored_nbrs,list(itertools.combinations(unexplored_nbrs,g.field[prev_loc]))]
    if debug:   print(len(new_combination_set[1]))
    if not(len(new_combination_set[1])):
        new_combination_set=[new_combination_set[0],[[]]]
    if debug:   print(len(new_combination_set[1]))
    for nbr in unexplored_nbrs:
        if debug:
            if nbr==invalid_node:
                print("old combinations for invalid")
                print(g.combinations[nbr])
        g.combinations[nbr]=intersect_combinations(g.combinations[nbr],new_combination_set)
        location_event_count=len([c for c in g.combinations[nbr][1] if nbr in c])
        try:
            g.probs[g.actual_index(nbr)]=location_event_count/len(g.combinations[nbr][1])
        except: g.probs[g.actual_index(nbr)]=0
        if debug:
            if nbr==invalid_node:
                print("mid combinations for invalid")
                print(g.combinations[nbr])
    
    # propogate the changes radially outward.
    for nbr1 in g.seen_nbrs:
        nbr1_nbrs=get_neighbors(g.actual_index(nbr1)[0],g.actual_index(nbr1)[1])
        nbr1_nbrs=[g.flat_index(n) for n in nbr1_nbrs if g.flat_index(n) in g.seen_nbrs]
        for nbr2 in nbr1_nbrs:
            if debug:
                if nbr1==invalid_node:
                    print(nbr2)
            g.combinations[nbr1]=intersect_combinations(g.combinations[nbr1],g.combinations[nbr2])
        location_event_count=len([c for c in g.combinations[nbr1][1] if nbr1 in c])
        try:
            g.probs[g.actual_index(nbr1)]=location_event_count/len(g.combinations[nbr1][1])
        except: g.probs[g.actual_index(nbr1)]=0
        if debug:
            if nbr1==invalid_node:
                print("new combinations for invalid")
                print(g.combinations[nbr1])            
    
    if debug:
        for x in range(g.dim1):
            for y in range(g.dim2):
                print("p",(x,y),": ",g.probs[x,y])
    
    #find node with minimum probability of being a mine, definite mines, definite clear cells
    minimum=1.1
    minimum_set=[]
    for flat_loc in g.fringe:
        actual_loc=g.actual_index(flat_loc)
        p=g.probs[actual_loc]
        if p==1:
            g.mines.append(flat_loc)
        if p<minimum:
            minimum=p
            minimum_set=[flat_loc]
        elif p==minimum:
            minimum_set.append(flat_loc)
    
    # if p=0, add item to clear mines
    if not(minimum):
        g.clear.append(flat_loc)
    
    # select the item with minimum prob which has the max number of seen neighbors
    # if 2 ore more such nodes exist, select one with the least number of unknown neighbors (happens only on boundaries of the field.)
    if len(minimum_set):
        max_nbr_count=-1
        max_item=minimum_set[0]
        min_count=9 
        for item in minimum_set:
            item_nbrs=get_neighbors(g.actual_index(item)[0], g.actual_index(item)[1])
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
    
    # if the minimum encountered probability is 1, then only mines remain unrevealed.
    if minimum==1:
        print("-------------------\nMaze successfully solved!!! \n All unexplored cells are expected to be mines.")
        g.next_loc=(0,0)
        
    if debug:    
        print("seen nbrs:", g.seen_nbrs)
        print("fringe:", g.fringe)
        
    g.next_loc=(g.actual_index(max_item)[0], g.actual_index(max_item)[1])
