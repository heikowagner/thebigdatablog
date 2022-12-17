import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf
from scipy.integrate import quad
import numpy as np
import logging
from datetime import timedelta, datetime

logger = logging


def compute_parameter(price, n_days = 1):

    log_price = np.log(price)
    delta = log_price[1:] - log_price[:-1]
    n_samples = delta.size
    n_days = n_days 
    total_change = log_price[-1] - log_price[0]

    vol2 = (-total_change ** 2 / n_samples + np.sum(delta ** 2)) / n_days
    vol = np.sqrt(vol2)

    drift = total_change / n_days + 0.5 * vol2
    return (drift, vol)


def min_props(i, X0, mu_hat, sigma, llambda, T):

    return 1- min(
            (i / X0) ** (2 * llambda) * norm.cdf((np.log(i / X0) + mu_hat * T) / (sigma * np.sqrt(T)))
            + norm.cdf( (np.log(i / X0) - mu_hat * T) / (sigma * np.sqrt(T)))
        ,1)

def max_props(i, X0, mu_hat, sigma, llambda, T):

    return min(
            (i / X0) ** (2 * llambda) * norm.cdf((-np.log(i / X0) - mu_hat * T) / (sigma * np.sqrt(T)))
            + norm.cdf((-np.log(i / X0) + mu_hat * T) / (sigma * np.sqrt(T)))
            , 1)

def optimal_limits_exact(mu, sigma, current_price, n_days):
    T=n_days
    X0=current_price
    mu_hat =  (mu - sigma**2/2)
    llambda = mu_hat/sigma**2

    if X0 > 1000:
        limit=X0**1.5
        logger.warning(f"upper bound for the integral was set to {limit}")
    else:
        limit = np.inf

    buy =  quad(min_props, 0, limit,   args=(X0, mu_hat, sigma, llambda, T))[0]
    sell =  quad(max_props, 0, limit,  args=(X0, mu_hat, sigma, llambda, T))[0]
    prop_buy = min_props(buy, X0, mu_hat, sigma, llambda, T)
    prop_sell = max_props(sell, X0, mu_hat, sigma, llambda, T)
    return(buy,sell, prop_buy, prop_sell)


def get_prices(symbol, days, start=None, end=None):
    print(symbol)
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

    print(F"To estimate the coefficents we use the time between {start_date.strftime('%Y-%m-%d')} and {current_date.strftime('%Y-%m-%d')}")

    # Determine minimal date  
    price = df['Close']
    price = price.values
    plt.plot(df['Close'])

    mu_est, sigma_est = compute_parameter(price ,  price.size) # The last var is how many days we are looking at
    
    plt.plot(df.index,price[0]*np.exp(range(0,price.size)*(mu_est -0.5*sigma_est**2)))
    print(f"Estimated µ: {mu_est}")
    print(f"Estimated σ: {sigma_est}")
    print('Last observed price: {0:06.3f}'.format(price[-1]))    
    buy, sell, prop_buy, prop_sell = optimal_limits_exact(mu_est, sigma_est, price[-1], days)   #10 days in advance
    print(f"Optimal Buy Limit within the next {days} days : {round(buy,2)}")
    print(f"Optimal Sell Limit within the next {days} days : {round(sell,2)}")
    print(f'Propability to buy for that price: {round(prop_buy*100,2)} %')
    print(f'Propability to sell for that price: {round(prop_sell*100,2)} %')
    print(f"""

Disclaimer: Based on the assumption that the stock price follows a geometric brownian motion. 
To learn more visit https://www.thebigdatablog.com.
Find more symbols: https://de.finance.yahoo.com/lookup.""")
    plt.legend(['actual stock price', 'longtime trend'])
    plt.show()
    return plt
