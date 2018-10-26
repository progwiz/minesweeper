import numpy as np
import minefield_generator
from PIL import Image
import matplotlib.pyplot as plt

#universal constants
global dim1,dim2,p,next_loc

#all datastructures used by algorithm. All the datastructures contain flat indices of nodes.
global probs,seen_nbrs,fringe,explored,clear,mines, combs, locs, parent_dict, child_dict

# this function computes the flat index of a cell, i.e. x*dim1+y, for easier processing
def flat_index(index):
    x,y=index
    return x*dim1+y

# this function returns the actual 2D index from the flat index
def actual_index(flat_index):
    x=int(flat_index/dim1)
    y=flat_index-x*dim1
    return (x,y)

# this function runs right after starting the UI and initializes all the variables for UI iand algorithm.
def initialize_vals(d1,d2, p= 0.5):
    # universal variable for dimensions of the minefield
    global dim1,dim2
    dim1,dim2=d1,d2
    
    # universal variable for next cell to be revealed
    global next_loc
    next_loc=(int(dim1/2),int(dim2/2))
    
    global probs, seen_nbrs, fringe, explored, clear, mines, combs, locs, parent_dict, child_dict
    probs=np.full((dim1,dim2), p)
    
    fi=flat_index(next_loc)
    seen_nbrs=[fi]
    fringe=[fi]
    explored=[]
    locs=[]
    combs=[[]]
    parent_dict={actual_index(i):[] for i in np.arange(dim1*dim2)}
    child_dict={actual_index(i):[] for i in np.arange(dim1*dim2)}
    
    global clear, mines
    clear=[]
    mines=[]

# This generates a field for the UI
def generate_field(dim1,dim2,p=0):
    global field
    field= minefield_generator.generate_field(dim1,dim2,p) 
    
# create PIL image from numpy array
# This function is used by the UI
# random_field is True when this function is called from the random field generator
def image_from_array(arr, random_field=False):
    img=np.full((arr.shape[0],arr.shape[1],3),255, dtype=np.uint8)
    for row in np.arange(arr.shape[0]):
        for column in np.arange(arr.shape[1]):
            if arr[row,column] == 255:
                img[row, column] = [255,255,255]
            elif arr[row, column] == -1:
                img[row, column] = [255, 0, 0]
            elif arr[row,column] == 99:
                img[row,column] = [0,255,0]
            else:
                img[row, column] = [0, 0, 0]
    if not(random_field):
        img[next_loc[0],next_loc[1]]=[0,255,0]
    img=Image.fromarray(img,"RGB")
    return img


# this function displays the minefield and saves the picture with the name
    
def display_field(field, dim1, dim2,filename="random-field.png"):
    fig,ax=plt.subplots()
    for row in range(dim1):
        for column in range(dim2):
            if field[row,column]!=0 and field[row,column]!=-1:
                ax.text(column, row, str(field[row,column]), va='center', ha='center')
    ax.set_xlim(-0.5,dim2-0.5)
    ax.set_ylim(-0.5,dim1-0.5)
    ax.set_xticks(np.arange(-0.5,dim2,1))
    ax.set_yticks(np.arange(-0.5,dim1,1))
    ax.set_xticklabels(np.arange(0,dim2))
    ax.set_yticklabels(np.arange(0,dim1))
    ax.grid()
    plt.gca().invert_yaxis()
    field_PIL_img=image_from_array(field, random_field=True)
    field_np_arr=np.array(field_PIL_img, dtype=np.uint8)
    for row in range(dim1):
        for column in range(dim2):
            if np.array_equal(field_np_arr[row,column],[0,0,0]):
                field_np_arr[row,column]=[255,255,255]
    ax.imshow(field_np_arr)
    plt.savefig(filename)