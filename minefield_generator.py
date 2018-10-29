import numpy as np
import global_vars

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
def generate_random_field(dim1,dim2,p=0.1, display=True):
    field=generate_field(dim1,dim2,p)
    
    for row in range(dim1):
        for column in range(dim2):
            nbr_mine_count=0
            for dx,dy in [(-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1), (1,0),(1,1)]:
                if -1<row+dx<dim1 and -1<column+dy<dim2:
                    if field[row+dx, column+dy]==-1:
                        nbr_mine_count+=1
            if field[row,column]!=-1:
                field[row,column]=nbr_mine_count
    
    if display:
        global_vars.display_field(field, dim1,dim2)
    return field

if __name__ == "__main__":
    generate_random_field(10,10,0.2)
    