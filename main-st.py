import krakenex
import streamlit as st
from datetime import datetime
import time

kraken = krakenex.API()

# define UI elements
asset_pair = st.selectbox(
    "Which asset pair did you invest in?",
    [
        "AAVEEUR",
        "ADAEUR",
        "ALGOEUR",
        "ANTEUR",
        "ATOMEUR",
        "BALEUR",
        "BATEUR",
        "BCHEUR",
        "COMPEUR",
        "CRVEUR",
        "DAIEUR",
        "DASHEUR",
        "DOTEUR",
        "EOSEUR",
        "FILEUR",
        "FLOWEUR",
        "GNOEUR",
        "GRTEUR",
        "ICXEUR",
        "KAVAEUR",
        "KEEPEUR",
        "KNCEUR",
        "KSMEUR",
        "LINKEUR",
        "LSKEUR",
        "MANAEUR",
        "NANOEUR",
        "OMGEUR",
        "OXTEUR",
        "PAXGEUR",
        "QTUMEUR",
        "REPV2EUR",
        "SCEUR",
        "SNXEUR",
        "STORJEUR",
        "TBTCEUR",
        "TRXEUR",
        "UNIEUR",
        "USDCEUR",
        "USDTEUR",
        "WAVESEUR",
        "XDGEUR",
        "ETCEUR",
        "ETHEUR",
        "LTCEUR",
        "MLNEUR",
        "REPEUR",
        "XTZEUR",
        "XBTEUR",
        "XLMEUR",
        "XMREUR",
        "XRPEUR",
        "ZECEUR",
        "YFIEUR",
    ],
)
investment_frequency = st.selectbox(
    "How frequently did you invest?", ["every month", "every 2 weeks", "every week"]
)
recurring_investment = st.number_input(
    "How much did you invest every time? (€)", min_value=1
)
start_date = st.date_input("When did you start investing?")
submit_button = st.button("Calculate profits")


def date_to_timestamp(value: datetime.date) -> int:
    return int(time.mktime(value.timetuple()))


def get_ohlc_data(asset_pair, start_date):
    return kraken.query_public(
        "OHLC", {"pair": asset_pair, "interval": 1440, "since": 1451520000}
    )


def get_frequency(freq: str):
    if freq == "every month":
        return 30
    elif freq == "every 2 weeks":
        return 15
    elif freq == "every week":
        return 7


def calculate_profits():
    first_investment_date = date_to_timestamp(start_date)
    ohlc_response = get_ohlc_data(asset_pair, first_investment_date)
    ohlc_data = ohlc_response["result"][asset_pair]
    frequency = get_frequency(investment_frequency)
    recurring_amount = float(recurring_investment)
    coin_amount = 0.0
    nb_investments = 0

    for index, price in enumerate(ohlc_data):
        # if even number
        if (index % frequency) == 0:
            coin_amount = coin_amount + recurring_amount / float(price[4])
            nb_investments = nb_investments + 1

    current_value = coin_amount * float(ohlc_data[-1][4])
    total_cost = float(nb_investments) * recurring_amount
    roi = current_value / total_cost
    return {
        "coin_amount": coin_amount,
        "current_value": current_value,
        "total_cost": total_cost,
        "roi": roi,  # x100 to get %
    }


# need to convert it to float for calculs

# interval 15 days, since december 31, 2015
# coin_ohlc = kraken.query_public(
#     "OHLC", {"pair": coin, "interval": 1440, "since": 1451520000}
# )  # CHANGE INTERVAL TO 1440 TO GET DAILY OHLC DATA. NEEDED TO BE MORE PRECISE 1 ADD NEW FEATURES

# result format (<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)

# coin_price = kraken.query_public("Ticker", {"pair": coin}) # this is no longer needed. i can just use last day's price
# latest_price = float(coin_price["result"][coin]["c"][0])

# if len(coin_ohlc["error"]) == 0:
#     price_history = coin_ohlc["result"][coin]
#     nb_months = 0
#     coin_amount = 0.0

#     for index, price in enumerate(price_history):
#         # if even number
#         if (index % 2) == 0:
#             nb_months = nb_months + 1
#             coin_amount = coin_amount + monthly_investment / float(price[4])

#     roi = (coin_amount * latest_price) / (monthly_investment * nb_months)
#     st.write(
#         "First investment: {}".format(
#             datetime.utcfromtimestamp(coin_ohlc["result"][coin][0][0]).strftime(
#                 "%d %B %Y"
#             )
#         )
#     )
#     st.write("Months of investment: {}".format(nb_months))
#     st.write("Total investment: {:.2f} €".format(monthly_investment * nb_months))
#     st.write("Total coin amount: {:.8f} {}".format(coin_amount, coin))
#     st.write("Current portfolio value: {:.2f} €".format(coin_amount * latest_price))
#     st.write("Return on investment: {:.2f} %".format(roi * 100))
# else:
#     st.write(coin_ohlc["error"])
if submit_button:
    st.write(calculate_profits())