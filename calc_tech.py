import pandas as pd
import talib
import time
import threading
import datetime
# import tushare as ts
import v20

import gen_indicators_html

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

tz_offset = datetime.timedelta(hours=8)

def get_hist_df(instrument, granularity=None, count=None, fromTime=None, toTime=None):
    params = {
        "granularity": granularity,
        "smooth": None,
        "count": count,
        "fromTime": fromTime,
        "toTime": toTime,
        "alignmentTimezone": None
        # "price": 'mid'
    }
    req_count = 0
    req_status = 0
    while req_status != 200 and req_count < 3:
        # print('request trial ', req_count)
        try:
            response = api.instrument.candles(instrument, **params)
            req_status = response.status

            if req_status == 200:
                candles = response.get("candles", 200)

                df = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
                df.index.name = 'time'

                for c in candles:
                    df = df.append(pd.DataFrame({'open': c.mid.o,
                                                'high': c.mid.h,
                                                'low': c.mid.l,
                                                'close': c.mid.c},
                                                index=[pd.to_datetime(c.time) + tz_offset]),
                                ignore_index=False)

                return df
        except Exception:
            pass
        req_count += 1



def get_indicators(df):
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

    # print(ma, ema, macd, rsi, stoch, adx, cci, willr, uo, roc, sar, atr)
    return [ma, ema, macd, rsi, stoch, adx, cci, willr, uo, roc, sar, atr]


def make_indicators_dict(li):
    indic_data = {
        'ma5': li[0][0],
        'ma10': li[0][1],
        'ma20': li[0][2],
        'ma50': li[0][3],
        'ma100': li[0][4],
        'ema5': li[1][0],
        'ema10': li[1][1],
        'ema20': li[1][2],
        'ema50': li[1][3],
        'ema100': li[1][4],
        'macd': li[2],
        'rsi': li[3],
        'stoch': li[4],
        'adx': li[5],
        'cci': li[6],
        'willr': li[7],
        'uo': li[8],
        'roc': li[9],
        'sar': li[10],
        'atr': li[11]
    }
    return indic_data



# fdt = datetime.datetime.strptime('2017-06-09 19:00:00', '%Y-%m-%d %H:%M:%S')
# ft_apistr = api.datetime_to_str(fdt)
# df = get_hist_df('USD_JPY', 'M1', count=100, fromTime=ft_apistr)
# print(df.tail())

pairs = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'AUD_USD', 'NZD_USD', 'USD_CAD']
freqs = ['D', 'H1', 'M1']
pair_freqs = [(p, f) for p in pairs for f in freqs]
fxdfs = {k: None for k in pair_freqs}
print(fxdfs)


# init hist df
for pair, freq in fxdfs:
    # fxdfs[(pair, freq)] = get_hist_df(pair, freq, count=100, fromTime=ft_apistr)  # for testing
    fxdfs[(pair, freq)] = get_hist_df(pair, freq, count=100)
    print(pair, freq)
    print(fxdfs[(pair, freq)].tail())


# while 1:
#     t1 = time.time()
#     for (pair, freq), df in fxdfs.items():
#         # if dealing with sfc str:
#         # time_str = df.iloc[-1].time[:19]
#         # dt_last = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

#         dt_last = df.index[-1]
#         # df = get_hist_df(pair, 'M1', 100)
#         dt_now = datetime.datetime.now()
#         if (dt_now - dt_last) > datetime.timedelta(minutes=5):
#             from_t = api.datetime_to_str(dt_last + datetime.timedelta(minutes=1))
#             # df1 = get_hist_df(pair, freq, count=5, fromTime=from_t)  # for testing
#             df1 = get_hist_df(pair, freq, fromTime=from_t)
#             fxdfs[(pair, freq)] = df.append(df1)
#         else:
#             df1 = get_hist_df(pair, freq, count=5)  # re-fetch last 5, maybe 2 ok
#             fxdfs[(pair, freq)] = df.update(df1)

#         print(pair, freq)
#         print(fxdfs[(pair, freq)].tail())

#     time.sleep(1)


def stream_one(pair, freq):
    while 1:
        df = fxdfs[(pair, freq)]
        # if dealing with sfc str:
        # time_str = df.iloc[-1].time[:19]
        # dt_last = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

        dt_last = df.index[-1]
        dt_now = datetime.datetime.now()
        # if (dt_now - dt_last) > datetime.timedelta(minutes=5):
        #     from_t_val = dt_last + datetime.timedelta(minutes=1) - tz_offset
        #     from_t = api.datetime_to_str(from_t_val)
        #     # df1 = get_hist_df(pair, freq, count=5, fromTime=from_t)  # for testing
        #     df1 = get_hist_df(pair, freq, fromTime=from_t)
        #     fxdfs[(pair, freq)] = df.append(df1)
        # else:
        #     df1 = get_hist_df(pair, freq, count=5)  # re-fetch last 5, maybe 2 ok
        #     fxdfs[(pair, freq)] = pd.concat([df[~df.index.isin(df1.index)], df1])
        #     print(pair, freq)
        #     print(fxdfs[(pair, freq)].tail())
        from_t = api.datetime_to_str(dt_last - tz_offset)
        df1 = get_hist_df(pair, freq, fromTime=from_t)
        fxdfs[(pair, freq)] = pd.concat([df[~df.index.isin(df1.index)], df1])

        time.sleep(0.1)


output_dir = './output/'


def gen_pic(save_dir, pair, freq, px, pre_px, indicators, dt_last):
    filename = '{}_{}'.format(pair.replace('_', ''), freq)
    csv_file = save_dir + filename + '.csv'
    string = []
    # string.append(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    string.append(str(datetime.datetime.now())[:19])
    string.append(dt_last)
    string.append(str(px))
    string.append(str(pre_px))
    for x in indicators:
        if isinstance(x, list):
            for xi in x:
                string.append('{:.4f}'.format(xi))
        else:
            string.append('{:.4f}'.format(x))
    with open(csv_file, 'w') as f:
        f.write(','.join(string))

    data = make_indicators_dict(indicators)
    data['shit'] = 'shit'
    data['shit2'] = 'shit2'
    gen_indicators_html.gen_html_pic(data, filename)


threads = []
for p, f in fxdfs.keys():
    t = threading.Thread(target=stream_one, args=(p, f))
    threads.append(t)
    t.start()


while 1:
    for p, f in fxdfs.keys():
        # print(p, f, "indicators")
        indicators = get_indicators(fxdfs[(p, f)])
        dt_last = str(fxdfs[(p, f)].index[-1])
        px = fxdfs[(p, 'D')].close[-1]
        pre_px = fxdfs[(p, 'D')].close[-2]
        # print(p, px, pre_px)
        # print(fxdfs[(p, 'D')].tail())
        t_pic = threading.Thread(
            target=gen_pic,
            args=(output_dir, p, f, px, pre_px, indicators, dt_last))
        t_pic.daemon = True
        t_pic.start()
    time.sleep(10)


for t in threads:
    t.join()
