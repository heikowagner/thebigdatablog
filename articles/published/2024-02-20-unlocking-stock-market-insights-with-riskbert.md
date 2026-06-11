---
categories:
- All Articles
- Coding
- Finance
- Large Language Models
- Python
date: '2024-02-20'
slug: unlocking-stock-market-insights-with-riskbert
status: publish
tags: []
title: Unlocking Stock Market Insights with RiskBERT
wp_id: 4598
wp_modified: '2024-08-04T08:45:08'
---

Predicting stock prices is akin to the attempts of alchemists in the Middle Ages to transmute lead into gold. Just as alchemists sought to unlock the secrets of transformation, statisticians and investors alike strive to decipher the patterns and signals hidden within market data. Traditional models often assume that stock prices follow a Brownian motion, making them appear entirely random and unpredictable. However, the reality is far more nuanced. While stock prices may exhibit elements of randomness, they are also influenced by a myriad of external factors, including news articles detailing significant events such as annual general meetings or company scandals.

In the fast-paced world of stock trading, staying ahead of the curve often means processing vast amounts of information in real-time. Investors are constantly seeking tools that can help to make more informed decisions amidst the chaos of market fluctuations and news updates. In recent years, advancements in natural language processing (NLP) and machine learning have paved the way for innovative approaches to analyzing market sentiment and risk. \
\
In this blog post, we’ll explore how RiskBERT, can be leveraged to gain insights into stock market dynamics. In particular we try to figure out if, given the open price, a news release during the days is related to the closing price of that day.

### Introducing RiskBERT

Built upon the foundation of BERT (Bidirectional Encoder Representations from Transformers), [RiskBERT](https://www.thebigdatablog.com/generalized-semantic-regression-using-contextual-embeddings/) harnesses the power of deep learning to extract signals from textual data to quantify and assess the potential impact of news events on stock prices.

### Analyzing Apple Inc. (AAPL) Stock

To demonstrate the capabilities of RiskBERT, let’s delve into a case study focusing on Apple Inc. (AAPL) stock. We’ll walk through a Python script that fetches news articles related to AAPL from a financial API, retrieves historical stock price data using Yahoo Finance, and applies RiskBERT to analyze the relationship between news sentiment and stock price movement.

#### Fetching News Data

We start by retrieving news articles related to AAPL using the EOD Historical Data API. Since the API limits the number of records per call, we implement a loop to fetch data iteratively until reaching the desired timeframe.

```
import requests
import pandas as pd
import yahooquery as yq
import matplotlib.pyplot as plt
import numpy as np
from RiskBERT import normalLoss
from RiskBERT import RiskBertModel
from RiskBERT import trainer, evaluate_model
from RiskBERT import DataConstructor
import torch
from transformers import AutoTokenizer

i=0
start_from= datetime.datetime.today().strftime(&quot;%Y-%m-%d&quot;)
while True:
    try:
        url = f&#039;https://eodhd.com/api/news?s=AAPL.US&amp;offset=0&amp;limit=1000&amp;to={start_from}&amp;api_token=demo&amp;fmt=json&#039;
        data = requests.get(url).json()
        if i==0:
            appl_news = pd.DataFrame( data )
        else:
            appl_news=appl_news._append(pd.DataFrame( data ), ignore_index=True)
        start_from=str( min( pd.to_datetime(appl_news[&quot;date&quot;]).dt.date ) )

        if min( pd.to_datetime(appl_news[&#039;date&#039;]).dt.date )&lt;=datetime.date.fromisoformat(&#039;2016-02-19&#039;):
            break
        i=i+1
    except Exception as e: 
        print(e)
        break
```

#### Retrieving Stock Price Data

Next, we obtain historical stock price data for AAPL from Yahoo Finance. This data will serve as the basis for our analysis, allowing us to correlate news events with changes in stock prices.

```
end = max(appl_news[&quot;date&quot;]) 
start = min(appl_news[&quot;date&quot;])

tq = yq.Ticker(&quot;AAPL&quot;)
stock_data = tq.history(start=start, end=end)
```

#### Preparing the Data

Before applying RiskBERT, we preprocess the data and join the news articles with the corresponding stock price data. We also perform feature engineering to enrich the dataset with additional information relevant to our analysis.

```
appl_news[&quot;daydate&quot;]=pd.to_datetime(appl_news[&quot;date&quot;]).dt.date
stock_with_news = stock_data.merge(appl_news,left_on=&quot;date&quot;,right_on=&quot;daydate&quot;, how=&quot;left&quot;)

stock_with_news = stock_with_news.dropna()
stock_with_news[&quot;label&quot;] = np.log(stock_with_news[&quot;close&quot;])-np.log(stock_with_news[&quot;open&quot;])
stock_with_news[&quot;num_symbols&quot;] = stock_with_news[&quot;symbols&quot;].apply(lambda x: len(x))
```

#### Analyzing Stock Price Distribution

To determine the correct distribution for RiskBERT, we plot a basic histogram of the stock price changes. The distribution appears to be fairly “normal,” validating our choice of using the normalLoss as the loss function for RiskBERT. This is what to be expected theoretically which should not be surprising for the frequent reader of this blog (see <https://www.thebigdatablog.com/does-my-stock-trading-strategy-work/>)

```
plt.hist(np.log(stock_data[&quot;close&quot;])-np.log(stock_data[&quot;open&quot;]), bins=50, color=&quot;skyblue&quot;, edgecolor=&quot;black&quot;)
```

[![image](https://www.thebigdatablog.com/wp-content/uploads/2024/02/image.png)](https://www.thebigdatablog.com/wp-content/uploads/2024/02/image.png)

#### Applying RiskBERT

With the data prepared, we proceed to apply RiskBERT to analyze the relationship between news sentiment and stock price movement. We utilize a pre-trained BERT model and fine-tune it for our specific task, incorporating additional features such as the number of symbols mentioned in each news article.

```
# Set device to gpu if available
device = torch.device(&quot;cuda:0&quot; if torch.cuda.is_available() else &quot;cpu&quot;)

pre_model= &quot;distilbert-base-uncased&quot;
model = RiskBertModel(model=pre_model, input_dim=1, dropout=0.4, freeze_bert=True, mode=&quot;CLS&quot;, loss_fn=normalLoss).to(device)
tokenizer = AutoTokenizer.from_pretrained(pre_model)

covariates = np.array(
        [ 
         stock_with_news[&quot;num_symbols&quot;] 
        ]
    ).T

my_data = DataConstructor( 
    sentences=[ [x] for x in stock_with_news[&quot;title&quot;] ], 
    covariates=covariates,
    labels= [ [x] for x in stock_with_news[&quot;label&quot;] ],
    tokenizer= tokenizer,
    device=device)

fitted_model, Total_Loss, Validation_Loss, Test_Loss = trainer(model =model, 
        model_dataset=my_data, 
        epochs=100,
        batch_size=1000,
        evaluate_fkt=evaluate_model,
        tokenizer=tokenizer, 
        optimizer=torch.optim.SGD(model.parameters(), lr=0.001),
        device = device
        )

my_prediction=fitted_model(**my_data.prepare_for_model())
```

### Unveiling Insights

In conclusion, our exploration into the world of stock market analysis with RiskBERT has yielded promising insights and results. Observing how the validation loss evolved over epochs provides valuable insights into the training process. Despite fluctuations, we can discern a clear trend of decreasing validation loss over time, indicating that RiskBERT continuously improves its predictive capabilities as it learns from the data. Thus RiskBERT is able to capture the impact of certain news on the closing price. However, before false hopes arise, the estimated model cannot be used for forecasts. The observed learning curve is mainly the estimate of the intercept. If you want to experiment with RiskBERT by yourself, the code is available at <https://github.com/heikowagner/generalized-semantic-regression/blob/main/RiskBERT/simulation/stock_market_example.py>.

[![image 1](https://www.thebigdatablog.com/wp-content/uploads/2024/02/image-1.png)](https://www.thebigdatablog.com/wp-content/uploads/2024/02/image-1.png)

Validation Loss over 100 epochs