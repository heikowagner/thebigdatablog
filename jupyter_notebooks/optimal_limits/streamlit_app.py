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


def get_prices(symbol, days, start=None, end=None):
    st.write("loading...")
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

    st.write("data loaded...")
    # Determine minimal date  
    price = df['Close']
    price = price.values
    
    mu_est, sigma_est = utils.compute_parameter(price ,price.size) # The last var is how many days we are looking at
    #time = np.concatenate( ([x.date() for x in df.index] , [df.index[-1].date() + dt.timedelta(day) for day in days]), axis=0)
    time = [x.date() for x in df.index] + [df.index[-1].date() + datetime.timedelta(day) for day in days]

    days_ahead = np.array( list( range(0,price.size) )  + [day + price.size for day in days] )  #days ahead should be more dense

    print(days_ahead)
    trend = price[0]*np.exp( days_ahead *(mu_est -0.5*sigma_est**2))
    
    # construct an array of 0 for price lengt

    buy = [np.nan]*price.size
    sell = [np.nan]*price.size

    for day in days:  #atm we only get the last
        buy_d, sell_d, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], day)
        buy.append(buy_d)
        sell.append(sell_d)

    #buy, sell, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], days)   #10 days in advance
    return (trend, buy, sell, prop_buy, prop_sell, time, 
            np.array(list(price) + [np.nan]*len(days)) #Here i need the full prices
            )


st.write("""
# Stockmarket Oracle
At what price should i buy or sell my stock?
""")

choices = ["^GDAXI", "^DJI", "GC=F", "BTC-EUR", "META" ,"AMZN","DTE.DE"]

selected_stock = st.selectbox("Which stock do you want to analyze", choices)

st.set_option('deprecation.showPyplotGlobalUse', False)

# st.write("What is your timeframe in days where you want to buy or sell your stock?")
days_in_advance = st.number_input("What is your timeframe where you want to buy or sell your stock?", step = 1, value=5 )
#st.write("How many historical data do you want to use to fit the model?")

today = datetime.datetime.now()

d = st.date_input(
    "How many historical data do you want to use to fit the model?",
    (datetime.date(2000, 1, 1), today),
    datetime.date(2000, 1, 1),
    today,
    format="MM.DD.YYYY",
)

start_date = d[0]
end_date = d[1]


# result = get_prices(selected_stock, days_in_advance, start_date)

st.write("Based on the assumtions to be verified here. This is no financial advise.")

trend, buy, sell, prop_buy, prop_sell, time, price = get_prices(selected_stock, [1,2,3,4,5,10,20,30,800, 1500, 2000, 2500, 3000], start_date, end_date) # stock 5 days ahead

st.write(f"""
The best limit to sell the  {selected_stock} within the next {days_in_advance} is {sell} the order will be fullfilled with a probability of {prop_sell}.

The best limit to buy the  {selected_stock} within the next {days_in_advance} is {buy} the order will be fullfilled with a probability of {prop_buy}.
""")

stock =  yf.Ticker(selected_stock)
df = stock.history(period="max")


fig = go.Figure()
fig0 = px.line(df, x=df.index, y="Close")

fig1 = px.line({ "date": time, "stockprice": price}, x="date", y="stockprice")
fig2 = px.line({ "date": time, "trend": trend}, x="date", y="trend")

fig3 = px.line({ "date": time, "buy": buy}, x="date", y="buy")
fig4 = px.line({ "date": time, "sell": sell}, x="date", y="sell")
fig = go.Figure(data = fig0.data + fig1.data + fig2.data + fig3.data + fig4.data)
fig.data[0].line.color = 'lightgrey'
fig.data[1].line.color = 'blue'
fig.data[2].line.color = 'orange'
fig.data[3].line.color = 'red'
fig.data[4].line.color = 'red'

st.plotly_chart(fig, use_container_width=True)

# fig = plt.plot(result.trend)
# st.pyplot(fig=fig)

st.write("To learn more about the theoretical backgound of this calculations check out my blogpost at thebigdatablog.com.")