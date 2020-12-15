import os

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

size = 1000
image_width = 1440
image_height = 720
pos_x = 0
pos_y = 0

def reference_click():
    global image_width
    global image_height
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    ref_image_path.set(filepath)
    im_next = Image.open(filepath)
    image_width = im_next.width
    image_height = im_next.height
    im_next = im_next.resize((int(size*0.9),int(size*0.45)))
    im_next = ImageTk.PhotoImage(im_next)
    canvas.photo=im_next
    image_on_canvas = canvas.create_image(0,0,image=im_next,anchor=tk.NW)

def reference_click2():
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    ref_csv_path.set(filepath)

def mouse_click(event):
    global pos_x
    global pos_y
    canvas.coords(circle_on_canvas, event.x-5,event.y-5,event.x+5,event.y+5)
    canvas.tag_raise(circle_on_canvas)
    x = int((event.x/(size*0.9)) * image_width)
    y = int((event.y/(size*0.45)) * image_height)
    print(x)
    print(y)
    pos_x = x
    pos_y = y

def add_vanish_point():
    csv_path = ref_csv_path.get()
    image_path = ref_image_path.get()
    image_num = image_path.split("/")[-1].split(".")[0]
    with open(csv_path,"a") as fp:
        print(image_num+","+str(pos_y)+","+str(pos_x),file=fp)
    print("added point")


if __name__=="__main__":
    window = tk.Tk()
    window.title("Vanish Point Annotator")
    window.geometry(str(int(size))+"x"+str(int(size*0.6)))

    image_frame = tk.Frame(window,width=int(size*0.9),height=int(size*0.45),bg='red')
    reference_image_frame = tk.Frame(window,width=int(size*0.9),height=int(size*0.04),bg='blue')
    reference_image_button = tk.Button(reference_image_frame,text="ref image path",command=reference_click)
    reference_csv_frame = tk.Frame(window,width=int(size*0.9),height=int(size*0.04),bg='yellow')
    reference_csv_button = tk.Button(reference_csv_frame,text='ref csv path',command=reference_click2)
    add_button = tk.Button(window,text="add vanish point",command=add_vanish_point)

    image_frame.pack(side="top")
    reference_image_frame.pack(side="top")
    reference_image_button.pack(side="right")
    reference_csv_frame.pack(side="top")
    reference_csv_button.pack(side="right")
    add_button.pack(side="bottom")

    ref_image_path = tk.StringVar()
    ref_csv_path = tk.StringVar()

    image_label = tk.Label(reference_image_frame,textvariable=ref_image_path)
    image_label.pack(side="left")
    reference_label = tk.Label(reference_csv_frame,textvariable=ref_csv_path)
    reference_label.pack(side="left")

    canvas = tk.Canvas(master=image_frame,bg="black",width=int(size*0.9),height=int(size*0.45))
    canvas.place(x=0,y=0)
    circle_on_canvas = canvas.create_oval(0,0,15,15,fill = '#ff00ff')
    canvas.bind("<Button-1>",mouse_click)
    
    window.mainloop()