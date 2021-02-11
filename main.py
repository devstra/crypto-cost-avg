import krakenex
import streamlit as st
from datetime import datetime
import time

kraken = krakenex.API()

# define UI elements
st.title("Cryptocurrency Cost Averaging Calculator")
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


@st.cache
def get_ohlc_data(asset_pair: str, start_date: int):
    return kraken.query_public(
        "OHLC", {"pair": asset_pair, "interval": 1440, "since": start_date}
    )


def get_frequency(freq: str) -> int:
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
        "roi": roi,
        "nb_of_investments": nb_investments,
        "first_investment_date": ohlc_data[0][0],
    }


def display_results(results):
    st.write(
        "Date of first investment: {}".format(
            datetime.utcfromtimestamp(result["first_investment_date"]).strftime(
                "%d %B %Y"
            )
        )
    )
    st.write("Number of BUY orders:    {}".format(result["nb_of_investments"]))
    st.write("Total investment cost:    {:.2f} €".format(result["total_cost"]))
    st.write(
        "Total asset amount:    {:.8f} {}".format(result["coin_amount"], asset_pair)
    )
    st.write("Current portfolio value:    {:.2f} €".format(result["current_value"]))
    st.write("Return on investment:    {:.2f} %".format(result["roi"] * 100))


if submit_button:
    result = calculate_profits()
    display_results(result)

st.text("Note: the asset pairs and price data are all in EUR and provided by Kraken.")