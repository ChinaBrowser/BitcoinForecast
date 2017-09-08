import requests
import time

maxs =[]
mins =[]

def loadData(f_name):
        data    = f_name.read().split("\n")
        data = data[:len(data)-1]
        label = []
        for i in range(len(data)):
                data[i] = data[i].split(",")
                data[i] = [float(x) for x in data[i]]
                label.append(data[i][len(data[i])-1])
                data[i] = data[i][0:len(data[i])-1]
        return data[2:],label[:-2]    #Removing first two and last two so each X[i] tries to predict Y[i+2] (i've used i+2 and not to i+1 to force it to predict the future (O) )

def reduceVector(vec,getVal=False):
        vect = []
        mx,mn = max(vec),min(vec)
        mx = mx+mn
        mn = mn-((mx-mn)*0.4)
        for x in vec:
                vect.append((x-mn)/(mx-mn))
        if not getVal:return vect
        else:return vect,mx,mn

def reduceValue(x,mx,mn):
        return (x-mn)/(mx-mn)

def augmentValue(x,mx,mn):
        return (mx-mn)*x+mn

def reduceMatRows(data):
        l = len(data[0])
        for i in range(l):
                v = []
                for t in range(len(data)):
                        v.append(data[t][i])
                v,mx,mn = reduceVector(v,getVal=True)
                maxs.append(mx)
                mins.append(mn)
                for t in range(len(data)):
                        data[t][i] = v[t]

        return data
def reduceCurrent(data):
        for i in range(len(data)):
                data[i] = reduceValue(data[i],maxs[i],mins[i])
        return data

def getCurrentData(label=False):
    data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()[0]
    poloniex_data = requests.get("https://poloniex.com/public?command=returnTicker").json()
    ts = int(time.time())-900
    ts2 = int(time.time())-86400
    chart_request = "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=%d&end=9999999999&period=900" % ts
    chart_request2 = "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=%d&end=9999999999&period=86400" % ts2
    poloniex_chart = requests.get(chart_request).json()[0]
    poloniex_chart2 = requests.get(chart_request2).json()[0]
    vect = []
    data_usdlast = "%.2f" % float(poloniex_data["USDT_BTC"]["last"])
    data_15m = "%.2f" % float(poloniex_chart2["weightedAverage"])
    vect.append(float(data_usdlast))
    vect.append(float(poloniex_data["USDT_BTC"]["baseVolume"]))
    vect.append(float(data["market_cap_usd"]))
    vect.append(float(data["total_supply"]))
    vect.append(float(data["total_supply"]))
    vect.append(float(data["percent_change_1h"]))
    vect.append(float(data["percent_change_24h"]))
    vect.append(float(data["percent_change_7d"]))
    vect.append(float(poloniex_chart2["quoteVolume"]))
    vect.append(float(data_15m))
    data_usdlowest = "%.2f" % float(poloniex_data["USDT_BTC"]["lowestAsk"])
    data_usdhighest = "%.2f" % float(poloniex_data["USDT_BTC"]["highestBid"])
    data_usdclose = "%.2f" % float(poloniex_chart["close"])
    vect.append(float(data_usdlowest))
    vect.append(float(data_usdhighest))
    vect.append(float(data_usdclose))

    if label:
        return vect,float(data_15m)
    return vect
