import streamlit as st
import utils
import matplotlib as plt
import yfinance as yf

st.write("""
# Stockmarket Oracle
At what price should i buy or sell my stock?
""")

choices = ["^GDAXI", "^DJI", "GC=F", "BTC-EUR", "META" ,"AMZN","DTE.DE"]

selected_stock = st.selectbox("stock", choices)

st.set_option('deprecation.showPyplotGlobalUse', False)

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
    
    trend = [df.index, price[0]*np.exp(range(0,price.size)*(mu_est -0.5*sigma_est**2))]
    buy, sell, prop_buy, prop_sell = utils.optimal_limits_exact(mu_est, sigma_est, price[-1], days)   #10 days in advance
    return (trend, buy, sell, prop_buy, prop_sell)

st.write(f"""
The best prices for {selected_stock}
""")

result = get_prices(selected_stock, 5)
fig = plt.plot(result.trend)
st.pyplot(fig=fig)