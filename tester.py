import numpy as np
import pickle
import os
import algorithm
import global_vars as g
import sys
from time import time
import minefield_generator as mg
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    path="data/"
    os.makedirs(path, exist_ok=True)
    explored_na1=[]
    explored_na2=[]
    explored_na3=[]
    explored_na4=[]
    explored_na5=[]
    explored_a=[]
    success_na1=[]
    success_na2=[]
    success_na3=[]
    success_na4=[]
    success_na5=[]
    success_a=[]
    mine_counts=[]
    final_dict={}
    trial_count=5
    for dim in range(10,11):
        cell_count=dim*dim
        for p in np.arange(0.2,0.21,0.05):
            p_dict={}
            explored_counts_adaptive=[]
            explored_counts_nonadaptive1=[]
            explored_counts_nonadaptive2=[]
            explored_counts_nonadaptive3=[]
            explored_counts_nonadaptive4=[]
            explored_counts_nonadaptive5=[]
            explored_counts_special=[]
            mc=[]
            success_count_adaptive=0
            success_count_nonadaptive1=0
            success_count_nonadaptive2=0
            success_count_nonadaptive3=0
            success_count_nonadaptive4=0
            success_count_nonadaptive5=0
            success_count_special=0
            
            for trials in range(trial_count):
                sys.stdout.write("\r p: "+str(p)+" dim: "+str(dim)+" trial_no: "+str(trials)+"               ")
                explored_len_adaptive,explored_len_nonadaptive1, explored_len_nonadaptive2, explored_len_nonadaptive3, explored_len_nonadaptive4, explored_len_nonadaptive5, explored_len_special=0,0,0,0,0,0,0
                
                flag1,flag2,flag3,flag4,flag5,flaga,flags=0,0,0,0,0,0,0
                while explored_len_adaptive<dim and explored_len_nonadaptive1<dim and explored_len_nonadaptive2<dim and explored_len_nonadaptive3<dim and explored_len_nonadaptive4<dim and explored_len_nonadaptive5<dim and explored_len_special<dim :
                    
                    # generate field and register mine-count
                    field=mg.generate_random_field(dim,dim,p=p,display=False)
                    mine_count=0
                    for x in np.arange(dim):
                        for y in np.arange(dim):
                            if field[x,y]==-1: mine_count+=1 

                    # solve for non adaptive w/ initial p=0.3
                    g.initialize_vals(dim,dim,0.1)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    t=time()
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        g.field[g.next_loc]=field[g.next_loc]
                
                    explored_len_nonadaptive1=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flag1=1
                        
                    # solve for non adaptive w/ initial p=0.3
                    g.initialize_vals(dim,dim,0.2)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        g.field[g.next_loc]=field[g.next_loc]
                    explored_len_nonadaptive2=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flag2=1
                    
                    # solve for non adaptive w/ initial p=0.3
                    g.initialize_vals(dim,dim,0.3)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        g.field[g.next_loc]=field[g.next_loc]
                    explored_len_nonadaptive3=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flag3=1
                        
                    # solve for non adaptive w/ initial p=0.4
                    g.initialize_vals(dim,dim,0.4)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        g.field[g.next_loc]=field[g.next_loc]
                    explored_len_nonadaptive4=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flag4=1
                    
                    # solve for non adaptive w/ initial p=0.5
                    g.initialize_vals(dim,dim)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        g.field[g.next_loc]=field[g.next_loc]
                    explored_len_nonadaptive5=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        g.display_field(field,10,10,"random-field2.png")
                        flag5=1
                    
                    # solve for adaptive
                    g.initialize_vals(dim,dim)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        algorithm.fetch_next(adaptive=True)
                        g.field[g.next_loc]=field[g.next_loc]
                    explored_len_adaptive=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flaga=1
                        
                    # solve for nonadaptive special case w/ initial p=0.5
                    g.initialize_vals(dim,dim)
                    g.generate_field(dim,dim)
                    g.field[g.next_loc]=field[g.next_loc]
                    while not(np.array_equal(g.next_loc,(-1,-1))) and g.field[g.next_loc]!=-1:
                        #print(g.next_loc)
                        algorithm.fetch_next(adaptive=False)
                        val=np.random.uniform()
                        if val>0.2:
                            g.field[g.next_loc]=field[g.next_loc]
                        else:
                            g.field[g.next_loc]= -2
                    explored_len_special=len(g.explored)
                    if np.array_equal(g.next_loc,(-1,-1)):
                        flags=1
                #save values
                success_count_nonadaptive1+=flag1
                success_count_nonadaptive2+=flag2
                success_count_nonadaptive3+=flag3
                success_count_nonadaptive4+=flag4
                success_count_nonadaptive5+=flag5
                success_count_adaptive+=flaga
                success_count_special+=flags
                mc.append(mine_count)
                explored_counts_adaptive.append(explored_len_adaptive)
                explored_counts_nonadaptive1.append(explored_len_nonadaptive1)
                explored_counts_nonadaptive2.append(explored_len_nonadaptive2)
                explored_counts_nonadaptive3.append(explored_len_nonadaptive3)
                explored_counts_nonadaptive4.append(explored_len_nonadaptive4)
                explored_counts_nonadaptive5.append(explored_len_nonadaptive5)
                explored_counts_special.append(explored_len_special)
            
            # calculate averages
            avg_mine_count=int(np.mean(mc))
            mine_counts.append(avg_mine_count)
            
            avg_explored_count_adaptive=np.mean(explored_counts_adaptive)
            avg_explored_count_nonadaptive1=np.mean(explored_counts_nonadaptive1)
            avg_explored_count_nonadaptive2=np.mean(explored_counts_nonadaptive2)
            avg_explored_count_nonadaptive3=np.mean(explored_counts_nonadaptive3)
            avg_explored_count_nonadaptive4=np.mean(explored_counts_nonadaptive4)
            avg_explored_count_nonadaptive5=np.mean(explored_counts_nonadaptive5)
            avg_explored_count_special=np.mean(explored_counts_special)
            
            
            explored_na1.append(avg_explored_count_nonadaptive1)
            explored_na2.append(avg_explored_count_nonadaptive2)
            explored_na3.append(avg_explored_count_nonadaptive3)
            explored_na4.append(avg_explored_count_nonadaptive4)
            explored_na5.append(avg_explored_count_nonadaptive5)
            explored_a.append(avg_explored_count_adaptive)
            
            success_na1.append(success_count_nonadaptive1/trial_count)
            success_na2.append(success_count_nonadaptive2/trial_count)
            success_na3.append(success_count_nonadaptive3/trial_count)
            success_na4.append(success_count_nonadaptive4/trial_count)
            success_na5.append(success_count_nonadaptive5/trial_count)
            success_a.append(success_count_adaptive/trial_count)
            # add to pickle file
            #p_dict[p]=(mine_counts,{"adaptive":(avg_explored_count_adaptive,success_count_adaptive),"nonadaptive":(avg_explored_count_nonadaptive, success_count_nonadaptive)})
            
            # add to txt file
            print(success_count_nonadaptive1)
            with open(path+"trials5.txt", "a+") as f:
                f.write("\n\nDIM: "+str(dim)+" X "+str(dim)+"  P: "+str(p)+ " Trials: "+str(trial_count) +"  Mine count: "+str(avg_mine_count))
                f.write("\nNonadaptive p=0.1 Explored : "+str(avg_explored_count_nonadaptive1)+"  Success : "+str(success_count_nonadaptive1/trial_count))
                f.write("\nNonadaptive p=0.2 Explored : "+str(avg_explored_count_nonadaptive2)+"  Success : "+str(success_count_nonadaptive2/trial_count))
                f.write("\nNonadaptive p=0.3 Explored : "+str(avg_explored_count_nonadaptive3)+"  Success : "+str(success_count_nonadaptive3/trial_count))
                f.write("\nNonadaptive p=0.4 Explored : "+str(avg_explored_count_nonadaptive4)+"  Success : "+str(success_count_nonadaptive4/trial_count))
                f.write("\nNonadaptive p=0.5 Explored : "+str(avg_explored_count_nonadaptive5)+"  Success : "+str(success_count_nonadaptive5/trial_count))

                f.write("\nAdaptive Explored : "+str(avg_explored_count_adaptive)+"  Success : "+str(success_count_adaptive/trial_count))
                f.write("\nSpecial case Explored : "+str(avg_explored_count_special)+"  Success : "+str(success_count_special/trial_count))
        
        final_dict[dim]=p
    
    print("done")
    
    plt.figure()
    plt.title("success rate on 8x8 board")
    plt.plot(mine_counts,success_na1,color="blue")
    plt.plot(mine_counts,success_na2,color="red")
    plt.plot(mine_counts,success_na3,color="green")
    plt.plot(mine_counts,success_na4,color="yellow")
    plt.plot(mine_counts,success_na5,color="purple")
    plt.plot(mine_counts,success_a, color="black")
    plt.xlabel("Number of mines")
    plt.ylabel("Success rate")
    plt.savefig("Success rate.png")
    plt.legend(["p0=0.1","p0=0.2","p0=0.3","p0=0.4","p0=0.5","Adaptive"], loc="upper right")
    plt.ylim([0,1])
    
    
    plt.figure()
    plt.title("Avg number of expanded nodes on 8x8 board")
    plt.plot(mine_counts,explored_na1, color="blue")
    plt.plot(mine_counts,explored_na2, color="red")
    plt.plot(mine_counts,explored_na3, color="green")
    plt.plot(mine_counts,explored_na4,color="yellow")
    plt.plot(mine_counts,explored_na5,color="purple")
    plt.plot(mine_counts,explored_a,color="black")
    plt.xlabel("Number of mines")
    plt.ylabel("Number of expanded nodes")
    plt.savefig("expanded nodes.png")
    plt.legend(["p0=0.1","p0=0.2","p0=0.3","p0=0.4","p0=0.5","Adaptive"], loc="upper right")
    plt.ylim([0,64])   
    
    #save pickle file
    with open(path+"trials.pickle","wb+") as f:
        pickle.dump(final_dict,f)
            
        
                
            
                
