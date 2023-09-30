# %%
# Step 1: Import packages, functions, and classes
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np

# Step 2: Get data
n =1000000

X = 2.5 * np.random.randn(n) + 1.5   # Array of 100 values with mean = 1.5, stddev = 2.5
X2 = [np.random.binomial(1, 0.3) for i in range(0,n) ]   # Array of 100 values with mean = 1.5, stddev = 2.5
X3 = [np.random.binomial(1, 0.3) for i in range(0,n) ]   # Array of 100 values with mean = 1.5, stddev = 2.5
# %%
res = 0.5 * np.random.randn(n)       # Generate 100 residual terms
xb = 2 + 0.3 * X + 0.8 * np.array(X2) #+ res                  # Actual values of Y
# %%
p = 1/(1 + np.exp(-xb))

Y = [ np.random.binomial(1,p) for p in p]


# %%

# Create pandas dataframe to store our X and y values
df_x = pd.DataFrame(
    {'X1': X, 
     'X2': np.array(X3)
     }
)




# %%

model = LogisticRegression()
model.fit(df_x , Y)

# %%

# Step 4: Evaluate the model
p_pred = model.predict_proba(df_x)
y_pred = model.predict(df_x)
score_ = model.score(df_x, Y)
conf_m = confusion_matrix(Y, y_pred)
report = classification_report(Y, y_pred)

# %%
print(report)
print(model.coef_)
# %%
