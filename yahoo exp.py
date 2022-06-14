# WARNING!!! 
# THE DATA FEED IS FAULTY! 
# THE OPEN, HIGH, LOW DATA MAY (and probably will) BE DIFFERENT FROM THE ACTUAL
# THE CLOSING SHOULD BE THE SAME THOUGH.

# UPDATE!!! THE DATA FEED IS FINE BUT IF THERE IS AN ISSUE, USE YFINANCE (IT'S NOT INSTALLED) 

# VI turn this into a class -- DONE! 

import yahoo_fin.stock_info as si
from numpy import std
import datetime as dt
import time

d1 = dt.date(2020, 12, 24) - dt.timedelta(days=14)
d2 = dt.date(2020, 12, 24) + dt.timedelta(days=1)    #first and last days inclusive
#print(type(d1)) 
#print(dt.date.fromisoformat(d1),d2)
start = time.time()
class indicators():
    def __init__(self, security, start_date=d1, end_date=d2, index_as_date = True, interval = "1d"):

        self.columnC = list(si.get_data(security, start_date, end_date, index_as_date, interval).adjclose)
        self.columnH = list(si.get_data(security, start_date, end_date, index_as_date, interval).high)
        self.columnL = list(si.get_data(security, start_date, end_date, index_as_date, interval).low)
        self.period = len(self.columnC) # could also be high, low, or open. it doesn't matter
        self.security = security
        self.emaClosing = list(si.get_data(security, '2018-09-15', end_date, index_as_date, interval).adjclose) 

#-----------------------RSI----------------------- [should be OK]   [update: is NOT OK]

    def rsi(self):

        positive = []
        negative = []

        for i in range(len(self.columnC)):
            x = self.columnC[len(self.columnC)-1-i]
            y = self.columnC[len(self.columnC)-2-i]
            
            if x-y >= 0 and len(self.columnC)-2-i != -1:
                positive.append((x-y)/y*100)
            elif x-y < 0 and len(self.columnC)-2-i != -1:
                negative.append(abs(x-y)/y*100)

        prim_avg_gain = sum(positive)/len(positive)
        prim_avg_loss = sum(negative)/len(negative)

        current = si.get_live_price(self.security) - self.columnC[len(self.columnC)-1]   #applicable to live trading only
        if current >= 0:                                          #if the daily is a gain then loss avg is 0 and vice versa
            avg_gain = prim_avg_gain*(self.period-1) + current    #requires a revision
            avg_loss = prim_avg_loss*(self.period-1)

        elif current < 0:
            avg_gain = prim_avg_gain*(self.period-1)
            avg_loss = (prim_avg_loss*(self.period-1) + current)     #requires a revision

        rsi = round(100 - (100/(1 + avg_gain/avg_loss)), 2)
        return rsi


#----------------------Bollinger Bands---------------------- [is OK]
    def bb(self, m=2):      #standard is 2, can be changed

        # BOLU = SMA(TP, n) + m*σ[TP, n]
        # BOLU = SMA(TP, n) - m*σ[TP, n]
        # TP: tp = (high + low + close)/3

        # Note: BB is weird. The period is different when operating with different
        # exchanges. Ex: if period=14 some exchanges may include the weekends like Sydney
        # and some won't like NYSE 
        
        tp = []

        for i in range(self.period):
            tp.append((self.columnC[i] + self.columnH[i] + self.columnL[i]) / 3)

        sma = sum(tp)/len(self.columnC)   #middle band 
        standard_dev = std(tp)

        upper = round(sma + m*standard_dev, 2)      #upper band
        lower = round(sma - m*standard_dev, 2)      #lower band
        sma = round(sma, 2)
        return upper, sma, lower

    def test_ema(self): # [EMA works OK]

        positive = []
        negative = []

        for i in range(len(self.emaClosing)):
            x = self.emaClosing[len(self.emaClosing)-1-i]
            y = self.emaClosing[len(self.emaClosing)-2-i]
            
            if x-y >= 0 and len(self.emaClosing)-2-i != -1:
                positive.append((x-y)/y*100)
                

            elif x-y < 0 and len(self.emaClosing)-2-i != -1:
                negative.append(abs(x-y)/y*100)
                


        smaG = sum(positive[:5])/len(positive[:5])
        k = 2/5
        emaG = k*(positive[5] - smaG) + smaG           # ema part here is right
        emaG_list = []
        for e in positive [6:]:
            emaG = k*(e - emaG) + emaG
            emaG_list.append(emaG)


        smaL = sum(negative[:5])/len(negative[:5])
        emaL = k*(negative[5] - smaL) + smaL
        emaL_list = []
        for e in negative[6:]:
            emaL = k*(e - emaL) + emaL
            emaL_list.append(emaL)



        rsi = 100 - (100 / (1 + ( sum( emaG_list ) / len( emaG_list ) / ( sum ( emaL_list ) / len( emaL_list )))))
        
        return rsi






stock = indicators('cfw.to', '2020-12-07', '2020-12-25')
end = time.time()
print(stock.test_ema(), end-start)
print(si.get_data("gme", '2020-12-19', '2020-12-30'))