#!/usr/bin/python3

##
## run the code for about 2/3 days
##

import requests
import time

f_name = input("dataset name:")
f = open(f_name,"a")

while True:
    bter = requests.get("https://data.bter.com/api2/1/ticker/btc_cny").json()
    bter_trade = requests.get("http://data.bter.com/api2/1/tradeHistory/btc_cny").json()["data"]
    sell = 0
    buy = 0
    sell_sum = 0
    buy_sum = 0
    for i in range(0,29):
        if bter_trade[i]["type"] == "sell":
            sell = sell + 1
            sell_sum = sell_sum + bter_trade[i]["amount"]
        else:
            buy = buy + 1
            buy_sum = buy_sum + bter_trade[i]["amount"]
    
    f.write("{},{},{},{},{},{},{},{},{},{},{},{}".format(bter["last"],bter["lowestAsk"],bter["highestBid"],bter["percentChange"],bter["baseVolume"],bter["quoteVolume"],bter["high24hr"],bter["low24hr"],sell,buy,sell_sum,buy_sum))
    f.write("\n")
    f.flush()
    time.sleep(5*60)
