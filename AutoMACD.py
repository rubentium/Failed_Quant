
import pandas as pd

data = pd.read_csv("HistoricalQuotes.csv")

ema12 = 140.40  # 09/16/2010

ema26 = 134.66  # 09/16/2010

ema12before = 138.99  # 09/15/2010

ema26before = 133.58  # 09/15/2010

ema9start = 4.37 # 09/16/2010

closeRow = 2397  # for 09/17/2010

closeRowbefore = 2398  # 09/16/2010

OrderProfitShort = 0
OrderProfit = 0
orderOpen = 0
orderOpenShort = 0

while closeRow >= 0:
    

    ema12 = (data.iloc[closeRow, 3] * (2 / 13) + (ema12 * (1 - (2 / 13))))
    ema26 = (data.iloc[closeRow, 3] * (2 / 27) + (ema26 * (1 - (2 / 27))))

    ema26before = (data.iloc[closeRowbefore, 3] * (2 / 27) + (ema26before * (1 - (2 / 27))))
    ema12before = (data.iloc[closeRowbefore, 3] * (2 / 13) + (ema12before * (1 - (2 / 13))))

    ema1226 = ema12 - ema26
    
    ema1226before = ema12before - ema26before
    
    
    ema9before = (ema1226before/5) + ((ema9start*(1-2/10)))
    ema9start = ema9before
    ema9 = (ema1226/5) + ((ema9before*(1-(1/5))))
    
    print(data.iloc[closeRow, 0])
    #print(ema9before)
    #print(ema1226before)
    #print("%.2f" % ema9)
    #print("%.2f" % ema1226)
    
    
    if ema9before > ema1226before and ema9 <= ema1226:
        orderOpen = data.iloc[closeRow, 3]
        print("orderOpen " + str(orderOpen))
        closeRow -= 1
        closeRowbefore -= 1
        
    elif  orderOpen != 0 and ema9before < ema1226before and ema9 >= ema1226:
        orderClose = data.iloc[closeRow, 3]
        OrderProfit = orderClose - orderOpen
        print("orderClose " + str(orderClose))
        
        
    elif ema9before < ema1226before and ema9 >= ema1226:
        orderOpenShort = data.iloc[closeRow, 3]
        print("orderOpenShort " + str(orderOpenShort))
        closeRow -= 1
        closeRowbefore -= 1
        
    elif orderOpenShort !=0 and ema9before > ema1226before and ema9 <= ema1226:
        OrderCloseShort = data.iloc[closeRow, 3]
        OrderProfitShort = orderOpenShort - OrderCloseShort
        print("OrderCloseShort " + str(OrderCloseShort))
        
    
    closeRow -= 1
    closeRowbefore -= 1

    #print("%.2f" % ema9)   
    #print("Profit "+ str("%.2f" % Profit))
    #print(ema1226)
Profit = OrderProfitShort + OrderProfit
print("Profit "+ str("%.2f" % Profit))
    
