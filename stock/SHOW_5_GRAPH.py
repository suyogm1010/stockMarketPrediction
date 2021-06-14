import tkinter as tk
from PIL import Image , ImageTk
import PIL
# from pandas import DataFrame
# from pandas import Series
# from pandas import concat
# from pandas import read_csv
# from pandas import datetime
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense
# import pandas as pd
# from keras.layers.convolutional import Conv1D, MaxPooling1D
# from keras.layers import Dense, Flatten



def SHOW5():
    text_file = open(r"IMAGE_LIST.txt","r")
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
    load1 =load1.resize((400,300), Image.ANTIALIAS)
    render1 = ImageTk.PhotoImage(load1)
    i1 = tk.Label(window, image = render1)
    i1.image = render1
    i1.place(x=5,y=0)
    i1_n = tk.Label(window,text=str(GRAPH_LIST[0].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i1_n.place(x=5,y=305)
    
    
    load2 = PIL.Image.open(GRAPH_LIST[1])
    load2 =load2.resize((400,300), Image.ANTIALIAS)
    render2 = ImageTk.PhotoImage(load2)
    i2 = tk.Label(window, image = render2)
    i2.image = render2
    i2.place(x=450,y=0)
    i2_n = tk.Label(window,text=str(GRAPH_LIST[1].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i2_n.place(x=450,y=305)
    
    
    load3 = PIL.Image.open(GRAPH_LIST[2])
    load3 =load3.resize((400,300), Image.ANTIALIAS)
    render3 = ImageTk.PhotoImage(load3)
    i3 = tk.Label(window, image = render3)
    i3.image = render3
    i3.place(x=900,y=0)
    i3_n = tk.Label(window,text=str(GRAPH_LIST[2].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i3_n.place(x=900,y=305)
    
    
    load4 = PIL.Image.open(GRAPH_LIST[3])
    load4 =load4.resize((500,300), Image.ANTIALIAS)
    render4 = ImageTk.PhotoImage(load4)
    i4 = tk.Label(window, image = render4)
    i4.image = render4
    i4.place(x=100,y=350)
    i4_n = tk.Label(window,text=str(GRAPH_LIST[3].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i4_n.place(x=100,y=655)
    
    
    load5 = PIL.Image.open(GRAPH_LIST[4])
    load5 =load5.resize((500,300), Image.ANTIALIAS)
    render5 = ImageTk.PhotoImage(load5)
    i5 = tk.Label(window, image = render5)
    i5.image = render5
    i5.place(x=700,y=350)
    i5_n = tk.Label(window,text=str(GRAPH_LIST[4].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i5_n.place(x=700,y=655)
    
    
    
    window.mainloop()
    



    
SHOW5()