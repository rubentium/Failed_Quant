import pandas as pd

data = pd.read_csv("C:\\Users\\ruben\\Downloads\\HistoricalPrices.csv")
#print(data.shape)
match = 0
mismatch = 0
count = 257

closeYy = 257

openTy = 256

closeTy = 256


while count > 0:
    closeY = data.iloc[closeYy,1]
    openT = data.iloc[openTy,3]
    closeT = data.iloc[closeTy,3]
    
    if closeY < openT < closeT or closeY > openT > closeT:
        match +=1
        count -=1
        
        closeYy -=1
        openTy -=1
        closeTy -=1
    else:  
         mismatch +=1
         count -=1
         closeYy -=1
         openTy -=1
         closeTy -=1
total =match + mismatch
print(match)
print(mismatch)
print(total)
print(match*100/total)
