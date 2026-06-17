---
categories:
- All Articles
- Finance
- Introduction
date: '2022-08-13'
slug: does-my-stock-trading-strategy-work
status: publish
tags: []
title: Expected maxima of a Brownian Motion- Does my stock trading strategy work?
wp_id: 3596
wp_modified: '2023-10-01T10:10:56'
---

I recently realized that I have a certain habit when it comes to stock trading even though I used to tell myself that “every trading strategy is useless because the stock market is just random”. If I buy a share I usually set the limit just a little below the actual price while if i sell I place the limit above. The question we want to answer today is if such a trading strategy is reasonable and if there is an optimal limit to maximize the expected profit. \
\
More formally, let ![S(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-38e49d63c9cb435c0ce173ba053ca5dc_l3.png "Rendered by QuickLaTeX.com") be the stock price at time ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com") and let ![l](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-502276c66966e5a861539c7de60c26c0_l3.png "Rendered by QuickLaTeX.com") be a limit set for a certain order, then the order will be fulfilled if ![S(t) = l](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2967945f8e05e3a91f90b728e96c63e7_l3.png "Rendered by QuickLaTeX.com") for some ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"). In the following we will investigate how to set a best price if an order should be processed within a given time ![\tau](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-13197f4653c1fd428a291609eb1e3b87_l3.png "Rendered by QuickLaTeX.com")

(1)    ![\begin{eqnarray*}l^* = E (max_{0\leq s \leq \tau} S(s) ).\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ceae7d22fb721c2d4494e7760376c644_l3.png "Rendered by QuickLaTeX.com")

\

To answer the questions we have deduct a model based on some assumptions. A popular start is to think about a stock price as a brownian motion to capture the random behavior. Remember, we already covered the brownian motion in [a previous post](https://www.thebigdatablog.com/functional-principal-component-analysis-with-spark/). However the properties of a Brownian motion do not match the experience of a stock price entirely. Usually a stock price has to be non negative, we can also assume that it follows some kind of trend and the increment size will change based on the price. More formally ,we assume for the exchange rate ![S(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-38e49d63c9cb435c0ce173ba053ca5dc_l3.png "Rendered by QuickLaTeX.com") that

- ![S(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-38e49d63c9cb435c0ce173ba053ca5dc_l3.png "Rendered by QuickLaTeX.com") is the [logarithm](https://en.wikipedia.org/wiki/Logarithm) of a randomly varying Brownian Motion ![W_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1d768bcb71676da7d7190c91bf53f3f1_l3.png "Rendered by QuickLaTeX.com")
- a percentage drift ![\mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-461fe1a58a75801541487ddf10d32abd_l3.png "Rendered by QuickLaTeX.com")
- a percentage volatility ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com")

This then gives

(2)    ![\begin{eqnarray*}S(t) = S(0) \exp \left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t \right) \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e15af09167ee10cbfe9ed871f76866c2_l3.png "Rendered by QuickLaTeX.com")

where ![W_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1d768bcb71676da7d7190c91bf53f3f1_l3.png "Rendered by QuickLaTeX.com") is a standard [brownian motion](https://www.thebigdatablog.com/functional-principal-component-analysis-with-spark/) and ![S(0)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-072851f0c79b46270655edea924e6ebc_l3.png "Rendered by QuickLaTeX.com") the initial value. By definition ([3](#id4040228949)) is a geometric brownian motion since it solves the stochastic differential equation ![dS_t = \mu S_t dt + \sigma S_tdW_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd2ac78eed4b68aec9a105550c71a682_l3.png "Rendered by QuickLaTeX.com"). Assuming a geometric brownian motion is also the foundation of the famous black-scholes-model. Thus ![S_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3e279cd3791c554f6a9337bcf21d1b1b_l3.png "Rendered by QuickLaTeX.com") is log normally distributed with\

(3)    ![\begin{eqnarray*}E(S(t)) = S(0) \exp(\mu t), \; Var(S(t))= S_0^2 exp (2 \mu t) (exp(\sigma^2 t)-1).\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-39bb65fd6fc5297381da7df1d60ed465_l3.png "Rendered by QuickLaTeX.com")

\

To answer our initial question we use a commonly known result based on the [Girsanov theorem](https://en.wikipedia.org/wiki/Girsanov_theorem):\
\
**Proposition 1** ([proof as Proposition 3.2)](https://famille-chazal.pagesperso-orange.fr/articles/maxbrownien.pdf)\
Let ![W_t^{\mu} = (W_t + \mu t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd3b64a72bb18484957d21beb4d53d55_l3.png "Rendered by QuickLaTeX.com") be a brownian motion with drift ![\mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-461fe1a58a75801541487ddf10d32abd_l3.png "Rendered by QuickLaTeX.com"), let ![t \in \mathbb{R}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c7cf513e0c3476d50e9f52f3b7136a38_l3.png "Rendered by QuickLaTeX.com") ![M_t^{\mu} := (sup_{s \in [0,t]} W_s^{\mu})>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-17ed2fb13493982e604645e0bd8ca6e2_l3.png "Rendered by QuickLaTeX.com"), ![x \in \mathbb{R}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5dd56a8e9c5e12a00cda4c65de181936_l3.png "Rendered by QuickLaTeX.com") then\

(4)    ![\begin{eqnarray*}\mathbb{P}(M_t^{\mu} \geq x) = e^{2 \mu x}  \Phi\left( \frac{-x-\mu t}{\sqrt{t}} \right) +  \Phi\left( \frac{-x+\mu t}{\sqrt{t}} \right)\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e634ced907cf78b139c902f199fc62c9_l3.png "Rendered by QuickLaTeX.com")

\
here ![\Phi()](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-79a9a9d569832d7a29e788ab4a24d8c3_l3.png "Rendered by QuickLaTeX.com") is [CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function) of the standard normal distribution.\
\
When we apply ([4](#id3329867258)) to the geometric brownian motion with ![S^{sup}_\tau :=  (sup_{t \in [0,\tau]} S(t))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9a3092543173422c713adcad15d96997_l3.png "Rendered by QuickLaTeX.com") we get \

(5)    ![\begin{eqnarray*}\mathbb{P}(S^{sup}_\tau \leq l) = \mathbb{P}\left(M^{\lambda}_\tau \leq ln\left(\frac{l}{S_0}\right)\right) \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-03f4b5ae7279814a11b4cd32da24ffbb_l3.png "Rendered by QuickLaTeX.com")

\
where ![\lambda= \frac{\mu - 0.5\sigma^2}{\sigma^2}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-50e2dee9a311396b58642e33620ba56f_l3.png "Rendered by QuickLaTeX.com"). ![M^{\lambda}_\tau](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8917cae6950e26ddf5201fffe1ae012c_l3.png "Rendered by QuickLaTeX.com") is thus a brownian motion with drift ![\lambda](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b5c45836864531b8e37025dabadd24a_l3.png "Rendered by QuickLaTeX.com"), in addition using a scaling with ![t=\sigma^2 \tau](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d525e469cbf5eb4eaf45f4ae6357b130_l3.png "Rendered by QuickLaTeX.com") of the underlying brownian motion, this lead to\

(6)    ![\begin{eqnarray*}\mathbb{P}(S^{sup}_\tau \geq l) = \frac{l}{S_0}^{2 \lambda} \Phi \left(\frac{ln(\frac{l}{S_0}) -\sigma^2 \lambda \tau}{\sigma \sqrt{\tau}}}\right) + \Phi \left(\frac{ln(\frac{l}{S_0}) +\sigma^2 \lambda \tau}{\sigma \sqrt{\tau}}}\right)\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-59659c7854b224e1f3405cf1c8f14d48_l3.png "Rendered by QuickLaTeX.com")

\
Accordingly, by symmetrie we get for ![S^{inf}_\tau :=  (inf_{t \in [0,\tau]} S(t))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1bf0332e2b8f7d15fcd9fa3e166d8819_l3.png "Rendered by QuickLaTeX.com")\

(7)    ![\begin{eqnarray*}\mathbb{P}(S^{inf}_\tau \leq l) = \frac{l}{S_0}^{2 \lambda} \Phi \left(\frac{ln(\frac{l}{S_0}) +\sigma^2 \lambda \tau}{\sigma \sqrt{\tau}}}\right) + \Phi \left(\frac{ln(\frac{l}{S_0}) -\sigma^2 \lambda \tau}{\sigma \sqrt{\tau}}}\right)\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b1152959de59cfafd8833ba1a58ed297_l3.png "Rendered by QuickLaTeX.com")

\
The equations above thus tell us how likely it is to sell/buy a stock within a time interval of length ![\tau](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-13197f4653c1fd428a291609eb1e3b87_l3.png "Rendered by QuickLaTeX.com"). To answer our initial question ([1](#id2624834689)) we derive the expectation, to get the best buy and sell limits, with\

(8)    ![\begin{eqnarray*}l_{buy, \tau}^* = \int_0^{\infty} 1- \mathbb{P}(S^{inf}_\tau \leq l) dl, \; l_{sell, \tau}^* = \int_{0}^{\infty} \mathbb{P}(S^{sup}_\tau \geq l) dl.\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8f38c2d1c28c1728737dcd9e6f3735fb_l3.png "Rendered by QuickLaTeX.com")

## Estimating \sigma and \mu

Since ![\mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-461fe1a58a75801541487ddf10d32abd_l3.png "Rendered by QuickLaTeX.com") and ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com") are unknown we have to estimate them from observations. Let ![\Delta = ln(S(t+\Delta t))-ln(S(t))=  \left( \mu -  \frac{\sigma^2}{2} \right)\Delta t + \sigma W_{\Delta t}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-334999e455a68dc9cdc8dd7c4515a5fd_l3.png "Rendered by QuickLaTeX.com"), which obviously follows a normal distribution with mean ![\mu_\Delta = (\mu - 0.5\sigma^2)\Delta t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d81df0de51db5a8463c976eaedc3bd91_l3.png "Rendered by QuickLaTeX.com") and variance ![\sigma_\Delta^2 = \sigma^2 \Delta t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a257908a9ba1d47f4886bd1d465eb915_l3.png "Rendered by QuickLaTeX.com"). Thus ![\sigma^2 = \frac{\sigma_\Delta^2}{\Delta t}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-175be0fe78bc9c9dbcc0b64c6db2d2c1_l3.png "Rendered by QuickLaTeX.com") and ![\mu= \frac{\mu_\Delta + 0.5 \sigma_\Delta^2}{\Delta t}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-266d7ce4a804ec199a33aebedfdde8ae_l3.png "Rendered by QuickLaTeX.com").\
Stock prices are usually not observed as a continuous process, but instead oftentimes on a daily or minutely basis. In fact stock prices are never continuous because price fluctuations are measured using ticks. This is one reason, among others, why a brownian motion can only be considered as an approximation of the true behaviour of a stock price. If we assume ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") discrete observations ![\Delta_1, \dots, \Delta_N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f95a9435699554355bdc58d69646005c_l3.png "Rendered by QuickLaTeX.com") with starting point ![t_0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4f748b339328872e9bd17f31810a92d_l3.png "Rendered by QuickLaTeX.com") and endpoint ![t_N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-663dba7e05ed1532fd6d2c8321b66258_l3.png "Rendered by QuickLaTeX.com") with an equidistant time gap of ![\Delta t  = \Delta t_i = t_{i}-t_{i-1} = \frac{t_N-t_0}{N}, i=1,\dots,N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2da7cbb589e994c23d2b6d39d8aff90f_l3.png "Rendered by QuickLaTeX.com") we can derive unbiased estimators \

(9)    ![\begin{eqnarray*}\hat{\mu}= \frac{\hat{\mu}_\Delta + 0.5 \hat{\sigma}_\Delta^2}{\Delta t}, \;\hat{\mu}_\Delta = \sum_{i=1}^N \frac{\Delta_i}{N} \rightarrow_p \left( \mu - \frac{\sigma^2}{2} \right)\Delta t\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-278b8df37f7e06d1901dea5c9bc1f31e_l3.png "Rendered by QuickLaTeX.com")

\
while\

(10)    ![\begin{eqnarray*}\hat{\sigma}^2 = \frac{\hat{\sigma}_\Delta^2}{\Delta t}, \; \hat{\sigma}^2_\Delta = \sum_{i=1}^N \frac{(\Delta_i-\hat{\mu}_\Delta)^2}{N-1} \rightarrow_p \sigma^2 \Delta t\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7acfffa7f73ccfeba50c793682ba303a_l3.png "Rendered by QuickLaTeX.com")

\
further we can verify that the estimators ![\hat{\mu}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2631e7f6512c982b1c6dae0f4797f19c_l3.png "Rendered by QuickLaTeX.com"), ![\hat{\sigma}^2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a9d6e6825a5fdea164a9b38f0ee91d43_l3.png "Rendered by QuickLaTeX.com") are consistent with\

(11)    ![\begin{eqnarray*}Var(\hat{\sigma}^2)= \frac{Var(\hat{\sigma}_\Delta^2)}{\Delta t^2}=\frac{E(\hat{\sigma}_\Delta^4)-  E(\hat{\sigma}_\Delta^2)^2}{\Delta t^2}= \frac{2 \sigma^4}{N}\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f15c5fbd23a75c4f76123dc0262a7bb0_l3.png "Rendered by QuickLaTeX.com")

\

(12)    ![\begin{eqnarray*}Var(\hat{\mu})= \frac{4 Var(\hat{\mu}_\Delta)+ Var(\hat{\sigma}^2_\Delta)}{4\Delta t^2} = \frac{2\sigma^2 + \sigma^4 \Delta t}{2N\Delta t} \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-727e360cbb0d353206696ed059d7b4f1_l3.png "Rendered by QuickLaTeX.com")

## Real Data Example

We use the above described method write a small python script that will estimate ![\mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-461fe1a58a75801541487ddf10d32abd_l3.png "Rendered by QuickLaTeX.com") and ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com") for a particular stock and then derive the optimal buy or sell limit dependent on ![\tau](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-13197f4653c1fd428a291609eb1e3b87_l3.png "Rendered by QuickLaTeX.com"). \
\
**Try it yourself with my online notebook:**

- [Colab (google account required)](https://colab.research.google.com/drive/11rmyL6wziSbjXzQXldzBklzCTEbfQrU7?usp=sharing)
- [Binder (slower bootup, no google account necessary)](https://mybinder.org/v2/gh/heikowagner/thebigdatablog/master?labpath=jupyter_notebooks%2Foptimal_limits%2Foptimal_limits.ipynb)

[![](https://www.thebigdatablog.com/wp-content/uploads/2022/08/2022-08-13-1-1024x599.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2022/08/2022-08-13-1.jpg)

**Figure 1:** A picture of the [python program](https://mybinder.org/v2/gh/heikowagner/thebigdatablog/master?labpath=jupyter_notebooks%2Foptimal_limits%2Foptimal_limits.ipynb). Beside the estimates for ![\mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-461fe1a58a75801541487ddf10d32abd_l3.png "Rendered by QuickLaTeX.com") and ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com") as well as ![\hat{l }_{buy, \tau}^*, \hat{l }_{sell, \tau}^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2306c7e675a3c3d9f58ab11e0ee3642d_l3.png "Rendered by QuickLaTeX.com") also is ![\mathbb{P}(S^{inf}_\tau \leq \hat{l }_{buy, \tau}^*), \mathbb{P}(S^{inf}_\tau \leq \hat{l }_{sell, \tau}^*)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-475d92a491b700b7f3765b9716d5f586_l3.png "Rendered by QuickLaTeX.com") shown. The blue line shows the share price of the DAX between 1988 and today.The orange line is the trend ![S(0) exp(\hat{\mu} - 0.5 \hat{\sigma}^2)t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-77ce9ed1e6ffb70a0e38e0337c0af198_l3.png "Rendered by QuickLaTeX.com").