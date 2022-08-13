
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf
from scipy.integrate import quad
from forex_python.converter import CurrencyRates 
import numpy as np


class GeometricBrownian():
    """
    A constructor for a geometric Brownian motion
    """
    def __init__(self,x0=0):
        self.x0 = float(x0)

    def gen_random_walk(self,n_step=100):
        """
        Generate motion by random walk

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        # Warning about the small number of steps
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step)*self.x0

        for i in range(1,n_step):
            # Sampling from the Normal distribution with probability 1/2
            yi = np.random.choice([1,-1])
            # Weiner process
            w[i] = w[i-1]+(yi/np.sqrt(n_step))

        return w

    def gen_normal(self,n_step=100, dt=.01):
        """
        Generate motion by drawing from the Normal distribution

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step)*self.x0

        for i in range(1,n_step):
            # Sampling from the Normal distribution
            yi = np.random.normal(0, np.sqrt(dt))
            # Weiner process
            w[i] = w[i-1]+yi

        return w

    def stock_price(
                    self,
                    s0=100,
                    mu=0.2,
                    sigma=0.68,
                    deltaT=52,
                    dt=0.1
                    ):
        """
        Models a stock price S(t) using the Weiner process W(t) as
        `S(t) = S(0).exp{(mu-(sigma^2/2).t)+sigma.W(t)}`

        Arguments:
            s0: Iniital stock price, default 100
            mu: 'Drift' of the stock (upwards or downwards), default 1
            sigma: 'Volatility' of the stock, default 1
            deltaT: The time period for which the future prices are computed, default 52 (as in 52 weeks)
            dt (optional): The granularity of the time-period, default 0.1

        Returns:
            s: A NumPy array with the simulated stock prices over the time-period deltaT
        """
        n_step = int(deltaT/dt)
        time_vector = np.linspace(0,deltaT,num=n_step)
        #print(time_vector)
        # Stock variation
        stock_var = (mu-(sigma**2/2))*time_vector
        #print(stock_var)
        # print((mu-(sigma**2/2)))
        # Forcefully set the initial value to zero for the stock price simulation
        self.x0=0
        # Weiner process (calls the `gen_normal` method)
        weiner_process = sigma*self.gen_normal(n_step,dt)
        # Add two time series, take exponent, and multiply by the initial stock price
        s = s0*(np.exp(stock_var+weiner_process))

        return s