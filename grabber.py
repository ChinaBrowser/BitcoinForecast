#!/usr/bin/python3

##
## run the code for about 2/3 days
##

import requests
import time

f_name = input("dataset name:")
f = open(f_name,"a")
keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
vals = [0]*len(keys)

while True:
    data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()[0]
    poloniex_data = requests.get("https://poloniex.com/public?command=returnTicker").json()
    ts = int(time.time())-900
    ts2 = int(time.time())-86400
    chart_request = "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=%d&end=9999999999&period=900" % ts
    chart_request2 = "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=%d&end=9999999999&period=86400" % ts2
    poloniex_chart = requests.get(chart_request).json()[0]
    poloniex_chart2 = requests.get(chart_request2).json()[0]
    f.write("{},{},{},{},{},{},{},{},{},{},".format("%.2f" % float(poloniex_data["USDT_BTC"]["last"]),poloniex_data["USDT_BTC"]["baseVolume"],data["market_cap_usd"],data["total_supply"],data["total_supply"],data["percent_change_1h"],data["percent_change_24h"],data["percent_change_7d"],poloniex_chart2["quoteVolume"],"%.2f" % float(poloniex_chart2["weightedAverage"])))
    f.write("{},{},{}".format("%.2f" % float(poloniex_data["USDT_BTC"]["lowestAsk"]),"%.2f" % float(poloniex_data["USDT_BTC"]["highestBid"]),"%.2f" % float(poloniex_chart["close"])))
    f.write("\n")
    f.flush()
    time.sleep(60)
