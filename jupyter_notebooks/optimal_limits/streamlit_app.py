import streamlit as st
import utils
import yfinance as yf
import numpy as np
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import datetime as datetime
from pytickersymbols import PyTickerSymbols
import pandas as pd
import math
from copy import deepcopy

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def get_symbol_by_company_name(company_name, companies):
    for company in companies:
        if company.get("name") == company_name:
            return company.get("symbols")[0].get("yahoo")
    return None  # or raise an error if preferred

@st.cache_data
def download_prices(symbol, days, start=None, end=None):
    stock =  yf.Ticker(symbol)
    if not start and not end:        
        # Determine minimal data
        df = stock.history(period="max")
        start_date = df.index.min()
        current_date = df.index.max()
    else:
        if not end:
            current_date = (datetime.datetime.today()  + datetime.timedelta(1))
        else:
            current_date = end
        if not start:
            start_date = stock.history(period="max").index.min()
        else:
            start_date = start
        df = stock.history(start=start_date, end=current_date)
    return df

@st.cache_data
def get_prices(symbol, days, start=None, end=None):
    df = download_prices(symbol, days, start, end)
    # Determine minimal date  
    price = df['Close']
    price = price.values

    if len(df)==0:
        st.write(f"There was an error downloading the data for {symbol}")
        return ([False], [0], [0], [0], [0], [datetime.date(2000,1,1)], 
            [0], #Here i need the full prices
            0, 0
            )
    mu_est, sigma_est = utils.compute_parameter(price ,price.size) # The last var is how many days we are looking at
    time = [x.date() for x in df.index] + [(df.index[-1].date() + 
                                           #datetime.timedelta(day) # Hier darf timedelta workday
                                           pd.tseries.offsets.BDay(day)).date()
                                           for day in days] #<- Days ahead darf nur auf eine Liste mit handelstagen angewendet werden

    days_ahead = np.array( list( range(0,price.size) )  + [day + price.size for day in days] )  #days ahead should be more dense
    trend = price[0]*np.exp( days_ahead *(mu_est -0.5*sigma_est**2))
    
    # construct an array of 0 for price length

    buy = [np.nan]*price.size
    sell = [np.nan]*price.size
    prop_buy = [np.nan]*price.size
    prop_sell = [np.nan]*price.size

    for day in days:  #atm we only get the last
        buy_d, sell_d, prop_buy_d, prop_sell_d = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], day)
        buy.append(buy_d)
        sell.append(sell_d)
        prop_buy.append(prop_buy_d)
        prop_sell.append(prop_sell_d)

    #buy, sell, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], days)   #10 days in advance
    return (trend, buy, sell, prop_buy, prop_sell, time, 
            np.array(list(price) + [np.nan]*len(days)), #Here i need the full prices
            mu_est, sigma_est
            )


st.markdown("""
# Stockmarket Oracle :wink:
At what price should i buy or sell a stock?
         
This app gives an indication how to set limits for a given stock based on [statistical insights](https://www.thebigdatablog.com/does-my-stock-trading-strategy-work/).
For a given stock the app will give you the expected maximal and minimal price based on the last trading day as reference as
well as the propability that the order is fullfilled for that price.
""")

stock_data = PyTickerSymbols()

col1, col2 = st.columns(2)

with col1:
    indexes = (
"DAX",
"AEX",
"BEL 20",
"CAC 40",
"DOW JONES",
"FTSE 100",
"IBEX 35",
"MDAX",
"NASDAQ 100",
"OMX Helsinki 15",
"OMX Helsinki 25",
"OMX Stockholm 30",
"S&P 100",
"S&P 500",
"SDAX",
"SMI",
"TECDAX",
"MOEX",
)
    index_choice = st.selectbox("Select an index", indexes)

with col2:
    german_stocks = stock_data.get_stocks_by_index(index_choice)
    choices = deepcopy(german_stocks) # [f["name"] for f in german_stocks]
    selected_stock = st.selectbox("Which stock do you want to analyze", choices, format_func= lambda x: x)

selected_stock = get_symbol_by_company_name(selected_stock, german_stocks)

if selected_stock=="DPW.F":
    selected_stock="DHL.DE"

#st.set_option('deprecation.showPyplotGlobalUse', False)

# st.write("What is your timeframe in days where you want to buy or sell your stock?")
# days_in_advance = st.number_input("What is your timeframe where you want to buy or sell your stock?", step = 1, value=5 )
#st.write("How many historical data do you want to use to fit the model?")

today = datetime.datetime.now()

d = st.date_input(
    "How many historical data do you want to use to fit the model?",
    (datetime.date(2000, 1, 1), today),
    datetime.date(2000, 1, 1),
    today,
    format="DD.MM.YYYY",
)

start_date = d[0]
end_date = d[1]

trend, buy, sell, prop_buy, prop_sell, time, price, mu, sigma= get_prices(selected_stock, [np.floor(x**2.5) for x in range(1,20) ], start_date, end_date) # stock 5 days ahead

if trend[0]:
    def convert_to_percentage(x):
        return [ str(round(y*100,2)) + ' %' for y in x]

    # Stockprice informations
    S0 = [np.round(item, 2) for item in list(price) if item is not None and not math.isnan(item)][-1]

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
            **Yahoo Symbol: {selected_stock}**

            $\hat{{\mu}}$= {mu} \n
            $\hat{{\sigma}}$= {sigma} \n
            $S_0$= {S0} € (reference price)
                """)

        with col2:
            st.write("""
                    
                    """)
            st.latex(r"S_t = S_0 \exp \left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t \right)"
                )


        result_df = pd.DataFrame({
            'Days in Advance (total)': [str( (day - datetime.datetime.now().date()).days +1 ) for day in time],
            'Trendbased price': trend,
            'Optimal buy limit': buy,
            'Propability to buy':  convert_to_percentage(prop_buy),
            'Optimal sell limit': sell,
            'Propability to sell': convert_to_percentage(prop_sell),
        })


    with st.container():
        st.markdown("**Price calculator**")

        col1, col2, col3, col4 = st.columns(4)

        sellbuy = "buy"

        with col1:
            sellbuy = st.radio(
                "Do you decide to buy or sell a stock?",
                ["Buy","Sell"])
            
            sellbuy = sellbuy.lower()

        with col2:
            target_price = st.number_input('Targetprice', value=S0)

        with col3:
            days = st.number_input(f"Timehorizont to {sellbuy} in workingdays", step=1, value=5 ) # Here we look at trading days, in the table days in total
            days = days

        with col4:
            try:
                mu_hat =  (mu - sigma**2/2)
                llambda = mu_hat/sigma**2

                if sellbuy =="buy":
                    prop =  1-utils.min_props(target_price, S0, mu_hat, sigma, llambda, days)
                else:
                    prop = utils.max_props(target_price, S0, mu_hat, sigma, llambda, days)
                prop = round(prop*100,2)
                #st.number_input(f"""Propability to {sellbuy}""", value=prop)
                st.write(f"""Propability to {sellbuy}: {prop}%""")
            except:
                st.write("Calculation not possible")

    with st.container():
        st.markdown("**Optimal prices**")

        # Results as Table

        styler = result_df[result_df["Optimal buy limit"].isnull()==False].style.hide().format('{0:,.2f} €', subset=['Trendbased price', 'Optimal buy limit','Optimal sell limit'], decimal=',', precision=2)#.bar(subset=['mean'], align="mid")
        st.write(styler.to_html(), unsafe_allow_html=True)

        stock =  yf.Ticker(selected_stock)
        df = stock.history(period="max")

        log_scale = st.checkbox('Log scale')

        if log_scale:
            price =np.log(price)
            buy =np.log(buy)
            sell =np.log(sell)
            trend =np.log(trend)
            df["Close"] = np.log(df["Close"])

        fig = go.Figure()
        fig0 = px.line(df, x=df.index, y="Close")

        fig1 = px.line({ "date": time, "stockprice": price}, x="date", y="stockprice")
        fig2 = px.line({ "date": time, "trend": trend}, x="date", y="trend")
        fig3 = px.scatter({ "date": time, "buy": buy, "propability" : prop_buy}, x="date", y="buy", color = "propability")
        fig4 = px.scatter({ "date": time, "sell": sell, "propability" : prop_sell}, x="date", y="sell", color = "propability")
        fig = go.Figure(data = fig0.data + fig1.data + fig2.data + fig3.data + fig4.data)
        fig.data[0].line.color = 'lightgrey'
        fig.data[1].line.color = 'blue'
        fig.data[2].line.color = 'orange'

        fig.update_layout(title_text=f'{selected_stock}', paper_bgcolor="white",  plot_bgcolor="white")

    st.plotly_chart(fig, use_container_width=True)
    st.write("""
            The dots are the expected maximal and minimal price within a given interval spanned by the last trading day.
            The color of the dots indicates the propability to buy or sell for this price.
            The orange line is the trend curve.
            The blue curve are the observed historical prices (grey stands for discarded observations).
            """)

    # fig = plt.plot(result.trend)
    # st.pyplot(fig=fig)

    st.markdown("""
            Based on the assumptions to be verified [here](https://www.thebigdatablog.com/does-my-stock-trading-strategy-work/). **This is no financial advise.**

            To learn more about the theoretical backgound of this calculations check out my blogpost at [thebigdatablog.com](https://www.thebigdatablog.com).
            """)
