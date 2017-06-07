import pandas as pd
import talib
import tushare as ts

# sample testing df
sym = '000001'
freq = '60'

df = ts.get_hist_data(sym, ktype=freq)
df = df.sort_index()
# to be changed to v20 fx df

po = df.open.values
ph = df.high.values
pl = df.low.values
pc = df.close.values

ma = []
ema = []
for i in [5, 10, 20, 50, 100]:
    ma.append(talib.MA(pc, i)[-1])
    ema.append(talib.EMA(pc, i)[-1])

macd = talib.MACD(pc)[2][-1]
rsi = talib.RSI(pc, 14)[-1]
stoch = talib.STOCH(ph, pl, pc, 9, 6)[0][-1]
adx = talib.ADX(ph, pl, pc, 14)[-1]
cci = talib.CCI(ph, pl, pc, 14)[-1]
willr = talib.WILLR(ph, pl, pc, 14)[-1]
uo = talib.ULTOSC(ph, pl, pc)[-1]
roc = pc[-1] / pc[-2] - 1
sar = talib.SAR(ph, pl)[-1]
atr = talib.ATR(ph, pl, pc, 14)[-1]

print(macd, rsi, stoch, adx, cci, willr, uo, roc, sar, atr)
