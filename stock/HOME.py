import tkinter as tk
from math import sqrt
from matplotlib import pyplot
from numpy import array
from PIL import ImageTk , Image
import PIL
from subprocess import call
def OPEN():
    root = tk.Tk()
    root.title("Stock Market Prediction")
    
    
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    
    
    load_bg = PIL.Image.open(r"bg1.jpg")
    load_bg = load_bg.resize((w,h))
    render_bg = ImageTk.PhotoImage(load_bg)
    bg = tk.Label(root, image = render_bg , height=h, width= w)
    bg.image = render_bg
    bg.place(x=0,y=0)
    
    home = tk.Label(root,text="----- Home Page -----",bg='black',fg='white',width=70,font=('Times',30,'italic'))
    home.place(x=0,y=0)
    
    def PRICE():
        call(['python','CNN_FILE.py'])
    
    def SENTIMENT():
        
        root.destroy()
        import Stock_Home
        Stock_Home.run()
    
    
    button1 = tk.Button(root, text = "View Price" ,command = PRICE,font=("Tempus Sans ITC", 15,"bold"),width= 20,height =2,bg ="red",fg="white")
    button1.place(x=400,y=300)
    
    button2 = tk.Button(root, text = "View Sentiment" ,command = SENTIMENT,font=("Tempus Sans ITC", 15,"bold"),width= 20,height =2,bg ="black",fg="white")
    button2.place(x=850,y=300)
    
    root.mainloop()
OPEN()