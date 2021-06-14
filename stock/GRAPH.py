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
    #itemsforlistbox = ['@Infosys', '@TCS', '@LTI_Global', '@Mindtree_Ltd','@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@canarabank','@bajaj_ltd','@tvsmotorcompany','@Maruti_Corp','@Mahindra_Auto','@AbbottNews','@sanofi','@Alkem_Lab','@pfizer','@KEC_Intl']      
    
    load1 = Image.open(r"Graphs/@Infosys.png")
    load1 = load1.resize((200,200))
    render1 = ImageTk.PhotoImage(load1)
    i1 = tk.Label(window, image = render1,fg="white" , height=170, width= 170)
    i1.place(x=0,y=0)
    i1_n = tk.Label(window,text="@Infosys",fg="black" , height=1, width= 10)
    i1_n.place(x=0,y=180)
    
    
    load2 = PIL.Image.open(r"Graphs/@TCS.png")
    load2 = load2.resize((200,200))
    render2 = ImageTk.PhotoImage(load2)
    i2 = tk.Label(window, image = render2 , height=170, width= 170)
    i2.place(x=190,y=0)
    i1_n = tk.Label(window,text="@TCS",fg="black" , height=1, width= 24)
    i1_n.place(x=190,y=180)
    
    load3 = PIL.Image.open(r"Graphs/@LTI_Global.png")
    load3 = load3.resize((200,200))
    render3 = ImageTk.PhotoImage(load3)
    i3 = tk.Label(window, image = render3 , height=170, width= 170)
    i3.place(x=380,y=0)
    i1_n = tk.Label(window,text="@LTI_Global",fg="black" , height=1, width= 10)
    i1_n.place(x=380,y=180)
    
    load4 = PIL.Image.open(r"Graphs/@Mindtree_Ltd.png")
    load4 = load4.resize((200,200))
    render4 = ImageTk.PhotoImage(load4)
    i4 = tk.Label(window, image = render4 , height=170, width= 170)
    i4.place(x=570,y=0)
    i1_n = tk.Label(window,text="@MindTree",fg="black" , height=1, width= 10)
    i1_n.place(x=570,y=180)
    
    load5 = PIL.Image.open(r"Graphs/@HDFC_Bank.png")
    load5 = load5.resize((200,200))
    render5 = ImageTk.PhotoImage(load5)
    i5 = tk.Label(window, image = render5 , height=170, width= 170)
    i5.place(x=760,y=0)
    i1_n = tk.Label(window,text="@HDFC_Bank",fg="black" , height=1, width= 15)
    i1_n.place(x=760,y=180)
    
    load6 = PIL.Image.open(r"Graphs/@TheOfficialSBI.png")
    load6 = load6.resize((200,200))
    render6 = ImageTk.PhotoImage(load6)
    i6 = tk.Label(window, image = render6 , height=170, width= 170)
    i6.place(x=950,y=0)
    i1_n = tk.Label(window,text="@TheOfficialSBI",fg="black" , height=1, width= 15)
    i1_n.place(x=950,y=180)
    
    load7 = PIL.Image.open(r"Graphs/@bankofbaroda.png")
    load7 = load7.resize((200,200))
    render7 = ImageTk.PhotoImage(load7)
    i7 = tk.Label(window, image = render7 , height=170, width= 170)
    i7.place(x=1140,y=0)
    i1_n = tk.Label(window,text="@bankofbaroda",fg="black" , height=1, width= 15)
    i1_n.place(x=1140,y=180)
    
    load8 = PIL.Image.open(r"Graphs/@canarabank.png")
    load8 = load8.resize((200,200))
    render8 = ImageTk.PhotoImage(load8)
    i8 = tk.Label(window, image = render8 , height=170, width= 170)
    i8.place(x=0,y=210)
    i1_n = tk.Label(window,text="@canarabank",fg="black" , height=1, width= 15)
    i1_n.place(x=0,y=390)
    
    load9 = PIL.Image.open(r"Graphs/@bajaj_ltd.png")
    load9 = load9.resize((200,200))
    render9 = ImageTk.PhotoImage(load9)
    i9 = tk.Label(window, image = render9 , height=170, width= 170)
    i9.place(x=190,y=210)
    i1_n = tk.Label(window,text="@bajaj_ltd",fg="black" , height=1, width= 15)
    i1_n.place(x=190,y=390)
    
    load10 = PIL.Image.open(r"Graphs/@tvsmotorcompany.png")
    load10 = load10.resize((200,200))
    render10 = ImageTk.PhotoImage(load10)
    i10 = tk.Label(window, image = render10 , height=170, width= 170)
    i10.place(x=380,y=210)
    i1_n = tk.Label(window,text="@tvsmotorcompany",fg="black" , height=1, width= 15)
    i1_n.place(x=380,y=390)
    
    load11 = PIL.Image.open(r"Graphs/@Maruti_Corp.png")
    load11 = load11.resize((200,200))
    render11 = ImageTk.PhotoImage(load11)
    i11 = tk.Label(window, image = render11 , height=170, width= 170)
    i11.place(x=570,y=210)
    i1_n = tk.Label(window,text="@Maruti_Corp",fg="black" , height=1, width= 15)
    i1_n.place(x=570,y=390)
    
    load12 = PIL.Image.open(r"Graphs/@Mahindra_Auto.png")
    load12 = load12.resize((200,200))
    render12 = ImageTk.PhotoImage(load12)
    i12 = tk.Label(window, image = render12 , height=170, width= 170)
    i12.place(x=760,y=210)
    i1_n = tk.Label(window,text="@Mahindra_Auto",fg="black" , height=1, width= 15)
    i1_n.place(x=760,y=390)
    
    load13 = PIL.Image.open(r"Graphs/@AbbottNews.png")
    load13 = load13.resize((200,200))
    render13 = ImageTk.PhotoImage(load13)
    i13 = tk.Label(window, image = render13 , height=170, width= 170)
    i13.place(x=950,y=210)
    i1_n = tk.Label(window,text="@AbbottNews",fg="black" , height=1, width= 15)
    i1_n.place(x=950,y=390)
    
    load14 = PIL.Image.open(r"Graphs/@sanofi.png")
    load14 = load14.resize((200,200))
    render14 = ImageTk.PhotoImage(load14)
    i14 = tk.Label(window, image = render14 , height=170, width= 170)
    i14.place(x=1140,y=210)
    i1_n = tk.Label(window,text="@sanofi",fg="black" , height=1, width= 10)
    i1_n.place(x=1140,y=390)
    
    load15 = PIL.Image.open(r"Graphs/@Alkem_Lab.png")
    load15 = load15.resize((200,200))
    render15 = ImageTk.PhotoImage(load15)
    i15 = tk.Label(window, image = render15 , height=170, width= 170)
    i15.place(x=0,y=420)
    i1_n = tk.Label(window,text="@Alkem_Lab",fg="black" , height=1, width= 10)
    i1_n.place(x=0,y=600)
    
    load16 = PIL.Image.open(r"Graphs/@pfizer.png")
    load16 = load16.resize((200,200))
    render16 = ImageTk.PhotoImage(load16)
    i16 = tk.Label(window, image = render16 , height=170, width= 170)
    i16.place(x=190,y=420)
    i1_n = tk.Label(window,text="@pfizer",fg="black" , height=1, width= 10)
    i1_n.place(x=190,y=600)
    
    load17 = PIL.Image.open(r"Graphs/@KEC_Intl.png")
    load17 = load17.resize((200,200))
    render17 = ImageTk.PhotoImage(load17)
    i17 = tk.Label(window, image = render17 , height=170, width= 170)
    i17.place(x=380,y=420)   
    i1_n = tk.Label(window,text="@KEC_Intl",fg="black" , height=1, width= 10)
    i1_n.place(x=380,y=600)
    
    load18 = PIL.Image.open(r"Graphs/@AdaniOnline.png")
    load18 = load17.resize((200,200))
    render18 = ImageTk.PhotoImage(load18)
    i18 = tk.Label(window, image = render18 , height=170, width= 170)
    i18.place(x=570,y=420)   
    i1_n = tk.Label(window,text="@AdaniOnline",fg="black" , height=1, width= 10)
    i1_n.place(x=570,y=600)
    
    load19 = PIL.Image.open(r"Graphs/@OfficialNBCC.png")
                              #E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\Graphs
    load19 = load17.resize((200,200))
    render19 = ImageTk.PhotoImage(load19)
    i19 = tk.Label(window, image = render19 , height=170, width= 170)
    i19.place(x=760,y=420)   
    i1_n = tk.Label(window,text="@OfficialNBCC",fg="black" , height=1, width= 10)
    i1_n.place(x=760,y=600)
    
    load20 = PIL.Image.open(r"Graphs/@BHEL_India.png")
    load20 = load17.resize((200,200))
    render20 = ImageTk.PhotoImage(load20)
    i20 = tk.Label(window, image = render20 , height=170, width= 170)
    i20.place(x=950,y=420)   
    i1_n = tk.Label(window,text="@BHEL_India",fg="black" , height=1, width= 10)
    i1_n.place(x=950,y=600)
    
    
    
    window.mainloop()
Home()