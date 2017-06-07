import pandas as pd
import talib
import tushare as ts
import v20

# sample testing df
# sym = '000001'
# freq = '60'

# df = ts.get_hist_data(sym, ktype=freq)
# df = df.sort_index()
# to be changed to v20 fx df

api = v20.Context(
    hostname='api-fxpractice.oanda.com',
    port=443,
    ssl=True,
    token='4d71e20d7e302fc02a69ba841a6b2c43-e1e062a933506b9a2354889ddad91e9e'
)

instrument = 'USD_JPY'

params = {
    "granularity": 'M30',
    "smooth": None,
    "count": None,
    "fromTime": None,
    "toTime": None,
    "alignmentTimezone": None,
    # "price": 'mid'
}

req_count = 0
req_status = 0
while req_status != 200 and req_count < 3:
    print('request trial ', req_count)
    try:
        response = api.instrument.candles(instrument, **params)
        req_status = response.status
    except Exception:
        pass
    req_count += 1

candles = response.get("candles", 200)

df = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close'])

for c in candles:
    df = df.append(
        {'time': c.time,
         'open': c.mid.o,
         'high': c.mid.h,
         'low': c.mid.l,
         'close': c.mid.c},
        ignore_index=True)
    # df.append(pd.DataFrame([c.time, c.mid.o, c.mid.h, c.mid.l, c.mid.c],
    #                        columns=['time', 'open', 'high', 'low', 'close']))

print(df)

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

print(ma, ema, macd, rsi, stoch, adx, cci, willr, uo, roc, sar, atr)
