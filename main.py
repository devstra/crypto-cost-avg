import krakenex
from datetime import datetime

kraken = krakenex.API()
coin = "XXBTZEUR"
monthly_investment = 500.0 # in euros or whatever coin is in

# interval 15 days, since december 31, 2015
bitcoin_ohlc = kraken.query_public("OHLC",
{"pair": coin, "interval":21600,"since":1451520000})

# result format (<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)

coin_price = kraken.query_public("Ticker",{"pair":coin})
latest_price = float(coin_price["result"][coin]["c"][0])

if len(bitcoin_ohlc["error"]) == 0:
    price_history = bitcoin_ohlc["result"][coin]
    nb_months = 0
    coin_amount = 0.0
    
    for index, price in enumerate(price_history):
    # if even number
        if (index % 2) == 0:
            nb_months = nb_months + 1
            coin_amount = coin_amount + monthly_investment/float(price[4])

    roi = (coin_amount*latest_price)/(monthly_investment*nb_months)
    print("First investment: {}".format(datetime.utcfromtimestamp(1451520000).strftime('%d %B %Y')))
    print("Months of investment: {}".format(nb_months))
    print("Total investment: {} €".format(monthly_investment*nb_months))
    print("Total coin amount: {} {}".format(coin_amount, coin))
    print("Current portfolio value: {} €".format(coin_amount*latest_price))
    print("Return on investment: {} %".format(roi*100))
else:
    print(bitcoin_ohlc["error"])

