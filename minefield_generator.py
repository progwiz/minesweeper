import numpy as np
import global_vars
import matplotlib.pyplot as plt

#this function generates a new field dim1,dim2 are dimensions of the field, p*dim*dim2 is the number of mines.
def generate_field(dim1,dim2,p=0):
    field= np.full((dim1,dim2), 255, dtype=np.int16)
    mine_count=int(dim1*dim2*p)
    mine_locs=[(int(np.random.choice(dim1)), int(np.random.choice(dim2))) for i in range(mine_count)]
    for x,y in mine_locs:
        field[x,y]= -1
    return field

# this generates a random field for the user to work with
# on running this function, an image of the field is saved as "random-field.png"
def generate_random_field(dim1,dim2,p=0.1):
    field=generate_field(dim1,dim2,p)
    fig,ax=plt.subplots()
    for row in range(dim1):
        for column in range(dim2):
            nbr_mine_count=0
            for dx,dy in [(-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1), (1,0),(1,1)]:
                if -1<row+dx<dim1 and -1<column+dy<dim2:
                    if field[row+dx, column+dy]==-1:
                        nbr_mine_count+=1
            if field[row,column]!=-1:
                field[row,column]=nbr_mine_count
    
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
    field_PIL_img=global_vars.image_from_array(field, random_field=True)
    field_np_arr=np.array(field_PIL_img, dtype=np.uint8)
    for row in range(dim1):
        for column in range(dim2):
            if np.array_equal(field_np_arr[row,column],[0,0,0]):
                field_np_arr[row,column]=[255,255,255]
    ax.imshow(field_np_arr)
    plt.savefig("random-field.png")

if __name__ == "__main__":
    generate_random_field(4,4,0.1)
    