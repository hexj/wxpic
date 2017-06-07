#!/usr/bin/env python

# import common.config
# import common.args
# from .view import CandlePrinter
# from datetime import datetime

import v20

api = v20.Context(
    hostname='api-fxpractice.oanda.com',
    port=443,
    ssl=True,
    token='4d71e20d7e302fc02a69ba841a6b2c43-e1e062a933506b9a2354889ddad91e9e'
)

params = {
    "granularity": 'D',
    "smooth": None,
    "count": None,
    "fromTime": None,
    "toTime": None,
    "alignmentTimezone": None,
    # "price": 'mid'
}

response = api.instrument.candles('USD_JPY', **params)

candles = response.get("candles", 200)

for c in candles:
    print(c)
