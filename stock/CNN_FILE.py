from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.layers import Dense, Flatten
from matplotlib import pyplot
import tkinter as tk
from math import sqrt
from numpy import array
from PIL import ImageTk , Image
import PIL


root = tk.Tk()
root.title("Stock Market Prediction")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
#root.configure(background='black')


load_bg = PIL.Image.open(r"bg2.jpg")
                           
load_bg = load_bg.resize((w,h))
render_bg = ImageTk.PhotoImage(load_bg)
bg = tk.Label(root, image = render_bg , height=h, width= w)
bg.place(x=0,y=0)

head= tk.Label(root,text="... Stock Price Prediction ...",font=("Elephant",30,'italic'),bg="brown",fg="white",width=55,height=2)
head.place(x=0,y=0)

#global TOP_10_LIST
#global TOP_5_LIST_IMG

def LOAD_FUNCTIONS():
    
    
    def parser(x):
        return datetime.strptime('190'+x, '%Y-%m')
    
    # convert time series into supervised learning problem
    def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        df = DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
        # put it all together
        agg = concat(cols, axis=1)
        print(agg)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg
    
    # create a differenced series
    def difference(dataset, interval=1):
        diff = list()
        for i in range(interval, len(dataset)):
            value = dataset[i] - dataset[i - interval]
            diff.append(value)
        return Series(diff)
    
    # transform series into train and test sets for supervised learning
    def prepare_data(series, n_test, n_lag, n_seq):
        # extract raw values
        raw_values = series.values
        # transform data to be stationary
        diff_series = difference(raw_values, 1)
        diff_values = diff_series.values
        diff_values = diff_values.reshape(len(diff_values), 1)
        # rescale values to -1, 1
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_values = scaler.fit_transform(diff_values)
        scaled_values = scaled_values.reshape(len(scaled_values), 1)
        # transform into supervised learning problem X, y
        supervised = series_to_supervised(scaled_values, n_lag, n_seq)
        supervised_values = supervised.values
        # split into train and test sets
        train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
        return scaler, train, test
    
    
    ####==========================================================================================
    
    ## fit an LSTM network to training data
    def fit_CNN(train, n_lag, n_seq, n_batch, nb_epoch, n_neurons):
    
        X, y = train[:, 0:n_lag], train[:, n_lag:]
        
        X = X.reshape(X.shape[0], X.shape[1],1)
    
    
    
    # design network
        model_cnn = Sequential()
        model_cnn.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(X.shape[1], X.shape[2])))
        model_cnn.add(MaxPooling1D(pool_size=2))
        model_cnn.add(Flatten())
        model_cnn.add(Dense(50, activation='relu'))
        model_cnn.add(Dense(y.shape[1]))
        model_cnn.compile(loss='mse', optimizer='adam')
        model_cnn.summary()
    # fit network
        cnn_history = model_cnn.fit(X,y, epochs=nb_epoch, verbose=2)
        
    
    
        return model_cnn
    
    
    
    ###=============================================================================================
    
    
    def forecast_cnn(model, X, n_batch):
        # reshape input pattern to [samples, timesteps, features]
        X = X.reshape(1, len(X),1)
        # make forecast
        forecast = model.predict(X, batch_size=n_batch)
        # convert to array
        return [x for x in forecast[0, :]]
    
    
    forecasts = []
    def make_forecasts(model, n_batch, train, test, n_lag, n_seq):
        forecasts = list()
        for i in range(len(test)):
            X,y = test[i, 0:n_lag], test[i, n_lag:]
            # make forecast
            forecast = forecast_cnn(model, X, n_batch)
    #        forecast = forecast_lstm(model, X, n_batch)
            # store the forecast
            forecasts.append(forecast)
        return forecasts
    
    
    #####==========================================================================================================
    # invert differenced forecast
    def inverse_difference(last_ob, forecast):
        # invert first forecast
        inverted = list()
        inverted.append(forecast[0] + last_ob)
        # propagate difference forecast using inverted first value
        for i in range(1, len(forecast)):
            inverted.append(forecast[i] + inverted[i-1])
        return inverted
    
    # inverse data transform on forecasts
    def inverse_transform(series, forecasts, scaler, n_test):
        inverted = list()
        for i in range(len(forecasts)):
            # create array from forecast
            forecast = array(forecasts[i])
            forecast = forecast.reshape(1, len(forecast))
            # invert scaling
            inv_scale = scaler.inverse_transform(forecast)
            inv_scale = inv_scale[0, :]
            # invert differencing
            index = len(series) - n_test + i - 1
            last_ob = series.values[index]
            inv_diff = inverse_difference(last_ob, inv_scale)
            # store
            inverted.append(inv_diff)
        return inverted
    
    RATIO_LIST2 = []
    RATIO_DICT2 = {}
    # evaluate the RMSE for each forecast time step
    
    def evaluate_forecasts(test, forecasts, n_lag, n_seq):
        #del pyplot
        from matplotlib import pyplot
        RMSE = []
        y = []
        x = []
        for i in range(n_seq):
            actual = [row[i] for row in test]
            predicted = [forecast[i] for forecast in forecasts]
            rmse = sqrt(mean_squared_error(actual, predicted))
            print('t+%d RMSE: %f' % ((i+1), rmse))
            RMSE.append(rmse)
        y=list(predicted)
        print(predicted)
        print(y)
        print(len(y))
        x=range(len(y))
        
        pyplot.plot(x,y , label="Y-axis=>Price",color='green', linewidth=2,marker='.', markerfacecolor='green', markersize=12)
        pyplot.xlabel('Days')
        # naming the y axis
        pyplot.ylabel('Price')
        #pyplot.legend()
        pyplot.legend(loc='upper left', bbox_to_anchor=(1,1))
        print('file ',file)
        
        pyplot.savefig(file.split('.')[0]+'.png')
        
        F_HALF = y[:int(len(y)/2)]
        S_HALF = y[int(len(y)/2):]
        ratio = sum(S_HALF)/sum(F_HALF)
        
        RATIO_LIST2.append(ratio)
        RATIO_DICT2[file.split('.')[0].split('/')[-1]]=ratio
        #del forecasts
        del y , x , RMSE , forecasts
        
        """
        
    def evaluate_forecasts(test, forecasts, n_lag, n_seq):
        RMSE = []
        predicted = None
        for i in range(n_seq):
            actual = [row[i] for row in test]
            predicted = [forecast[i] for forecast in forecasts]
            rmse = sqrt(mean_squared_error(actual, predicted))
            print('t+%d RMSE: %f' % ((i+1), rmse))
            RMSE.append(rmse)
        y=0
        x=0
        y=list(predicted)
        #print(predicted)
        #print(y)
        #print(len(y))
        x=range(len(y))
        print("y :",y,len(y))
        print("x :",x)
        #pyplot.plot(x , label="Y-axis=>Price",color='green', linewidth=2,marker='.', markerfacecolor='green', markersize=12)
        pyplot.plot(y , label="Y-axis=>Price",color='green', linewidth=2,marker='.', markerfacecolor='green', markersize=12)
        pyplot.xlabel('Days')
        # naming the y axis
        pyplot.ylabel('Price')
        pyplot.legend()
        print("Plotted Graph")
        #pyplot.savefig(r'Forecasting.png')
        #f=file.split("/").pop()
        f=file.split(".").pop(0)
        
        print('f',f)
        #print('file',file)
        f = f.replace("\\","/")
        pyplot.savefig(str(f)+'.png')
        """
    # plot the forecasts in the context of the original dataset
    def plot_forecasts(series, forecasts, n_test):
        # plot the entire dataset in blue
        pyplot.plot(series.values)
        # plot the forecasts in red
        for i in range(len(forecasts)):
            off_s = len(series) - n_test + i - 1
#            try:
            off_e = off_s + len(forecasts[i]) + 1
            xaxis = [x for x in range(off_s, off_e)]
            #xaxis =[series.index]
            yaxis = [series.values[off_s]] + forecasts[i]
            pyplot.plot(xaxis, yaxis, color='red')
            # show the plot
            f=file.split("/").pop()
            f=f.split(".").pop(0)
            #print(file)
            print(f)   
            #pyplot.savefig(str(f)+'.png')
            #pyplot.show()




    #CSV_PATH = {'@Infosys':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\INFY.csv', '@TCS':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\TCS.csv', '@LTI_Global':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\LTI.csv', '@Mindtree_Ltd':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\MINDTREE.csv','@HDFC_Bank':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\HDFC.csv','@TheOfficialSBI':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\SBI.csv','@bankofbaroda':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\BANKBARODA.csv','@canarabank':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\CANBK.csv','@bajaj_ltd':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\BAJAJ.csv','@tvsmotorcompany':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\TVS.csv','@Maruti_Corp':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\MARUTI.csv','@Mahindra_Auto':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\M&M.csv','@AbbottNews':'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\ABBOT.csv','@sanofi':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\SANOFI.csv','@Alkem_Lab':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\ALKEM.csv','@pfizer':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\PFIZER.csv','@KEC_Intl':r'E:\OMKARS\OMKARS1\Jagdish\DEVOPS\STOCK_ME\CSV\KEC.csv','@AdaniOnline':r'','@OfficialNBCC':r'','@BHEL_India':r''}
    #TOP_10_LIST = ['@Infosys','@HDFC_Bank','@TheOfficialSBI','@bankofbaroda','@bajaj_ltd','@tvsmotorcompany','@Mahindra_Auto','@AbbottNews','@Alkem_Lab','@pfizer','@KEC_Intl','@AdaniOnline','@OfficialNBCC']
    
    write = open(r"TOP_10_COMP.txt","r")
    
    GRAPH_LIST = write.readline()
    GRAPH_LIST = GRAPH_LIST.split("'")
    GRAPH_LIST.remove(', ')
    GRAPH_LIST.remove("[")
    GRAPH_LIST.remove("]")
    GRAPH_LIST = list(GRAPH_LIST)
    GRAPH_LIST = set(GRAPH_LIST)
    GRAPH_LIST = list(GRAPH_LIST)
    GRAPH_LIST.remove(', ')
    TOP_10_LIST = GRAPH_LIST
    print(TOP_10_LIST)
    write.close()
    
    import pandas_datareader as pdr
    from datetime import datetime
    datetime.today().strftime('%Y-%d-%m')
    now=datetime.today().strftime('%Y,%d,%m')
    print(now)
    SYMBOLS_LIST = {'@Infosys':'INFY.NS', '@TCS':'TCS.NS', '@LTI_Global':'LTI.NS', '@Mindtree_Ltd':'MINDTREE.NS','@HDFC_Bank':'HDFC.NS','@TheOfficialSBI':'SBIN.NS','@bankofbaroda':'BANKBARODA.NS','@canarabank':'CANBK.NS','@bajaj_ltd':'BAJAJ-AUTO.NS','@tvsmotorcompany':'TVSMOTOR.NS','@Maruti_Corp':'MARUTI.NS','@Mahindra_Auto':'M&M.NS','@AbbottNews':'ABBOTINDIA.NS','@sanofi':'SANOFI.NS','@Alkem_Lab':'ALKEM.NS','@pfizer':'PFIZER.NS','@KEC_Intl':'KEC.NS','@AdaniOnline':'ADANIPORTS.NS','@OfficialNBCC':'NBCC.NS','@BHEL_India':'BHEL.NS'}
    for comp in TOP_10_LIST:
        print(SYMBOLS_LIST[comp])
        print(comp)
        data = pdr.get_data_yahoo(symbols=str(SYMBOLS_LIST[comp]), start=datetime(2010, 1, 1), end=now)
        
        #file = 'E:/OMKARS/OMKARS1/Jagdish/DEVOPS/STOCK_ME/CSV/'+str(SYMBOLS_LIST[comp].split('.')[0])+'.csv'
        #print(file)
        
        data.to_csv(r'CSV'+str(SYMBOLS_LIST[comp].split('.')[0])+'.csv')
        file = r'CSV'+str(SYMBOLS_LIST[comp].split('.')[0])+'.csv'
        print(file)
        
    import os
    directory = r'CSV'
    file_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file = os.path.join(directory, filename)
            print(file)
            file_list.append(file)
            #file = "BHEL.csv"
    for file in file_list:       
        print(file)
    
                
        series = read_csv(file)
        #series = read_csv('E:/OMKARS/OMKARS1/Jagdish/DEVOPS/STOCK_ME/CSV/'+str(SYMBOLS_LIST[comp].split('.')[0])+'.csv')
        #print(series)
        series=series.iloc[ : , 2 ]
        
        # configure
        n_lag = 3
        n_seq = 30
        n_test = 50
        n_epochs =5
        n_batch = 1
        n_neurons = 1
        # prepare data
        scaler, train, test = prepare_data(series, n_test, n_lag, n_seq)
        
        print('Train set shape', train.shape)
        print('Test set shape', test.shape)
        
        # fit model
        model = fit_CNN(train, n_lag, n_seq, n_batch, n_epochs, n_neurons)
        
        
        # make forecasts
        forecasts = make_forecasts(model, n_batch, train, test, n_lag, n_seq)
        # inverse transform forecasts and test
        forecasts = inverse_transform(series, forecasts, scaler, n_test+2)
        actual = [row[n_lag:] for row in test]
        actual = inverse_transform(series, actual, scaler, n_test+2)
        # evaluate forecasts
        evaluate_forecasts(actual, forecasts, n_lag, n_seq)
        # plot forecasts
        date_here = [i for i in series.index]
        date_here=pd.DataFrame(date_here)
        #plot_forecasts(series, forecasts, n_test+2)
    
        
        """
        
        
        
        print(file)
        series = read_csv(file)
        series=series.iloc[ : , 2 ]
        
        # configure
        n_lag = 3
        n_seq = 30
        n_test = 50
        n_epochs =5
        n_batch = 1
        n_neurons = 1
        # prepare data
        scaler, train, test = prepare_data(series, n_test, n_lag, n_seq)
        
        print('Train set shape', train.shape)
        print('Test set shape', test.shape)
        
        # fit model
        model = fit_CNN(train, n_lag, n_seq, n_batch, n_epochs, n_neurons)
        
        
        # make forecasts
        forecasts = make_forecasts(model, n_batch, train, test, n_lag, n_seq)
        # inverse transform forecasts and test
        forecasts = inverse_transform(series, forecasts, scaler, n_test+2)
        actual = [row[n_lag:] for row in test]
        actual = inverse_transform(series, actual, scaler, n_test+2)
        # evaluate forecasts
        evaluate_forecasts(actual, forecasts, n_lag, n_seq)
        # plot forecasts
        date_here = [i for i in series.index]
        date_here=pd.DataFrame(date_here)
        #plot_forecasts(series, forecasts, n_test+2)
        """
        
        
        
        
        
        
        
        
        
        
        
    op = ['INFY.NS', 'TCS.NS','LTI.NS','MINDTREE.NS','HDFC.NS','SBIN.NS','BANKBARODA.NS','CANBK.NS','BAJAJ-AUTO.NS','TVSMOTOR.NS','MARUTI.NS','M&M.NS','ABBOTINDIA.NS','SANOFI.NS','ALKEM.NS','PFIZER.NS','KEC.NS','ADANIPORTS.NS','NBCC.NS','BHEL.NS']
    
        
        
    RATIO_DICT2 = {'INFY': 0.8641662860414908,'HDFC': 0.7499079522775906, 'SBIN': 0.7822953739123798,  'BAJAJ-AUTO': 0.7883904119300693, 'TVSMOTOR': 0.8292714405267352,  'ABBOTINDIA': 1.0896205182768666, 'ALKEM': 0.9820647368158472, 'PFIZER': 0.9667419935196737,  'ADANIPORTS': 0.7729570968510238, 'NBCC': 0.6138259970662694}    
    len(RATIO_DICT2)
    it_name= ['INFY','TCS','LTI','MINDTREE']
    bank_name = ['HDFC','SBIN','BANKBARODA','CANBK']
    automobile_name = ['BAJAJ-AUTO','TVSMOTOR','MARUTI','M&M']
    pharma_name = ['ABBOTINDIA','SANOFI','ALKEM','PFIZER']
    infra_name = ['KEC','ADANIPORTS','NBCC','BHEL']
    
    
    IT_SEC = []
    BANK_SEC = []
    AUTO_SEC = []
    PHARMA_SEC = []
    INFRA_SEC = []
    for keys,values in RATIO_DICT2.items():
        print(keys)
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
        print(j)
        IT_SEC_D[IT_SEC[c][0]]=IT_SEC[c][1]
        c+=1
        
    
    BANK_SEC_D = {}
    c=0
    for j in BANK_SEC:
        print(j)
        BANK_SEC_D[BANK_SEC[c][0]]=BANK_SEC[c][1]
        c+=1
    
    AUTO_SEC_D = {}
    c=0
    for j in AUTO_SEC:
        print(j)
        AUTO_SEC_D[AUTO_SEC[c][0]]=AUTO_SEC[c][1]
        c+=1

    PHARMA_SEC_D = {}
    c=0
    for j in PHARMA_SEC:
        print(j)
        PHARMA_SEC_D[PHARMA_SEC[c][0]]=PHARMA_SEC[c][1]
        c+=1

    INFRA_SEC_D = {}
    c=0
    for j in INFRA_SEC:
        print(j)
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
        print(list(IT_SEC_D.keys())[list(IT_SEC_D.values()).index(klm)])
        dat_d[list(IT_SEC_D.keys())[list(IT_SEC_D.values()).index(klm)]]=klm

    IT_1 =take(1,dat_d.items())
    
    
    
    
    dat = sorted(BANK_SEC_D.values())
    dat = dat[::-1]
    
    dat_d = {}
    for klm in dat:
        print(list(BANK_SEC_D.keys())[list(BANK_SEC_D.values()).index(klm)])
        dat_d[list(BANK_SEC_D.keys())[list(BANK_SEC_D.values()).index(klm)]]=klm

    BANK_1 =take(1,dat_d.items())
    
    
    
    dat = sorted(AUTO_SEC_D.values())
    dat = dat[::-1]
    
    dat_d = {}
    for klm in dat:
        print(list(AUTO_SEC_D.keys())[list(AUTO_SEC_D.values()).index(klm)])
        dat_d[list(AUTO_SEC_D.keys())[list(AUTO_SEC_D.values()).index(klm)]]=klm

    AUTO_1 =take(1,dat_d.items())
    
    
    
    
    dat = sorted(PHARMA_SEC_D.values())
    dat = dat[::-1]
    
    dat_d = {}
    for klm in dat:
        print(list(PHARMA_SEC_D.keys())[list(PHARMA_SEC_D.values()).index(klm)])
        dat_d[list(PHARMA_SEC_D.keys())[list(PHARMA_SEC_D.values()).index(klm)]]=klm

    PHARMA_1 =take(1,dat_d.items())
    
    

    
    dat = sorted(INFRA_SEC_D.values())
    dat = dat[::-1]
    
    dat_d = {}
    for klm in dat:
        print(list(INFRA_SEC_D.keys())[list(INFRA_SEC_D.values()).index(klm)])
        dat_d[list(INFRA_SEC_D.keys())[list(INFRA_SEC_D.values()).index(klm)]]=klm

    INFRA_1 =take(1,dat_d.items())
    
    
    
    RECIEVED = [IT_1,BANK_1, AUTO_1,PHARMA_1,INFRA_1]
    
    
    IT_1[0]
    #RECIEVED[2][0][0]
    
    
    TOP_5_LIST = []
    for Q in RECIEVED:
        #print(Q[0])
            for R in Q:
                print(R[0])
                TOP_5_LIST.append(R[0])
    print(len(TOP_5_LIST))
    TOP_5_LIST
    IMG_PATH = {'INFY':r'INFY.png',
                'TCS':r'TCS.png',
                'LTI':r'LTI.png', 
                'MINDTREE':r'MINDTREE.png',
                'HDFC':r'HDFC.png',
                'SBIN':r'SBIN.png',
                'BANKBARODA':r'BANKBARODA.png',
                'CANARABK':r'CANBK.png',
                'BAJAJ-AUTO':r'BAJAJ-AUTO.png',
                'TVSMOTOR':r'TVSMOTOR.png',
                'MARUTI':r'MARUTI.png',
                'M&M':r'M&M.png',
                'ABBOTINDIA':r'ABBOTINDIA.png',
                'SANOFI':r'SANOFI.png',
                'ALKEM':r'ALKEM.png',
                'PFIZER':r'PFIZER.png',
                'KEC':r'KEC.png',
                'ADANIPORTS':r'ADANIPORTS.png',
                'NBCC':r'NBCC.png',
                'BHEL':r'BHEL.png'}
    TOP_5_LIST_IMG = []
    for img_file in TOP_5_LIST:
        TOP_5_LIST_IMG.append(IMG_PATH[img_file])
    TOP_5_LIST_IMG
    GRAPH_LIST = []
    for  i in TOP_5_LIST_IMG:
        #print(i.replace('\\','/'))
        
        GRAPH_LIST.append(i.replace('\\','/'))
    print(GRAPH_LIST)
    
    text_file = open(r"IMAGE_LIST.txt","w")
    text_file.write(str(GRAPH_LIST))
    text_file.close()
    
    #RATIO_DICT2
    TOP_10_LIST = []
    for keys,values in RATIO_DICT2.items():
        #print(IMG_PATH[keys])
        TOP_10_LIST.append(IMG_PATH[keys])    
    
    TOP_10_GRAPHS = []
    for i in TOP_10_LIST:
        TOP_10_GRAPHS.append(i.replace('\\','/'))
    
    text_file = open(r"IMAGE_LIST_10.txt","w")
    text_file.write(str(TOP_10_GRAPHS))
    text_file.close()
    
    
    
    
    
    
from subprocess import call
def SHOW_TOP_5():
    call(["python",r"SHOW_5_GRAPH.py"])
    
def SHOW_TOP_10():
    call(["python",r"SHOW_10_GRAPH.py"])
    
def SHOW_IT_SEC():
    call(["python",r"SHOW_IT_GRAPH.py"])
    
    

def Home():
    
    call(['python',r'PRICE_GRAPH.py'])



# button_L = tk.Button(root, text = "RUN ALGORITHM" ,command = LOAD_FUNCTIONS,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="black",fg="white")
# button_L.place(x=50,y=100)




all_ = tk.Button(root, text = "Show all Graphs" ,command = Home,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =2,bg ="green",fg="white")
all_.place(x=50,y=500)



button2 = tk.Button(root, text = "SHOW_TOP_5" ,command = SHOW_TOP_5,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =2,bg ="#800517",fg="white")
button2.place(x=50,y=250)

button17 = tk.Button(root, text = "SHOW_TOP_10" ,command = SHOW_TOP_10,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =2,bg ="#800517",fg="white")
button17.place(x=50,y=350)

# button3 = tk.Button(root, text = "SHOW_IT_SECTOR" ,command = SHOW_IT_SEC,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="black",fg="white")
# button3.place(x=1100,y=130)


#button4 = tk.Button(root, text = "HDFC" ,command = HDFC,font=("Tempus Sans ITC", 13,"bold"),width= 20,height =1,bg ="black",fg="white")
#button4.place(x=1100,y=170)



root.mainloop()




# from tkinter import messagebox

# #help(messagebox)
# def deleteme():
#     result = messagebox.askquestion("Delete", "Are You Sure?", icon='question')
#     if result == 'yes':
#         print ("Deleted")
#     else:
#         print ("I'm Not Deleted Yet")
        
#deleteme()