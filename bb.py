import pandas as pd
from statistics import stdev

data = pd.read_csv('ETH-USD.csv')
date = data['Date']
prices = data['Close']

def bb(prices=prices, length=20, mu=2):
    outlist = []
    for i in range(length, len(prices)+1):
        period = prices[i-length: i+1]
        sma = sum(period)/length
        stdv = stdev(period)
        outlist.append((sma, sma+mu*stdv, sma-mu*stdv))
    return outlist

account = 100000

class order:
    def __init__(self, price: float, date: str, index: int, type_ord: str) -> None: #type is either long or short
        self.entry_date = date
        self.entry_price = price
        self.type = type_ord
        self.price_index = index
        self.endprice = None
        self.enddate = None
        self.pnl = None
    
    def close(self, price: float, date: str, account) -> float:
        self.endprice = price
        self.enddate = date
        self.pnl = self.endprice - self.entry_price
        account += self.pnl
        return account

other_open_short = False
other_open_long = False
open_dict = {}
open_dict['short'], open_dict['long'] = [], []
bbr = bb()

for price_index in range(20, len(prices)+1):
    price = prices[price_index]
    if price >= bb()[price_index][1]*0.99 and not other_open_short:
        open_dict['short'].append(order(price, date[price_index], price_index, 'short'))
        other_open_short = True
    elif price <= bb()[price_index][2]*1.01 and not other_open_long:
        open_dict['long'].append(order(price, date[price_index], price_index, 'long'))
        other_open_long = True

    if other_open_short:
        open_short = open_dict['short'][0]
        if price < bb()[price_index][0] or price_index - open_short.price_index >= 10:
            open_short.close(price, date[price_index], account)
            open_dict['short'].remove(open_short)
            other_open_short = False

    if other_open_long:
        open_long = open_dict['long'][0]
        if price > bb()[price_index][0] or price_index - open_long.price_index >= 10:
            open_long.close(price, date[price_index], account)
            open_dict['long'].remove(open_long)
            other_open_long = False

print(account)