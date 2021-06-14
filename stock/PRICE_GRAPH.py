from tkinter import * # for GUI
import tkinter as tk # For alias
import PIL.Image # to display image on tkinter
global fn # Global variable

global twit_sel # global variable
from PIL import ImageTk , Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer # Import function from library

def Home():
    window=tk.Tk()
    window.title("Sentiment Graph Per Company")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.configure(background="black")
    
    
    load1 = Image.open(r"CSV/INFY.png")
    load1 = load1.resize((200,200))
    render1 = ImageTk.PhotoImage(load1)
    i1 = tk.Label(window, image = render1,fg="white" , height=170, width= 170)
    i1.place(x=0,y=0)
    i1_n = tk.Label(window,text="@Infosys",fg="black" , height=1, width= 10)
    i1_n.place(x=0,y=180)
    
    
    load2 = PIL.Image.open(r"CSV/BHEL.png")
    load2 = load2.resize((200,200))
    render2 = ImageTk.PhotoImage(load2)
    i2 = tk.Label(window, image = render2 , height=170, width= 170)
    i2.place(x=190,y=0)
    i1_n = tk.Label(window,text="@BHEL",fg="black" , height=1, width= 24)
    i1_n.place(x=190,y=180)
    
    load3 = PIL.Image.open(r"CSV/M&M.png")
    load3 = load3.resize((200,200))
    render3 = ImageTk.PhotoImage(load3)
    i3 = tk.Label(window, image = render3 , height=170, width= 170)
    i3.place(x=380,y=0)
    i1_n = tk.Label(window,text="@M&M",fg="black" , height=1, width= 10)
    i1_n.place(x=380,y=180)
    
    load4 = PIL.Image.open(r"CSV/MINDTREE.png")
    load4 = load4.resize((200,200))
    render4 = ImageTk.PhotoImage(load4)
    i4 = tk.Label(window, image = render4 , height=170, width= 170)
    i4.place(x=570,y=0)
    i1_n = tk.Label(window,text="@MindTree",fg="black" , height=1, width= 10)
    i1_n.place(x=570,y=180)
    
    load5 = PIL.Image.open(r"CSV/HDFC.png")
    load5 = load5.resize((200,200))
    render5 = ImageTk.PhotoImage(load5)
    i5 = tk.Label(window, image = render5 , height=170, width= 170)
    i5.place(x=760,y=0)
    i1_n = tk.Label(window,text="@HDFC_Bank",fg="black" , height=1, width= 15)
    i1_n.place(x=760,y=180)
    
    load6 = PIL.Image.open(r"CSV/SBIN.png")
    load6 = load6.resize((200,200))
    render6 = ImageTk.PhotoImage(load6)
    i6 = tk.Label(window, image = render6 , height=170, width= 170)
    i6.place(x=950,y=0)
    i1_n = tk.Label(window,text="@TheOfficialSBI",fg="black" , height=1, width= 15)
    i1_n.place(x=950,y=180)
    
    load7 = PIL.Image.open(r"CSV/BANKBARODA.png")
    load7 = load7.resize((200,200))
    render7 = ImageTk.PhotoImage(load7)
    i7 = tk.Label(window, image = render7 , height=170, width= 170)
    i7.place(x=1140,y=0)
    i1_n = tk.Label(window,text="@bankofbaroda",fg="black" , height=1, width= 15)
    i1_n.place(x=1140,y=180)
    
    load8 = PIL.Image.open(r"CSV/CANBK.png")
    load8 = load8.resize((200,200))
    render8 = ImageTk.PhotoImage(load8)
    i8 = tk.Label(window, image = render8 , height=170, width= 170)
    i8.place(x=0,y=210)
    i1_n = tk.Label(window,text="@canarabank",fg="black" , height=1, width= 15)
    i1_n.place(x=0,y=390)
    
    load10 = PIL.Image.open(r"CSV/TVSMOTOR.png")
    load10 = load10.resize((200,200))
    render10 = ImageTk.PhotoImage(load10)
    i10 = tk.Label(window, image = render10 , height=170, width= 170)
    i10.place(x=190,y=210)
    i1_n = tk.Label(window,text="@tvsmotorcompany",fg="black" , height=1, width= 15)
    i1_n.place(x=190,y=390)
    
    # load11 = PIL.Image.open(r"E:\stock\stock\stockE\CSV\MARUTI.png")
    # load11 = load11.resize((200,200))
    # render11 = ImageTk.PhotoImage(load11)
    # i11 = tk.Label(window, image = render11 , height=170, width= 170)
    # i11.place(x=570,y=210)
    # i1_n = tk.Label(window,text="@Maruti_Corp",fg="black" , height=1, width= 15)
    # i1_n.place(x=570,y=390)
    
    load12 = PIL.Image.open(r"CSV/M&M.png")
    load12 = load12.resize((200,200))
    render12 = ImageTk.PhotoImage(load12)
    i12 = tk.Label(window, image = render12 , height=170, width= 170)
    i12.place(x=380,y=210)
    i1_n = tk.Label(window,text="@Mahindra_Auto",fg="black" , height=1, width= 15)
    i1_n.place(x=380,y=390)
    
    load13 = PIL.Image.open(r"CSV/ABBOTINDIA.png")
    load13 = load13.resize((200,200))
    render13 = ImageTk.PhotoImage(load13)
    i13 = tk.Label(window, image = render13 , height=170, width= 170)
    i13.place(x=570,y=210)
    i1_n = tk.Label(window,text="@AbbottNews",fg="black" , height=1, width= 15)
    i1_n.place(x=570,y=390)
    
    load14 = PIL.Image.open(r"CSV/SANOFI.png")
    load14 = load14.resize((200,200))
    render14 = ImageTk.PhotoImage(load14)
    i14 = tk.Label(window, image = render14 , height=170, width= 170)
    i14.place(x=760,y=210)
    i1_n = tk.Label(window,text="@sanofi",fg="black" , height=1, width= 10)
    i1_n.place(x=760,y=390)
    
    load16 = PIL.Image.open(r"CSV/PFIZER.png")
    load16 = load16.resize((200,200))
    render16 = ImageTk.PhotoImage(load16)
    i16 = tk.Label(window, image = render16 , height=170, width= 170)
    i16.place(x=950,y=210)
    i1_n = tk.Label(window,text="@pfizer",fg="black" , height=1, width= 10)
    i1_n.place(x=950,y=390)
    
    load17 = PIL.Image.open(r"CSV/KEC.png")
    load17 = load17.resize((200,200))
    render17 = ImageTk.PhotoImage(load17)
    i17 = tk.Label(window, image = render17 , height=170, width= 170)
    i17.place(x=1140,y=210)   
    i1_n = tk.Label(window,text="@KEC_Intl",fg="black" , height=1, width= 10)
    i1_n.place(x=1140,y=390)
    
    
    
    window.mainloop()
Home()