import requests,time,re,os
from pprint import pprint
import pandas as pd
import pickle as pkl 
from company_symbols import symbols

#api key
ameritrade = 'ARPAFPLETLIMAIQCAWXC9F3UANNVOMR5'
url = "https://api.tdameritrade.com/v1/instruments"

start=0
end=500
files = []
while start<len(symbols):
  symbols_500 = symbols[start:end]
  payload = {'apikey': ameritrade,
            'symbol': symbols_500,
            'projection': 'fundamental'}
  results = requests.get(url,params=payload)
  data = results.json()
  filename = time.asctime()+".pkl"
  filename = re.sub('[ :]','_',filename)
  files.append(filename)
  with open(filename,'wb') as f:
    pkl.dump(data,f)
  start=end
  end+=500

data = []

for f in files:
  with open(f,'rb') as f_:
    info=pkl.load(f_)
  points=['symbol','netProfitMarginMRQ','peRatio','pegRatio','high52']
  for ticker in info.keys():
    tick = []
    for point in  points:
      tick.append(info[ticker]['fundamental'][point])
    data.append(tick)
  os.remove(f)

points=['Symbol','Net_Profit_Margin','PE','PEG','High52']
df_results = pd.DataFrame(data,columns=points)
print(df_results.head(100))

screen = df_results[(df_results['PEG'] < 1) & (df_results['PEG'] >0) & (df_results['PE'] > 9) & (df_results['Net_Profit_Margin'] > 22)]
screen.sort_values(['PEG'])
print(screen)