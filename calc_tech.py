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
    # willr = talib.WILLR(ph, pl, pc, 14)[-1]
    stochrsi = talib.STOCHRSI(pc, 14)[0][-1]
    uo = talib.ULTOSC(ph, pl, pc)[-1]
    roc = pc[-1] / pc[-2] - 1
    sar = talib.SAR(ph, pl)[-1]

    plusDI = talib.PLUS_DI(ph, pl, pc, 14)[-1]
    minusDI = talib.MINUS_DI(ph, pl, pc, 14)[-1]
    adx *= (lambda x: 1 if x>0 else -1 if x<0 else 0)(plusDI - minusDI)

    # print(ma, ema, macd, rsi, stoch, adx, cci, stochrsi, uo, roc, sar)
    return [ma, ema, macd, rsi, stoch, adx, cci, stochrsi, uo, roc, sar]


def make_indicators_dict(li, fmt):
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
        'stochrsi': li[7],
        'uo': li[8],
        'roc': li[9],
        'sar': li[10],
        'ma5_str': fmt.format(li[0][0]),
        'ma10_str': fmt.format(li[0][1]),
        'ma20_str': fmt.format(li[0][2]),
        'ma50_str': fmt.format(li[0][3]),
        'ma100_str': fmt.format(li[0][4]),
        'ema5_str': fmt.format(li[1][0]),
        'ema10_str': fmt.format(li[1][1]),
        'ema20_str': fmt.format(li[1][2]),
        'ema50_str': fmt.format(li[1][3]),
        'ema100_str': fmt.format(li[1][4]),
        'sar_str': fmt.format(li[10]),
        'adx_str': '{:.2f}'.format(abs(li[5]))
    }
    return indic_data



# fdt = datetime.datetime.strptime('2017-06-09 19:00:00', '%Y-%m-%d %H:%M:%S')
# ft_apistr = api.datetime_to_str(fdt)
# df = get_hist_df('USD_JPY', 'M1', count=100, fromTime=ft_apistr)
# print(df.tail())

pairs = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'AUD_USD', 'NZD_USD', 'USD_CHF', 'USD_CAD']
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

ccy_cn = {'EUR': '欧元',
          'USD': '美元',
          'JPY': '日元',
          'GBP': '英镑',
          'AUD': '澳元',
          'NZD': '新西兰元',
          'CHF': '瑞士法郎',
          'CAD': '加拿大元'}


def trend_comment(x, c):
    if x < c:
        return '偏空'
    elif x > c:
        return '偏多'
    else:
        return '中性'

def range_comment(x, d2, d1, u1, u2):
    if x > u2:
        return '超买'
    elif x > u1 and x <= u2:
        return '偏多'
    elif x > d1 and x <= u1:
        return '中性'
    elif x > d2 and x <= d1:
        return '偏空'
    else:
        return '超卖'


def adx_comment(x):
    if x > 20:
        return '偏多'
    elif x < -20:
        return '偏空'
    else:
        return '中性'


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

    px_fmt = '{:.2f}' if pair[-3:] == 'JPY' else '{:.4f}'
    data = make_indicators_dict(indicators, px_fmt)
    data['pair'] = pair.replace('_', '')
    data['ccy1'] = pair[:3]
    data['ccy2'] = pair[-3:]
    data['ccy1_cn'] = ccy_cn[data['ccy1']]
    data['ccy2_cn'] = ccy_cn[data['ccy2']]

    data['last_px'] = px_fmt.format(px)
    data['chg'] = px_fmt.format(px - pre_px)
    data['chgpct'] = '{:.3%}'.format(px/pre_px-1)
    if px > pre_px:
        data['arrow_pic'] = 'arrow-up_red.png'
    elif px < pre_px:
        data['arrow_pic'] = 'arrow-down_green.png'
    else:
        data['arrow_pic'] = 'arrow-right_blue.png'

    data['shit'] = 'shit'
    data['shit2'] = 'shit2'

    data['ma5_comment'] = trend_comment(px, data['ma5'])
    data['ma10_comment'] = trend_comment(px, data['ma10'])
    data['ma20_comment'] = trend_comment(px, data['ma20'])
    data['ma50_comment'] = trend_comment(px, data['ma50'])
    data['ma100_comment'] = trend_comment(px, data['ma100'])
    data['ema5_comment'] = trend_comment(px, data['ema5'])
    data['ema10_comment'] = trend_comment(px, data['ema10'])
    data['ema20_comment'] = trend_comment(px, data['ema20'])
    data['ema50_comment'] = trend_comment(px, data['ema50'])
    data['ema100_comment'] = trend_comment(px, data['ema100'])
    data['macd_comment'] = trend_comment(data['macd'], 0)
    data['rsi_comment'] = range_comment(data['rsi'], 30, 45, 55, 70)
    data['stoch_comment'] = range_comment(data['stoch'], 20, 45, 55, 80)
    data['adx_comment'] = adx_comment(data['adx'])
    data['cci_comment'] = range_comment(data['cci'], -150, -50, 50, 150)
    data['stochrsi_comment'] = range_comment(data['stochrsi'], 0.2, 0.45, 0.55, 0.8)
    data['uo_comment'] = trend_comment(data['uo'], 50)
    data['roc_comment'] = trend_comment(data['roc'], 0)
    data['sar_comment'] = trend_comment(px, data['sar'])
    gen_indicators_html.gen_html_pic(data, filename)


def gen_mkt_snapshot(save_dir):
    filename = 'snapshot.csv'
    csv_file = save_dir + filename
    with open(csv_file, 'w') as f:
        for pair in pairs:
            f.write('{},{},{:.3%}\n'.format(
                pair.replace('_', ''),
                fxdfs[(pair, 'D')].close[-1],
                fxdfs[(pair, 'D')].close[-1]/fxdfs[(pair, 'D')].close[-2] - 1))



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

    gen_mkt_snapshot(output_dir)
    time.sleep(10)


for t in threads:
    t.join()
