from tkinter import * # for GUI
import tkinter as tk # For alias
import PIL.Image # to display image on tkinter
global fn # Global variable
import textwrap # For warpping texts
import tweepy # for loading twitts from twitter
global twit_sel # global variable
from PIL import ImageTk
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer # Import function from library
import cv2
def run():    
    twit_sel= '@TCS'
    # For getting authentication from twitter to get twit data
    CONSUMER_KEY = 'U6EGQgda0uChCDbrGDgFmqTbx'  # Consumaer key
    CONSUMER_SECRET = 'slNKflyQSHpStZXvS1lSXS9MDGb1tg4MyAo1VqVF78I5bZfdR4' # Secret key or Password
    ACCESS_KEY = '1149581774583808001-LmKDH5OHVIT71lDbY5iyiEX9EtyMcq' # Access token id
    ACCESS_SECRET = 'hfRBp2FqR0PgmJQoKPFLbhqcyZ5w1zGTPEKWTcfU6BgMP' # Accsess token Password
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    root = tk.Tk()
    root.title("Stock Market Prediction")
    
    
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    
    
    load = PIL.Image.open("S_BG.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(root, image = render , height=850, width= 1700)
    img.place(x=0,y=0)
    
    
    ########################################################################################################################
    
    def Tweet_Analysis():
        frame_display = tk.LabelFrame(root, text=" --Tweets-- ", width=400, height=300, bd=2, font=('times', 20, ' bold '),bg="white",fg="blue")
        frame_display.grid(row=0, column=0, sticky='s')
        frame_display.place(x=900, y=97)
    
    
        canvas=tk.Canvas(frame_display,bg='#FFFFFF',width=250,height=500,scrollregion=(0,0,1000,4000)) # to display twits in a  right side container
        hbar=tk.Scrollbar(frame_display,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=canvas.xview)
        vbar=tk.Scrollbar(frame_display,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=400,height=500)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
    
        # Left side container
        frame_alpr = tk.LabelFrame(root, text=" --Process-- ", width=200, height=600, bd=2,fg="black", font=('Tempus Sans ITC', 10, ' bold '),bg="white")
        frame_alpr.grid(row=0, column=0, sticky='nw')
        frame_alpr.place(x=10, y=97)
    
    
    
        
        def display_tweet(twitter_handle):
            iro = 10
            icol = 10
            print(twitter_handle)
            canvas.delete("all")
            #        twitter_handle=mylistbox.curselection()
            test = str(twitter_handle)
            frame_display.config(text="----" + test + "----")
            wrapper = textwrap.TextWrapper(width=100)
            #        details=tweet_frm.show_twee()
            tweets = api.user_timeline(twitter_handle, count=20, tweet_mode='extended')
            #value = {twitter_handle:{'pos':[],'neg':[]}}
    #        value = {}
    #        value[twitter_handle] = ('pos')
            #value[twitter_handle].add('pos','neg')
            negative,positive = [],[]
            print(type(tweets))
            for t in tweets:
                twit = t.full_text
                word_list = wrapper.wrap(text=twit)
                for element in word_list:
                    try:
                        canvas.create_text(iro, icol, font="times", anchor="w", text=element)
                        icol = icol + 30
                    except:
                        print('E')
                print(word_list)
    
                #z=[str(word_list)]
    
                sid = SentimentIntensityAnalyzer() # for getting polarity of twits
                for i in word_list:
                    ss = sid.polarity_scores(i)
                print(ss) # To display polarity on Console
                #value[twitter_handle['pos']]
                print(type(ss))
                ss = dict(ss)
                #print(type(ss))
                print(ss['pos'])
                negative.append(ss['neg'])
                positive.append(ss['pos'])
                print("negative",negative)
                print("positive",positive)
    #            value[twitter_handle]['pos'].append(positive)
    #            value[twitter_handle]['neg'].append(negative)
                import matplotlib.pyplot as plt
                y = [sum(negative)/len(negative),sum(positive)/len(positive)]
                
                
                x=['Negative','Positive']
                plt.bar(x,y ,color=['red','green'],align='center')
                plt.xlabel("Tweet's Sentiment")
                # naming the y axis
                plt.ylabel('Intensity')
                #plt.legend()
                plt.savefig(''+str(twitter_handle)+'.png')
                display_graph = cv2.imread('Graphs/'+str(twitter_handle)+'.png')
                cv2.imshow("Display_Graph",display_graph)
                cv2.waitKey(1)


        
                
                
    
            
    
    
    
        ################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        def Display_twits_fun(): # To display twite on GUI
            global twit_sel
            if twit_sel != "":
                display_tweet(twit_sel)
                #Example(frame_display,twit_sel).pack(side="top", fill="both", expand=True)
            else:
                print("Please Select Twitter Handle to analysis data")
    
    
        ################################################################################################################
        # twitter handlers of companies
        itemsforlistbox = ['@Infosys', '@TCS', '@LTI_Global', '@Mindtree_Ltd','@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@canarabank','@bajaj_ltd','@tvsmotorcompany','@Maruti_Corp','@Mahindra_Auto','@AbbottNews','@sanofi','@Alkem_Lab','@pfizer','@KEC_Intl','@AdaniOnline','@OfficialNBCC','@BHEL_India']  
    
    
        def CurSelet(event): # To Select Company and click on Display Tweets
            global twit_sel
            twit_sel = ""
            widget = event.widget
            selection = widget.curselection()
            picked = widget.get(selection[0])
            twit_sel = picked
    
        mylistbox=tk.Listbox(frame_alpr,width=25,height=20,font=('times',13),fg='blue',bg='snow')
        mylistbox.bind('<<ListboxSelect>>',CurSelet)
        mylistbox.place(x=0,y=40)
    
        for items in itemsforlistbox:
            mylistbox.insert(tk.END,items)
    
        button1 = tk.Button(frame_alpr, text=" Display Tweets ", command=Display_twits_fun, width=17, height=1,font=('times', 15, ' bold '), bg="black", fg="white")
        button1.place(x=1, y=0)
    
        #    Example(frame_display,twit_sel).pack(side="top", fill="both", expand=True)
    
    
    def GRAPH():
        from subprocess import call
        #call(["python","GRAPH.py"])
        call(["python","GRAPH.py"])
       
    def Exit():
        root.destroy()
    
    
    
    
    def TOP_10_FILTER():
        itemsforlistbox = ['@Infosys', '@TCS', '@LTI_Global', '@Mindtree_Ltd','@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@canarabank','@bajaj_ltd','@tvsmotorcompany','@Maruti_Corp','@Mahindra_Auto','@AbbottNews','@sanofi','@Alkem_Lab','@pfizer','@KEC_Intl','@AdaniOnline','@OfficialNBCC','@BHEL_India']  
        RATIO_LIST = []
        RATIO_DICT = {}
        def display_tweet1(twitter_handle):
                
                wrapper = textwrap.TextWrapper(width=100)
                #        details=tweet_frm.show_twee()
                tweets = api.user_timeline(twitter_handle, count=30, tweet_mode='extended')
                #value = {twitter_handle:{'pos':[],'neg':[]}}
        #        value = {}
        #        value[twitter_handle] = ('pos')
                #value[twitter_handle].add('pos','neg')
                negative,positive = [],[]
                for t in tweets:
                    twit = t.full_text
                    word_list = wrapper.wrap(text=twit)
                    
                    #print(word_list)
        
                    #z=[str(word_list)]
        
                    sid = SentimentIntensityAnalyzer() # for getting polarity of twits
                    for i in word_list:
                        ss = sid.polarity_scores(i)
                    #print(ss) # To display polarity on Console
                    #value[twitter_handle['pos']]
                    #print(type(ss))
                    ss = dict(ss)
                    #print(type(ss))
                    #print(ss['pos'])
                    negative.append(ss['neg'])
                    positive.append(ss['pos'])
                    #print("negative",negative)
                    #print("positive",positive)
                    try:
                        ratio = sum(positive)/sum(negative)
                        RATIO_LIST.append(ratio)
                        RATIO_DICT[twitter_handle]=ratio
                    except:
                        ZeroDivisionError
        jcb =1                    
        for pqr in itemsforlistbox:
            display_tweet1(pqr)
            #print(jcb)
            jcb+=1
                
        #RATIO_LIST = []
        #RATIO_DICT = {}            
        
        itemsforlistbox = ['@Infosys', '@TCS', '@LTI_Global', '@Mindtree_Ltd','@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@canarabank','@bajaj_ltd','@tvsmotorcompany','@Maruti_Corp','@Mahindra_Auto','@AbbottNews','@sanofi','@Alkem_Lab','@pfizer','@KEC_Intl','@AdaniOnline','@OfficialNBCC','@BHEL_India']
        it_name= ['@Infosys','@TCS', '@LTI_Global', '@Mindtree_Ltd']
        bank_name = ['@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@canarabank']
        automobile_name = ['@bajaj_ltd','@tvsmotorcompany','@Maruti_Corp','@Mahindra_Auto']
        pharma_name = ['@AbbottNews','@sanofi','@Alkem_Lab','@pfizer']
        infra_name = ['@KEC_Intl','@AdaniOnline','@OfficialNBCC','@BHEL_India']
        #'@Infosys' in RATIO_DICT
        
        IT_SEC = []
        BANK_SEC = []
        AUTO_SEC = []
        PHARMA_SEC = []
        INFRA_SEC = []
        for keys,values in RATIO_DICT.items():
            #print(keys)
            if keys in it_name:
                IT_SEC.append((keys,values))
            if keys in bank_name:
                BANK_SEC.append((keys,values))
            if keys in automobile_name:
                AUTO_SEC.append((keys,values))
            if keys in pharma_name:
                PHARMA_SEC.append((keys,values))
            if keys in infra_name:
                INFRA_SEC.append((keys,values))
                
                    
        
        IT_SEC_D = {}
        c=0
        for j in IT_SEC:
            #print(j)
            IT_SEC_D[IT_SEC[c][0]]=IT_SEC[c][1]
            c+=1
            
        
        BANK_SEC_D = {}
        c=0
        for j in BANK_SEC:
            #print(j)
            BANK_SEC_D[BANK_SEC[c][0]]=BANK_SEC[c][1]
            c+=1
        
        AUTO_SEC_D = {}
        c=0
        for j in AUTO_SEC:
            #print(j)
            AUTO_SEC_D[AUTO_SEC[c][0]]=AUTO_SEC[c][1]
            c+=1
    
        PHARMA_SEC_D = {}
        c=0
        for j in PHARMA_SEC:
            #print(j)
            PHARMA_SEC_D[PHARMA_SEC[c][0]]=PHARMA_SEC[c][1]
            c+=1
    
        INFRA_SEC_D = {}
        c=0
        for j in INFRA_SEC:
            #print(j)
            INFRA_SEC_D[INFRA_SEC[c][0]]=INFRA_SEC[c][1]
            c+=1
        
        #==================================================
        from itertools import islice
        def take(n,iterable):
            return list(islice(iterable,n))
    
        dat = sorted(IT_SEC_D.values())
        dat = dat[::-1]
        
        dat_d = {}
        for klm in dat:
            #print(list(IT_SEC_D.keys())[list(IT_SEC_D.values()).index(klm)])
            dat_d[list(IT_SEC_D.keys())[list(IT_SEC_D.values()).index(klm)]]=klm
    
        IT_2 =take(2,dat_d.items())
        
        
        
        
        dat = sorted(BANK_SEC_D.values())
        dat = dat[::-1]
        
        dat_d = {}
        for klm in dat:
            #print(list(BANK_SEC_D.keys())[list(BANK_SEC_D.values()).index(klm)])
            dat_d[list(BANK_SEC_D.keys())[list(BANK_SEC_D.values()).index(klm)]]=klm
    
        BANK_2 =take(2,dat_d.items())
        
        
        
        dat = sorted(AUTO_SEC_D.values())
        dat = dat[::-1]
        
        dat_d = {}
        for klm in dat:
            #print(list(AUTO_SEC_D.keys())[list(AUTO_SEC_D.values()).index(klm)])
            dat_d[list(AUTO_SEC_D.keys())[list(AUTO_SEC_D.values()).index(klm)]]=klm
    
        AUTO_2 =take(2,dat_d.items())
        
        
        
        
        dat = sorted(PHARMA_SEC_D.values())
        dat = dat[::-1]
        
        dat_d = {}
        for klm in dat:
            #print(list(PHARMA_SEC_D.keys())[list(PHARMA_SEC_D.values()).index(klm)])
            dat_d[list(PHARMA_SEC_D.keys())[list(PHARMA_SEC_D.values()).index(klm)]]=klm
    
        PHARMA_2 =take(2,dat_d.items())
        
        
    
        
        dat = sorted(INFRA_SEC_D.values())
        dat = dat[::-1]
        
        dat_d = {}
        for klm in dat:
            #print(list(INFRA_SEC_D.keys())[list(INFRA_SEC_D.values()).index(klm)])
            dat_d[list(INFRA_SEC_D.keys())[list(INFRA_SEC_D.values()).index(klm)]]=klm
    
        INFRA_2 =take(2,dat_d.items())
        
        
        
        RECIEVED = [IT_2,BANK_2, AUTO_2,PHARMA_2,INFRA_2]
        
        
        IT_2[0]
        RECIEVED[2]
        #RECIEVED[2][1][0]
        
        TOP_10_LIST = []
        for Q in RECIEVED:
            #print(Q[0])
                for R in Q:
                    print(R[0])
                    TOP_10_LIST.append(R[0])
        #print(len(TOP_10_LIST))
        
        write = open(r"TOP_10_COMP.txt","w")
        write.write(str(TOP_10_LIST))
        write.close()
        #return TOP_10_LIST
        
    #answer = TOP_10_FILTER()
   ################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
    
    
    
    
    
    def OPP():
        from subprocess import call
        call(["python","CNN_FILE.py"])
    
    ########################################################################################################################
    
    wlcm = "Stock Market Prediction using NLP and Deep Learning"
    welcome = tk.Label(root, text = wlcm ,font=("Tempus Sans ITC", 20,"bold"),bg="green",fg="white",width=110,height=2)
    welcome.place(x=0,y=20)
    
    #button1 = tk.Button(frame_alpr, text=" Display Tweets ", command=Display_twits_fun,width=17, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
    #button1.place(x=1, y=0)
    
    analysis = tk.Button(root, text = "Twitter Analysis" ,command = Tweet_Analysis,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="#7D0552",fg="white")
    analysis.place(x=220,y=150)
    
    graph = tk.Button(root, text = "Show All Graphs" ,command = GRAPH,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="#7D0552",fg="white")
    graph.place(x=220,y=250)
    
    filter_button = tk.Button(root, text = "Filter top 10 Compnaies" ,command = TOP_10_FILTER,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="#7D0552",fg="white")
    filter_button.place(x=220,y=350)
    
    price_predictor = tk.Button(root, text = "Open Price Predictor" ,command = OPP,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="#7D0552",fg="white")
    price_predictor.place(x=220,y=450)
    
    
    exit = tk.Button(root, text = "Exit" ,command = Exit,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="black",fg="white")
    exit.place(x=220,y=650)
    
    
    root.mainloop()
    
    
    #Import the necessary methods from tweepy library
    
    
    
    #This is a basic listener that just prints received tweets to stdout.

run()