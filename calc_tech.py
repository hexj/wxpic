import datetime
import os
import threading
import time

import gen_indicators_html
import gen_snapshot_html
import pandas as pd
import talib
import v20

api = v20.Context(
    hostname='api-fxpractice.oanda.com',
    port=443,
    ssl=True,
    token='4d71e20d7e302fc02a69ba841a6b2c43-e1e062a933506b9a2354889ddad91e9e'
)

tz_offset = datetime.timedelta(hours=8)

ccy_cn = {'EUR': '欧元',
          'USD': '美元',
          'JPY': '日元',
          'GBP': '英镑',
          'AUD': '澳元',
          'NZD': '新西兰元',
          'CHF': '瑞士法郎',
          'CAD': '加拿大元'}


def get_hist_df(instrument, granularity=None, count=None, fromTime=None,
                toTime=None):
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
    while req_status != 200 and req_count < 5:
        # print('request trial ', req_count)
        try:
            response = api.instrument.candles(instrument, **params)
            req_status = response.status

            if req_status == 200:
                candles = response.get("candles", 200)

                df = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
                df.index.name = 'time'

                for c in candles:
                    df = df.append(
                        pd.DataFrame({'open': c.mid.o,
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
    adx *= (lambda x: 1 if x > 0 else -1 if x < 0 else 0)(plusDI - minusDI)

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


last_feed_error_time = datetime.datetime.now()


def stream_one(pair, freq):
    global last_feed_error_time
    while 1:
        try:
            df = fxdfs[(pair, freq)]

            dt_last = df.index[-1]
            from_t = api.datetime_to_str(dt_last - tz_offset)
            df1 = get_hist_df(pair, freq, fromTime=from_t)
            fxdfs[(pair, freq)] = pd.concat([df[~df.index.isin(df1.index)], df1])
        except Exception as e:
            dt_now = datetime.datetime.now()
            print(pair, freq, '\033[41m' + str(dt_now)[:-7] + '   ',
                  str(dt_now - last_feed_error_time)[:-7] + '\033[0m')
            print(e)
            print(fxdfs[(pair, freq)].tail())
            last_feed_error_time = datetime.datetime.now()
        time.sleep(1)


def trend_comment(x, c):
    if x < c:
        return '偏空'
    elif x > c:
        return '偏多'
    else:
        return '中性'


def trend_cond_comment(x, c):
    if x < c * (1 - 3e-4):
        return '偏空'
    elif x > c * (1 + 3e-4):
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


def gen_data(pair, freq, px, pre_px, indicators):
    px_fmt = '{:.2f}' if pair[-3:] == 'JPY' else '{:.4f}'
    data = make_indicators_dict(indicators, px_fmt)
    data['pair'] = pair.replace('_', '')
    data['freq'] = freq
    data['ccy1'] = pair[:3]
    data['ccy2'] = pair[-3:]
    data['ccy1_cn'] = ccy_cn[data['ccy1']]
    data['ccy2_cn'] = ccy_cn[data['ccy2']]
    dict_freqcn = {'D': '日线', 'W': '周线', 'M': '月线',
                   'H1': '1小时', 'H4': '4小时', 'H8': '8小时',
                   'M1': '1分钟', 'M5': '5分钟', 'M10': '10分钟', 'M15': '15分钟',
                   'M30': '30分钟'}
    data['freq_cn'] = dict_freqcn[freq]

    data['last_px'] = px_fmt.format(px)
    data['chg'] = px_fmt.format(px - pre_px)
    data['chgpct'] = '{:.3%}'.format(px / pre_px - 1)
    if px > pre_px:
        data['chgcolor'] = 'redFont'
    elif px < pre_px:
        data['chgcolor'] = 'greenFont'
    else:
        data['chgcolor'] = ''

    if px > pre_px:
        data['arrow_pic'] = 'arrow-up_red.png'
    elif px < pre_px:
        data['arrow_pic'] = 'arrow-down_green.png'
    else:
        data['arrow_pic'] = 'arrow-right_blue.png'

    data['ma5_comment'] = trend_cond_comment(px, data['ma5'])
    data['ma10_comment'] = trend_cond_comment(px, data['ma10'])
    data['ma20_comment'] = trend_cond_comment(px, data['ma20'])
    data['ma50_comment'] = trend_cond_comment(px, data['ma50'])
    data['ma100_comment'] = trend_cond_comment(px, data['ma100'])
    data['ema5_comment'] = trend_cond_comment(px, data['ema5'])
    data['ema10_comment'] = trend_cond_comment(px, data['ema10'])
    data['ema20_comment'] = trend_cond_comment(px, data['ema20'])
    data['ema50_comment'] = trend_cond_comment(px, data['ema50'])
    data['ema100_comment'] = trend_cond_comment(px, data['ema100'])
    data['macd_comment'] = trend_comment(data['macd'], 0)
    data['rsi_comment'] = range_comment(data['rsi'], 30, 45, 55, 70)
    data['stoch_comment'] = range_comment(data['stoch'], 20, 45, 55, 80)
    data['adx_comment'] = adx_comment(data['adx'])
    data['cci_comment'] = range_comment(data['cci'], -150, -50, 50, 150)
    data['stochrsi_comment'] = range_comment(data['stochrsi'], 0.2, 0.45, 0.55,
                                             0.8)
    data['uo_comment'] = trend_comment(data['uo'], 50)
    data['roc_comment'] = trend_comment(data['roc'], 0)
    data['sar_comment'] = trend_comment(px, data['sar'])

    n_long1, n_short1, n_neu1, n_long2, n_short2, n_neu2, n_ob, n_os = 0, 0, 0, 0, 0, 0, 0, 0
    for k, v in data.items():
        if v == '偏多':
            if (k.startswith('ma') or k.startswith('ema')) and not k.startswith('macd'):
                n_long1 += 1
            else:
                n_long2 += 1
        elif v == '偏空':
            if (k.startswith('ma') or k.startswith('ema')) and not k.startswith('macd'):
                n_short1 += 1
            else:
                n_short2 += 1
        elif v == '中性':
            if (k.startswith('ma') or k.startswith('ema')) and not k.startswith('macd'):
                n_neu1 += 1
            else:
                n_neu2 += 1
        elif v == '超买':
            n_ob += 1
        elif v == '超卖':
            n_os += 1

    data['n_long1'] = n_long1
    data['n_short1'] = n_short1
    data['n_neu1'] = n_neu1
    data['n_long2'] = n_long2
    data['n_short2'] = n_short2
    data['n_neu2'] = n_neu2
    data['n_ob'] = n_ob
    data['n_os'] = n_os

    img_up = '<img src="arrow-up_red.png" style="width:20px; height:20px; margin-bottom: -7px; margin-right: -5px"/>'
    img_down = '<img src="arrow-down_green.png" style="width:20px; height:20px; margin-bottom: -7px; margin-right: -5px"/>'
    if n_neu1 >= 7:
        data['summary1'] = '中性'
    elif n_neu1 == 6 and n_long1 - n_short1 >= 2:
        data['summary1'] = '偏多' + img_up
    elif n_neu1 == 6 and n_long1 - n_short1 <= -2:
        data['summary1'] = '偏空' + img_down
    elif n_neu1 <= 5 and n_long1 - n_short1 >= 4:
        data['summary1'] = '偏多' + img_up * 2
    elif n_neu1 <= 5 and n_long1 - n_short1 <= -4:
        data['summary1'] = '偏空' + img_down * 2
    elif n_neu1 <= 5 and n_long1 - n_short1 < 4 and n_long1 - n_short1 >= 2:
        data['summary1'] = '偏多' + img_up
    elif n_neu1 <= 5 and n_long1 - n_short1 > -4 and n_long1 - n_short1 <= -2:
        data['summary1'] = '偏空' + img_down
    else:
        data['summary1'] = '中性'

    if n_long2 - n_short2 >= 4:
        data['summary2'] = '偏多' + img_up * 2
    elif n_long2 - n_short2 < 4 and n_long2 - n_short2 > 0:
        data['summary2'] = '偏多' + img_up
    elif n_long2 - n_short2 <= -4:
        data['summary2'] = '偏空' + img_down * 2
    elif n_long2 - n_short2 > -4 and n_long2 - n_short2 < 0:
        data['summary2'] = '偏空' + img_down
    else:
        data['summary2'] = '中性'

    px_data = []
    for i in range(12):
        px_data.append([i, fxdfs[(pair, freq)].close[-12 + i]])
    data['px_data'] = str(px_data)

    return data


def gen_single_pic(save_dir, pair, freq):
    indicators = get_indicators(fxdfs[(pair, freq)])
    dt_last = str(fxdfs[(pair, freq)].index[-1])
    px = fxdfs[(pair, 'D')].close[-1]
    pre_px = fxdfs[(pair, 'D')].close[-2]

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

    data = gen_data(pair, freq, px, pre_px, indicators)
    gen_indicators_html.gen_html_pic(data, filename)


def gen_mkt_snapshot(save_dir):
    filename = 'snapshot.csv'
    csv_file = save_dir + filename
    with open(csv_file, 'w') as f:
        for pair in pairs:
            f.write('{},{},{:.3%}\n'.format(
                pair.replace('_', ''),
                fxdfs[(pair, 'D')].close[-1],
                fxdfs[(pair, 'D')].close[-1] / fxdfs[(pair, 'D')].close[-2] - 1))


def gen_snapshot_pic(filename):
    out_html = gen_snapshot_html.html
    for pair in pairs:
        indicators = get_indicators(fxdfs[(pair, 'H1')])
        px = fxdfs[(pair, 'D')].close[-1]
        pre_px = fxdfs[(pair, 'D')].close[-2]
        data = gen_data(pair, 'H1', px, pre_px, indicators)
        out_html += gen_snapshot_html.html2.format(**data)
    out_html += gen_snapshot_html.html3

    with open(output_dir + filename + '.html', 'w') as f:
        f.write(out_html)

    html_url = 'file:///home/yiju/wxfx/wxpic/output/{}.html'.format(filename)
    pic_path = './output/{}.png'.format(filename)
    os.system(
        'CutyCapt --url={} --out={} --min-width=900 --zoom-factor=3.0'.format(
            html_url, pic_path))


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
    print(pair, freq, datetime.datetime.now())
    print(fxdfs[(pair, freq)].tail())

threads = []
for p, f in fxdfs.keys():
    t = threading.Thread(target=stream_one, args=(p, f))
    threads.append(t)
    t.start()

output_dir = './output/'

while 1:
    for p, f in fxdfs.keys():
        t_pic = threading.Thread(target=gen_single_pic, args=(output_dir, p, f),
                                 daemon=True)
        t_pic.start()

    t_snapshot = threading.Thread(target=gen_snapshot_pic, args=('snapshot',),
                                  daemon=True)
    t_snapshot.start()
    gen_mkt_snapshot(output_dir)
    time.sleep(10)

# for t in threads:
#     t.join()
