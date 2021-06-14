from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
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
from matplotlib import pyplot
from numpy import array
from PIL import ImageTk , Image
import PIL


def SHOW_IT():
    
    
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
    IT_COMP = ['INFY','TCS','LTI','MINDTREE']
    for  i in GRAPH_LIST:
        
        if i.split('/')[-1].split('.')[0] in IT_COMP:
            TOP_IT_1 = i
            
    print(TOP_IT_1)
    import pandas_datareader as pdr    
    datetime.today().strftime('%Y-%d-%m')
    now=datetime.today().strftime('%Y,%d,%m')
    print(now)
       
    
    
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
    # reshape training into [samples, timesteps, features]
    #    X, y = train[:, 0:n_seq], train[:, n_seq:]
    #    X = X.reshape((X.shape[0], X.shape[1], 1))
        X, y = train[:, 0:n_lag], train[:, n_lag:]
        
        X = X.reshape(X.shape[0], X.shape[1],1)
    #    print(X,y)
    
    
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
    
    ## evaluate the persistence model
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
    
    
    # evaluate the RMSE for each forecast time step
    def evaluate_forecasts(test, forecasts, n_lag, n_seq):
        RMSE = []
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
        pyplot.legend()
        pyplot.savefig(r'Forecasting.png')
        f=file.split("/").pop()
        f=f.split(".").pop(0)
        
        print('f',f)
        print('file',file)
        pyplot.savefig('stock/'+str(f)+'.png')
        pyplot.savefig(file.split('.')[0]+'.png')
        
        
        
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
            pyplot.savefig(str(f)+'.png')
            pyplot.show()
                

    
    import os
    
    
    
    import pandas_datareader as pdr
    from datetime import datetime
    datetime.today().strftime('%Y-%d-%m')
    now=datetime.today().strftime('%Y,%d,%m')
    print(now)
    SYMBOLS = ['HCLTECH.NS','WIPRO.NS','TECHM.NS','MPHASIS.NS','HEXAWARE.NS']
    NEW_IT_GRAPH_LIST = []
    for comp in SYMBOLS:
        print(comp)
        data = pdr.get_data_yahoo(symbols=str(comp), start=datetime(2010, 1, 1), end=now)
        file = r'CSV'+str(comp.split('.')[0])+'.csv'
        print(file)
        data.to_csv(r'CSV'+str(comp.split('.')[0])+'.csv')
        NEW_IT_GRAPH_LIST.append(r'CSV'+str(comp.split('.')[0])+'.png')
    
        series = read_csv(r'CSV'+str(comp.split('.')[0])+'.csv')
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
        plot_forecasts(series, forecasts, n_test+2)
    
    
    
    window = tk.Tk()
    w,h = window.winfo_screenwidth() , window.winfo_screenheight()
    window.geometry("%dx%d+0+0"%(w,h))
    window.configure(background="cyan")
    
    load1 = PIL.Image.open(TOP_IT_1)
    load1 =load1.resize((400,300), Image.ANTIALIAS)
    render1 = ImageTk.PhotoImage(load1)
    i1 = tk.Label(window, image = render1)
    i1.image = render1
    i1.place(x=5,y=0)
    i1_n = tk.Label(window,text=str(TOP_IT_1.split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i1_n.place(x=5,y=305)
    
    
    load2 = PIL.Image.open(NEW_IT_GRAPH_LIST[0])
    load2 =load2.resize((400,300), Image.ANTIALIAS)
    render2 = ImageTk.PhotoImage(load2)
    i2 = tk.Label(window, image = render2)
    i2.image = render2
    i2.place(x=450,y=0)
    i2_n = tk.Label(window,text=str(NEW_IT_GRAPH_LIST[0].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i2_n.place(x=450,y=305)
    
    
    load3 = PIL.Image.open(NEW_IT_GRAPH_LIST[1])
    load3 =load3.resize((400,300), Image.ANTIALIAS)
    render3 = ImageTk.PhotoImage(load3)
    i3 = tk.Label(window, image = render3)
    i3.image = render3
    i3.place(x=900,y=0)
    i3_n = tk.Label(window,text=str(NEW_IT_GRAPH_LIST[1].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i3_n.place(x=900,y=305)
    
    
    load4 = PIL.Image.open(NEW_IT_GRAPH_LIST[2])
    load4 =load4.resize((400,300), Image.ANTIALIAS)
    render4 = ImageTk.PhotoImage(load4)
    i4 = tk.Label(window, image = render4)
    i4.image = render4
    i4.place(x=5,y=350)
    i4_n = tk.Label(window,text=str(NEW_IT_GRAPH_LIST[2].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i4_n.place(x=5,y=655)
    
    
    load5 = PIL.Image.open(NEW_IT_GRAPH_LIST[3])
    load5 =load5.resize((400,300), Image.ANTIALIAS)
    render5 = ImageTk.PhotoImage(load5)
    i5 = tk.Label(window, image = render5)
    i5.image = render5
    i5.place(x=450,y=350)
    i5_n = tk.Label(window,text=str(NEW_IT_GRAPH_LIST[3].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i5_n.place(x=450,y=655)
    
    
    load6 = PIL.Image.open(NEW_IT_GRAPH_LIST[4])
    load6 =load5.resize((400,300), Image.ANTIALIAS)
    render6 = ImageTk.PhotoImage(load6)
    i6 = tk.Label(window, image = render6)
    i6.image = render6
    i6.place(x=900,y=350)
    i6_n = tk.Label(window,text=str(NEW_IT_GRAPH_LIST[4].split('/')[-1].split('.')[0]),fg="black",bg="cyan" , height=1, width= 12)
    i6_n.place(x=900,y=655)
    
    
    window.mainloop()
    
SHOW_IT()