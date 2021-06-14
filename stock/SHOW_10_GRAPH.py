import tkinter as tk
from PIL import Image , ImageTk
import PIL

def SHOW10():
    text_file = open(r"IMAGE_LIST_10.txt","r")
    GRAPH_LIST = text_file.readline()
    
    GRAPH_LIST = GRAPH_LIST.split("'")
    
    GRAPH_LIST.remove(', ')
    GRAPH_LIST.remove("[")
    GRAPH_LIST.remove("]")
    GRAPH_LIST = list(GRAPH_LIST)
    GRAPH_LIST = set(GRAPH_LIST)
    GRAPH_LIST = list(GRAPH_LIST)
    GRAPH_LIST.remove(', ')
    
    print("\nY is : ",GRAPH_LIST)
    
    
    window = tk.Tk()
    w,h = window.winfo_screenwidth() , window.winfo_screenheight()
    window.geometry("%dx%d+0+0"%(w,h))
    window.configure(background="cyan")
    
    load1 = PIL.Image.open(GRAPH_LIST[0])
    load1 =load1.resize((275,300), Image.ANTIALIAS)
    render1 = ImageTk.PhotoImage(load1)
    i1 = tk.Label(window, image = render1)
    i1.image = render1
    i1.place(x=0,y=0)
    i1_n = tk.Label(window,text=str(GRAPH_LIST[0].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i1_n.place(x=0,y=305)
    
    
    load2 = PIL.Image.open(GRAPH_LIST[1])
    load2 =load2.resize((275,300), Image.ANTIALIAS)
    render2 = ImageTk.PhotoImage(load2)
    i2 = tk.Label(window, image = render2)
    i2.image = render2
    i2.place(x=280,y=0)
    i2_n = tk.Label(window,text=str(GRAPH_LIST[1].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i2_n.place(x=280,y=305)
    
    
    load3 = PIL.Image.open(GRAPH_LIST[1])
    load3 =load3.resize((275,300), Image.ANTIALIAS)
    render3 = ImageTk.PhotoImage(load3)
    i3 = tk.Label(window, image = render3)
    i3.image = render3
    i3.place(x=560,y=0)
    i3_n = tk.Label(window,text=str(GRAPH_LIST[1].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i3_n.place(x=560,y=305)
    
    
    load4 = PIL.Image.open(GRAPH_LIST[2])
    load4 =load4.resize((275,300), Image.ANTIALIAS)
    render4 = ImageTk.PhotoImage(load4)
    i4 = tk.Label(window, image = render4)
    i4.image = render4
    i4.place(x=840,y=0)
    i4_n = tk.Label(window,text=str(GRAPH_LIST[2].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i4_n.place(x=840,y=305)
    
    
    load5 = PIL.Image.open(GRAPH_LIST[3])
    load5 =load5.resize((275,300), Image.ANTIALIAS)
    render5 = ImageTk.PhotoImage(load5)
    i5 = tk.Label(window, image = render5)
    i5.image = render5
    i5.place(x=1120,y=0)
    i5_n = tk.Label(window,text=str(GRAPH_LIST[3].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i5_n.place(x=1100,y=305)
    
    
    
    load6 = PIL.Image.open(GRAPH_LIST[4])
    load6 =load1.resize((275,300), Image.ANTIALIAS)
    render6 = ImageTk.PhotoImage(load6)
    i6 = tk.Label(window, image = render6)
    i6.image = render6
    i6.place(x=0,y=350)
    i6_n = tk.Label(window,text=str(GRAPH_LIST[4].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i6_n.place(x=0,y=655)
    
    
    load7 = PIL.Image.open(GRAPH_LIST[6])
    load7 =load2.resize((275,300), Image.ANTIALIAS)
    render7 = ImageTk.PhotoImage(load7)
    i7 = tk.Label(window, image = render7)
    i7.image = render7
    i7.place(x=280,y=350)
    i7_n = tk.Label(window,text=str(GRAPH_LIST[6].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i7_n.place(x=280,y=655)
    
    
    load8 = PIL.Image.open(GRAPH_LIST[5])
    load8 =load3.resize((275,300), Image.ANTIALIAS)
    render8 = ImageTk.PhotoImage(load8)
    i8 = tk.Label(window, image = render8)
    i8.image = render8
    i8.place(x=560,y=350)
    i8_n = tk.Label(window,text=str(GRAPH_LIST[5].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i8_n.place(x=560,y=655)
    
    
    load9 = PIL.Image.open(GRAPH_LIST[6])
    load9 =load4.resize((275,300), Image.ANTIALIAS)
    render9 = ImageTk.PhotoImage(load9)
    i9 = tk.Label(window, image = render9)
    i9.image = render9
    i9.place(x=840,y=350)
    i9_n = tk.Label(window,text=str(GRAPH_LIST[6].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i9_n.place(x=840,y=655)
    
    
    load10 = PIL.Image.open(GRAPH_LIST[7])
    load10 =load5.resize((275,300), Image.ANTIALIAS)
    render10 = ImageTk.PhotoImage(load10)
    i10 = tk.Label(window, image = render10)
    i10.image = render10
    i10.place(x=1120,y=350)
    i10_n = tk.Label(window,text=str(GRAPH_LIST[7].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i10_n.place(x=1100,y=655)
    
    window.mainloop()

SHOW10()