# %%
import numpy as np
import pandas as pd
# %%
# This implies that the number of the occurance has an impact of the arrival time of the next occurence. For example if the first occurance takes place it is more likely that the second occurance happens short after. 


# %%
M=500  # max anz. incremente
N=2 # anz prozesse

lambda_i = np.random.rand(M)
#lambda_i = np.ones(M)*2

X = pd.DataFrame( [np.random.exponential(scale=1/lambda_i, size=M) for j in range(0,N)] )
T = X.cumsum(axis = 1)

# %%
# Computing sum over Index axis
def N(t, T):
    return (T<t).sum(axis=1)

# %%
# 1. Variant use a Poisson Process

t= T.max().min()
hat_lambda = np.mean(N(t,T))   #Even better use the integral!
print(hat_lambda/t)
print( np.log( np.mean( np.exp(lambda_i) ) ))
# %%
# 2nd Variant use the increments
# Estimator of exponential is 1/x
1/(X).mean(axis=0)

# %%
# 3rd Shift the Process
# t= T.max().max() # <-- alle 500 in m
t = 500
T_t = T.transpose()<t
S= (X.transpose()*T_t).sum(axis = 1) # Total Exposure, index is the covariate

# cap all in S where T<500
T.transpose()


# Now we need to derive the number of arrivals of For each S
# We must to fix s somewhere
#Für gegeben t wie viele incremente sind <t wie muss ich t wählen???
m =(T.transpose()<t).sum(axis=1) 

# Estimator
hat_lambda = m/S
print(hat_lambda)

##Für die korrekte Simulation muss ich an irgend einem T abschneiden

# %%
print( lambda_i[100:200] )
print(hat_lambda[100:200])
print(m[100:200])

# https://stats.stackexchange.com/questions/497086/how-to-find-a-good-estimator-for-lambda-in-exponential-distibution

# %%
import matplotlib.pyplot as plt
plt.plot(m)

# How to handle the marked process