import numpy as np, matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import global_vars
import algorithm

def GUI(dim1, dim2):
    
    #write val for array index arr_x, arr_y
    def write_on_canvas(arr_x, arr_y, val):
        global numbers
        ver_ratio,hor_ratio = image.size[1]/global_vars.dim1, image.size[0]/global_vars.dim2
        write_ver,write_hor = arr_x*ver_ratio+ver_ratio/2, arr_y*hor_ratio+hor_ratio/2
        if int(val) not in [-1,0]:
            no=canvas.create_text(write_hor, write_ver, font = ("Purisa", int(0.5*image.size[1]/global_vars.dim1)),text=val, fill = "white")
            numbers.append([arr_x, arr_y, val, no])
            
    # event handler for button click
    def button_click():
        global image
        global curr_index
        green_box=False
        textbox_val=int(tb.get())
        global_vars.field[global_vars.next_loc]=textbox_val
        write_on_canvas(global_vars.next_loc[0], global_vars.next_loc[1], str(textbox_val)) 
        algorithm.fetch_next()
        if np.array_equal(global_vars.next_loc, (-1,-1)):
            canvas.create_text(image.size[0]/2, image.size[1]/2, font = ("Purisa", int(0.3*image.size[1])),text="SUCCESS!", fill = "blue")
            green_box=True
            for loc in np.arange(global_vars.dim1*global_vars.dim2):
                if loc not in global_vars.explored:
                    global_vars.field[global_vars.actual_index(loc)]=99
                
        if textbox_val == -1:
            green_box=True
            canvas.create_text(image.size[0]/2, image.size[1]/2, font = ("Purisa", int(0.3*image.size[1])),text="GAME\nOVER", fill = "red")
        image=global_vars.image_from_array(global_vars.field, green_box) 
        redraw_img()
        curr_index.set("Current Mine Field index: row = "+str(global_vars.next_loc[0])+" column="+str(global_vars.next_loc[1]))

        global count
        count+=1
        
        canvas.update()
        x=root.winfo_rootx()+canvas.winfo_x()
        y=root.winfo_rooty()+canvas.winfo_y()
        x1=x+canvas.winfo_width()
        y1=y+canvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("play-by-play/"+str(count)+".png")
        
    # draw lines on canvas
    def redraw_lines():
        global lines
        for line in lines:
            canvas.delete(line)
        lines=[]
        for i in np.arange(global_vars.dim2):
            coords=i*image.size[0]/global_vars.dim2,0,i*image.size[0]/global_vars.dim2, image.size[1]
            lines.append(canvas.create_line(coords))
        for i in np.arange(global_vars.dim1):
            coords=0,i*image.size[1]/global_vars.dim1,image.size[0],i*image.size[1]/global_vars.dim1
            lines.append(canvas.create_line(coords))
        canvas.update()
    
    def redraw_img():
        global image
        image=image.resize((canvas.winfo_width(), canvas.winfo_height()))
        photo.paste(image)
            
    # needed for basic functionality of the UI
    def resize_image(event= None):
        canvas.update()
        
        redraw_img()
        global numbers
        redraw_lines()
        numbers_copy=numbers.copy()
        for number_no,number in enumerate(numbers_copy):
            canvas.delete(number[3])
            write_on_canvas(number[0],number[1],number[2])
        try:
            numbers=numbers[len(numbers)/2:]
        except: pass

    global_vars.initialize_vals(dim1,dim2)
    
    # basic UI elements placement
    root=Tk()
    Grid.rowconfigure(root, 0, weight=20)
    Grid.rowconfigure(root, 1, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 1, weight=2)
    global image, lines, numbers, curr_index
    lines=[]
    numbers=[]
    curr_index=StringVar()
    global count
    count=0
    
    # create image from minefield array
    global_vars.generate_field(global_vars.dim1,global_vars.dim2)
    # add a canvas to the UI to draw the image on
    canvas=Canvas(root)
    canvas.grid(row=0, column=0, columnspan=3, sticky=N+S+W+E)
    canvas.bind('<Configure>', resize_image)
    # draw image on canvas
    image=global_vars.image_from_array(global_vars.field)
    image=image.resize((int(root.winfo_screenwidth()), int(root.winfo_screenheight())))
    photo=ImageTk.PhotoImage(image)
    canvas.create_image(0,0,image=photo, anchor=NW)
    photo.paste(image)
    canvas.update()
    image=image.resize((canvas.winfo_width(), canvas.winfo_height()))
    photo.paste(image)
    #draw lines for grid
    redraw_lines()

    # display current minefield/array index on the bottom left of UI
    curr_index.set("Current Minefield cell index: row = "+str(global_vars.next_loc[0])+" column= "+ str(global_vars.next_loc[1]))
    curr_index_label=Label(root, textvariable=curr_index)
    curr_index_label.grid(row=1, column=0, stick=N+S+W+E)

    # add the text box 
    mine_value=Frame(root)
    mine_value.grid(row=1,column=1,sticky=N+S+W+E)  
    label = Label(mine_value, text="| Enter number of mines around the cell (-1 if it is a mine) : ")
    label.pack( side = LEFT)
    tb = Entry(mine_value)
    tb.pack(side = LEFT)
    
    # add the button
    mine_value_btn=Button(mine_value, text="Return response", command=button_click)
    mine_value_btn.pack(side=LEFT)

    #start the GUI and its event handlers
    print("\n\n----------------")
    print ("GUI STARTED")
    

    root.mainloop()