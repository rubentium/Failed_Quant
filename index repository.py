import yfinance as yf
import yahoo_fin.stock_info as si

security = "bce"
com = yf.Ticker(security)
column = list(com.history("3wk").Close)
positive = []
negative = []
print(com.history("3wk").Close)


for i in range(len(column)):
    x = column[len(column)-1-i]
    y = column[len(column)-2-i]
    
    if x-y >= 0 and len(column)-2-i != -1:
        positive.append(x-y)
    elif x-y < 0 and len(column)-2-i != -1:
         negative.append(abs(x-y))


period = len(column)
prim_avg_gain = sum(positive)/len(positive)
prim_avg_loss = sum(negative)/len(negative)

current = si.get_live_price(security) - column[len(column)-1]   #applicable to live trading only
if current >= 0:
    avg_gain = prim_avg_gain*(period-1) + current    #requires a revision
    avg_loss = prim_avg_loss*(period-1)

elif current < 0:
    avg_gain = prim_avg_gain*(period-1)
    avg_loss = (prim_avg_loss*(period-1) + current)     #requires a revision

rsi = 100 - (100/(1 + avg_gain/avg_loss))
print(rsi)