import pandas as pd
import talib as tl
import numpy as np
from talib import MA_Type
import matplotlib.pyplot as plt
from datetime import timedelta
from source.data.preprocessing import Data
from source.order.action import *
from source.order.tradeBook import tradeBook
import matplotlib.patches as mpatches


def DM_RSI_ADX(data):
    float_close = Data.toFloatArray(df['Close'])
    float_high = Data.toFloatArray(df['High'])
    float_low = Data.toFloatArray(df['Low'])
    float_open = Data.toFloatArray(df['Open'])
    adx_values = tl.ADX(np.array(float_high),np.array(float_low),np.array(float_close), timeperiod = 14)
    dmi = tl.DX(np.array(float_high),np.array(float_low),np.array(float_close), timeperiod = 14)
    mdmi = tl.MINUS_DI(np.array(float_high),np.array(float_low),np.array(float_close), timeperiod = 14)
    rsi = tl.RSI(np.array(float_close),timeperiod = 4 )
    signals = []
    flag = 0
    for i in xrange(40 , len(adx_values) - 2):
        if flag ==0:
            if adx_values[i]>20  and dmi[i]>mdmi[i] and df.loc[i+1, 'Open']> (df.loc[i, 'Close']+1.8) and rsi[i]<50:
                signal = ['HSI', df.loc[i+1, 'Date'], 'Long',  df.loc[i+1, 'Close']]
                flag =1
                signals.append(signal)
            if adx_values[i]>20  and dmi[i]<mdmi[i] and df.loc[i+1, 'Open']< (df.loc[i, 'Close']-1.8) and rsi[i]<50:
                signal = ['HSI', df.loc[i+1, 'Date'], 'Short',  df.loc[i+1, 'Close']]
                flag =2
                signals.append(signal)
        elif flag ==1:
            if df.loc[i, 'Close']>= signal[3]*1.01 or df.loc[i, 'Close']<= signal[3]*0.90 or (df.loc[i, 'Date']-signal[1])>timedelta(days=5):
                signal = ['HSI', df.loc[i, 'Date'], 'Short',  df.loc[i+1, 'Open']]
                flag = 0
                signals.append(signal)
        elif flag ==2:
            if df.loc[i, 'Close']<= signal[3]*0.99 or df.loc[i, 'Close']>= signal[3]*1.10 or (df.loc[i, 'Date']-signal[1])>timedelta(days=5):
                signal = ['HSI', df.loc[i+1, 'Date'], 'Long',  df.loc[i+1, 'Close']]
                flag = 0
                signals.append(signal)

    sig = pd.DataFrame(signals, columns=['Code', 'Time', 'Action',  'Price'])
    print sig['Time'][10]-sig['Time'][0]
    profits = []
    print sig
    for k in range(0,len(signals)/2):
        if sig['Action'][k*2] == "Long":
            profit = sig['Price'][k*2+1] - sig['Price'][k*2]
        else:
            profit = sig['Price'][k*2]- sig['Price'][k*2+1]
        profits.append(profit)
    print np.sum(profits)
    print(profits)
    ###### PLOT #######
    longSignals = sig[sig['Action'] == 'Long']
    shortSignals = sig[sig['Action'] == 'Short']
    plt.plot(df['Date'], df['Close'], longSignals['Time'], longSignals['Price'], 'r^', shortSignals['Time'],
             shortSignals['Price'], 'gv', markersize=10)
    red_patch = mpatches.Patch(color='red', label='Long')
    green_patch = mpatches.Patch(color='green', label='Short')
    plt.legend(handles=[red_patch, green_patch])
    plt.grid()
    plt.show()
    ###### PLOT #######



if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)
    pd.set_option("display.max_rows", 280)
    dt = Data()
    df = dt.getCSVData()
    #ACOscillator(df)
    DM_RSI_ADX(df)