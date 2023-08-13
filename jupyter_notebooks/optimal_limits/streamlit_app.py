import streamlit as st
import utils
import yfinance as yf
import numpy as np

import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt


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
            current_date = (datetime.today()  + timedelta(1))
        if not start:
            start_date = stock.history(period="max").index.min()
        df = stock.history(start=start_date, end=current_date)

    st.write("data loaded...")
    # Determine minimal date  
    price = df['Close']
    price = price.values
    
    mu_est, sigma_est = utils.compute_parameter(price ,price.size) # The last var is how many days we are looking at
    #time = np.concatenate( ([x.date() for x in df.index] , [df.index[-1].date() + dt.timedelta(day) for day in days]), axis=0)
    time = [x.date() for x in df.index] + [df.index[-1].date() + dt.timedelta(day) for day in days]

    days_ahead = np.array( list( range(0,price.size) )  + [day + price.size for day in days] )

    print(days_ahead)
    trend = price[0]*np.exp( days_ahead *(mu_est -0.5*sigma_est**2))
    
    for day in days:
        buy, sell, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], day)

    #buy, sell, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], days)   #10 days in advance
    return (trend, buy, sell, prop_buy, prop_sell, time, np.array(list(price) + [np.nan]*len(days)) )


st.write("""
# Stockmarket Oracle
At what price should i buy or sell my stock?
""")

choices = ["^GDAXI", "^DJI", "GC=F", "BTC-EUR", "META" ,"AMZN","DTE.DE"]

selected_stock = st.selectbox("stock", choices)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.write(f"""
The best prices for {selected_stock}
""")

st.write("What is your timeframe where you want to buy or sell your stock?")
days_in_advance = st.textbox("")
st.write("How many historical data do you want to use to fit the model?")
start_date = st.datepicker("")


result = get_prices(selected_stock, days_in_advance, start_date)

st.write(f"""
The best limit to sell the  {selected_stock} within the next {days_in_advance} is {result.sell} the order will be fullfilled with a probability of {result.sell_prop}.
The best limit to buy the  {selected_stock} within the next {days_in_advance} is {result.buy} the order will be fullfilled with a probability of {result.sell_buy}.
""")

st.write("Based on the assumtions to be verified here. This is no financial advise.")

trend, buy, sell, prop_buy, prop_sell, time, price = get_prices(selected_stock, [1,2,3,4,5,10,20,30]) # stock 5 days ahead

st.write(f"""
Buy price: {buy} with propability {prop_buy}
Sell price: {sell} with propability {prop_sell}
""")

fig = go.Figure()
fig1 = px.line({ "date": time, "stockprice": price}, x="date", y="stockprice")
fig2 = px.line({ "date": time, "stockprice": trend}, x="date", y="stockprice")
fig = go.Figure(data = fig1.data + fig2.data)
st.plotly_chart(fig, use_container_width=True)

# fig = plt.plot(result.trend)
# st.pyplot(fig=fig)

st.write("To learn more about the theoretical foundation of this calculations check out my blogpost at thebigdatablog.com.")

