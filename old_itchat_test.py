import os
import time

import itchat
import pandas as pd
import requests
import talib
import tushare as ts
import numpy as np
import seaborn as sns

import btcore as bt
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    # 'font.size': 6
})
cnfont = FontProperties(
    fname="/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc", size=10)
sns.set_style('dark')


# generate symbol : name exch market fcode
symbol_info = pd.read_csv('/home/yiju/windows/mkt_data/symbol_info.csv', index_col=0)
stocknames = ts.get_today_all().set_index('code')['name']
for i in symbol_info.index:
    if i in stocknames.index:
        symbol_info.ix[i, 'name'] = stocknames[i]

cache_data = True
# load data in memory
if cache_data:
    fut_info = pd.read_csv('/home/yiju/windows/mkt_data/fut_info_df.csv', index_col=0)
    dfs = {}
    fut_path = '/home/yiju/windows/mkt_data/csv/data_fut_d1/'
    for prod in os.listdir(fut_path):
        df = pd.read_csv(fut_path + prod + '/' + prod + '_d1.csv')
        df = df.set_index('time')
        df.index = pd.to_datetime(df.index)
        df['preclose'] = df['close'].shift(1)
        df['adj_close'] = df['close']
        df = df.dropna()
        dfs[prod] = df
    stock_path = '/home/yiju/windows/mkt_data/csv/data_stock_d1/'
    for f in os.listdir(stock_path):
        sym = f.split('.')[0]
        df = pd.read_csv(stock_path + f)
        df = df.set_index('time')
        df.index = pd.to_datetime(df.index)
        df['preclose'] = df['adj_close'].shift(1)
        df = df.dropna()
        dfs[sym] = df

is_using_bot = False
lang_en = False


def rate(x):
    if x > 0:
        return 'Buy'
    else:
        return 'Sell'


def color_signal(val):
    color = 'red' if val == 'Buy' else 'green' if val == 'Sell' else 'black'
    return 'color: %s' % color


def parse_freq(fq):
    if fq in ['d', 'D', '日']:
        return 'D'
    elif fq in ['w', 'W', 'week', 'Week', '周']:
        return 'W'
    elif fq in ['m', 'M', 'month', 'Month', '月']:
        return 'M'
    elif fq in ['5', '5m', 'm5', '5min']:
        return '5'
    elif fq in ['15', '15m', 'm15', '15min']:
        return '15'
    elif fq in ['30', '30m', 'm30', '30min']:
        return '30'
    elif fq in ['60', '60m', 'm60', '60min', '1h', '1H', 'h1', 'H1']:
        return '60'


def save_table(sym, freq='D'):
    df = ts.get_hist_data(sym, ktype=freq)
    df = df.sort_index()
    px = df['close']
    ma_table = []
    for i in [5, 10, 20, 50, 100, 200]:
        mai = talib.MA(px.values, i)[-1]
        emai = talib.EMA(px.values, i)[-1]
        ma_table.append(['MA{}'.format(i),
                         mai,
                         rate(px[-1] - mai),
                         emai,
                         rate(px[-1] - emai)])
        # ma_table = pd.DataFrame(ma_table,
        # columns=[u'周期',u'均线',u'信号',u'Exp均线',u'Exp信号'])
    ma_table = pd.DataFrame(
        ma_table,
        columns=[
            u'Periods',
            u'MA',
            u'Signal',
            u'ExpMA',
            u'ExpSignal'])
    # ma_table = ma_table.set_index(u'Periods')

    freqdict = {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly',
                '5': '5min', '15': '15min', '30': '30min', '60': '60min'}
    fmt = ma_table.style.format("{:.2f}", subset=['MA', 'ExpMA']).set_caption(
        'Realtime Price relative to MAs\nSymbol:{}, LastPrice = {}, {}'.format(
            sym, px[-1], freqdict[freq])) \
        .applymap(color_signal)
    with open('a.html', 'w') as htmlout:
        htmlout.write(fmt.render())
    os.system(
        'CutyCapt --url=file:///home/yiju/weixin/a.html --out=ma.png --min-width=100 --min-height=100')


# @itchat.msg_register(itchat.content.TEXT)
def show_msg(msg):
    print(msg['FromUserName'] + ': ' + msg['Text'])


@itchat.msg_register(itchat.content.TEXT)
def show_ma(msg):
    global is_using_bot
    print(msg['FromUserName'] + ': ' + msg['Text'])
    cmd = msg['Text'].split()[0]
    if cmd.lower() in ['ma', '均线']:
        params = msg['Text'].split(' ')[1:]
        symbol = params[0]
        if len(params) == 1:
            save_table(symbol)
            time.sleep(0.1)
            itchat.send('@img@ma.png', msg['FromUserName'])

        elif len(params) == 2:
            freq = parse_freq(params[1])
            save_table(symbol, freq)
            time.sleep(0.1)
            itchat.send('@img@ma.png', msg['FromUserName'])
        else:
            return ('parameters error')

    elif cmd.lower() in ['bt', '回测']:
        args = msg['Text'].split(' ')[1:]
        if len(args) == 3:
            symbol = bt.get_proper_symbol(args[0])
            market = symbol_info.ix[symbol, 'market']
            name = symbol_info.ix[symbol, 'name']
            fast = int(args[1])
            slow = int(args[2])
            params = {'fast': fast, 'slow': slow}
            try:
                if cache_data:
                    df = dfs[symbol]
                else:
                    df = bt.read_raw_data(symbol, 'd1', 'csv')
                bt.calc_singals(df, params)
                if market == 'fut':
                    multi = fut_info.ix[symbol, 'contractmultiplier']
                    equity = bt.run_bt(df, output_level=2, const_volume=multi)
                    bt.btplot_ma(equity, df['adj_close'], fast, slow,
                                 symbol, name, market, lang_en=lang_en)
                elif market == 'stock':
                    equity = bt.run_bt(df, output_level=2, const_weight=1,
                                       long_only=True)
                    bt.btplot_ma(equity, df['adj_close'], fast, slow,
                                 symbol, name, market, ytick_pct=True,
                                 long_only=True, lang_en=lang_en)

                # plt.savefig('bt.png', bbox_inches='tight')
                plt.savefig('bt.png')
                plt.close()

                time.sleep(0.1)
                itchat.send('@img@bt.png', msg['FromUserName'])
            except Exception as e:
                print(e)
                return ('error')

        else:
            return ('parameters error')

    elif cmd.lower() in ['help', '帮助']:
        return ("""
                现开放两个展示功能。1.标的市场状态 2.策略回测表现
                1.发送消息“ma xxxxxx”，返回关于各条均线的当前快照，直观了解证券当前强弱。例如“ma 000002”，“均线 600000 5min" (5分钟周期)
                2.发送消息”bt xx.. 短周期 长周期"，返回根据快慢速均线交易的历史表现。可以测试期货或股票。例如"bt rb 5 20" (回测螺纹钢５日20日均线交叉策略), "回测 000002 10 30" (回测万科10日上穿30日均线买入结果)
                更多即时状态发送，概率回测，预约推送事件提醒及关注标的波动提醒将后续推出。
                """)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def show_msg(msg):
    # print(msg)
    print(msg['ActualNickName'] + ': ' + msg['Text'])


def re_run():
    itchat.run()


itchat.auto_login(enableCmdQR=2, hotReload=True, exitCallback=re_run)
itchat.run()

