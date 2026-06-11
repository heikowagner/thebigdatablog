---
categories:
- All Articles
- Introduction
date: '2023-09-07'
slug: notes-on-stochastic-processes-with-independent-non-stationary-increments
status: publish
tags: []
title: Notes on stochastic count processes with independent non stationary increments
wp_id: 4313
wp_modified: '2023-10-01T10:10:42'
---

## Problem Statement

Let ![\mathbb{P}(X_{ij}>t)=e^{-\lambda_i t}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b1d85338a2310e22c7f2c2537c90009e_l3.png "Rendered by QuickLaTeX.com") thus ![X_{ij} \sim Exponential(\lambda_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fbaa0e3092905a71404df693ab6b412_l3.png "Rendered by QuickLaTeX.com"), we construct a stochastic process as ![T_{jn} = \sum_{i=0}^n X_{ij}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d916e121089b9e493f98f724126c94bf_l3.png "Rendered by QuickLaTeX.com"), this kind of random variable are called hypoexponential random variables. We define a counting process such that ![N_j(t) = max\{n| T_{jn} < t\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-06d0cccd5d08d0ea4b75746ff2163919_l3.png "Rendered by QuickLaTeX.com"). This allows to model a certain relation between events, for example to have a shorter expected waiting time for a second event if the first event was observed.

**Statement 1:** ![N(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e255c9713203d41cd017c10b2a39b417_l3.png "Rendered by QuickLaTeX.com") is no Poisson process. \
To see this let ![0<T_1<t_1<T_2<T_3<t_2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-322a93012d6f5238097a7199b9564f9b_l3.png "Rendered by QuickLaTeX.com") and ![t_2-t_1<T_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7bcd5737833624182da408532a6a25a0_l3.png "Rendered by QuickLaTeX.com") then ![N(t_2)-N(t_1)=X_2 + X_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82916e116f2ab8617a77e86b1fe3c960_l3.png "Rendered by QuickLaTeX.com") while ![N(t_2 - t_1)=X_1 + X_2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a546ab0d2feb6719a6c86d64856b22cd_l3.png "Rendered by QuickLaTeX.com"). Since the density of ![X_i + X_{i+1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-06508dafc8b9d6e911865fdef86f1737_l3.png "Rendered by QuickLaTeX.com") is given by ![\frac{\lambda_i}{\lambda_i- \lambda_{i+1}} \lambda_{i+1} e^{-  \lambda_{i+1} t } + \frac{\lambda_{i+1}}{\lambda_{i+1} - \lambda_i} \lambda_i e^{-  \lambda_i t }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ace190cee469e8b9a271ff5df92a86bb_l3.png "Rendered by QuickLaTeX.com") with ![\lambda_1  \neq \lambda_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-462baf6ab12bfb8896634da41bf26ab4_l3.png "Rendered by QuickLaTeX.com") the process is non stationary and can thus not be a Poisson process.

**Statement 2:** The (hypoexponential) distribution of ![T_{jn}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3cd8cac90e7ba505164c5ae374c20e6f_l3.png "Rendered by QuickLaTeX.com") is given by ![f(t)= \sum_{i=1}^n C_{i,n} \lambda_i e ^{-\lambda_it}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-99a7f5e81eb9af1b8babd679e0070bfb_l3.png "Rendered by QuickLaTeX.com") for ![t>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ef70e5ae3f51890a98b73c9c01943afe_l3.png "Rendered by QuickLaTeX.com") and ![0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a5e437be25f29374d30f66cd46adf81c_l3.png "Rendered by QuickLaTeX.com") else where ![C_{i,n} = \prod_{i \neq j} \frac{\lambda_j}{\lambda_j - \lambda_i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1737ce17a821f3ef2eaae76c5c1f3de2_l3.png "Rendered by QuickLaTeX.com") and thus ![\mathbb{E}(T_{jn})= \int_{0}^\infty \sum_{i=1}^n t C_{i,n} \lambda_i e ^{-\lambda_it} dt = \sum_{i=1}^n  \frac{C_{i,n}}{\lambda_i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-088e91e8ea326dd0b2f79b49de087101_l3.png "Rendered by QuickLaTeX.com"). \

(1)    ![\begin{eqnarray*}\mathbb{E}(N_j(t))=\sum_m m \mathbb{P}(N_j(t)=m)= \sum_m m  \mathbb{P}\left(T_{jm}<t \leq T_{jm+1}\right) \\= \sum_m  m \left(1-\sum_{k=0}^{m} C_{k,m} e^{-\lambda_k t} \right) \left(\sum_{k=0}^{m+1} C_{k,m+1} e^{-\lambda_k t} \right)\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b3b2b5ea0119817e80508daef823d9ca_l3.png "Rendered by QuickLaTeX.com")

## Estimation

To estimate ![\lambda_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-130188abd4690d701177358e4ad96950_l3.png "Rendered by QuickLaTeX.com") we construct a different process. For fixed ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"), let ![N_{(j)}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e65e304cbb4f6948a3d52c183a45e5f4_l3.png "Rendered by QuickLaTeX.com") be ![N_j(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-97665436f1bfe04fc1ea1c3bff37ba2d_l3.png "Rendered by QuickLaTeX.com") sorted descending by size. ![S_i(t)=max\{j| N_{(j)}(t) \leq i\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e617fc8e42f7b66d9997b30ecdce25ff_l3.png "Rendered by QuickLaTeX.com") this is the amount of all processes where the ![i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-695d9d59bd04859c6c99e7feb11daab6_l3.png "Rendered by QuickLaTeX.com")-th event was reached at time ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"). Let ![E_i(t) = \sum_{j=0}^{S_i(t)}  X_{i(j)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bbbe074852fe544e3be4c2a03e496e32_l3.png "Rendered by QuickLaTeX.com"), here ![(j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b2df68841d7a627a41914e343b1096bd_l3.png "Rendered by QuickLaTeX.com") is determined by the ordering of ![N_{(j)}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e65e304cbb4f6948a3d52c183a45e5f4_l3.png "Rendered by QuickLaTeX.com"), this is also often referred to as exposure. ![\lambda_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-130188abd4690d701177358e4ad96950_l3.png "Rendered by QuickLaTeX.com") is now estimated with ![\hat{\lambda}_i=\frac{S_i(t)}{E_i(t)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fea54c387ffd66b635711dd354ae048c_l3.png "Rendered by QuickLaTeX.com").

The sum of order statistics exponential random variables is given by ![E_i(t) \sim \Gamma(\alpha= S_i(t), \beta= \lambda_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-002f9893c0cc116570517feab9a4b462_l3.png "Rendered by QuickLaTeX.com") [[1](#paperkey_7)] thus the joined distribution is given by\

(2)    ![\begin{eqnarray*}f_{E_i(t)}(x) = \sum_m  \frac{\lambda_i^m x^{m-1}}{\Gamma(m)}  e^{-\lambda_i x}    \mathbb{P}\left(S_i(t)=m\right).\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e00805be57e64532fa4bed2b8e1b8eac_l3.png "Rendered by QuickLaTeX.com")

Note that ![X_{ij}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f1eb6d955b36136010ddb28887d8f76b_l3.png "Rendered by QuickLaTeX.com") and ![S_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5554dec8764f63c626a9e7c0c8689b3a_l3.png "Rendered by QuickLaTeX.com") are not independent, in particular\

(3)    ![\begin{eqnarray*}\mathbb{E}(S_i(t)) = \sum_{j=0}^n \mathbb{P}(\sum_{k=0}^i X_{kj} \leq t) = n \int_0^t \sum_{k=0}^i C_{k,i} \lambda_k e ^{-\lambda_kx} dx = n -n \sum_{k=0}^i C_{k,i} e^{-\lambda_k t} \\\mathbb{P}\left(S_i(t)=m\right) =  \binom{n}{m}  \left(1 - \sum_{k=0}^i C_{k,i} e^{-\lambda_k t}\right)^m \left(\sum_{k=0}^i C_{k,i} e^{-\lambda_k t} \right)^{n-m}\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-668720aacf752793c9dc8f0a443379f1_l3.png "Rendered by QuickLaTeX.com")

\
 (see Statement 2), if the realisation of ![X_{ij}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f1eb6d955b36136010ddb28887d8f76b_l3.png "Rendered by QuickLaTeX.com") is relatively small than for given ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com") the probability that the event was observed is higher. For simplicity, in the following, we will consider a special case where ![t^*_i = max_j(T_{ji})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5ae6aa32a7921a61a0bdb2d4f1264c80_l3.png "Rendered by QuickLaTeX.com"), then ![S_i(t^*_i)=n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bef10c771b6a327b19b9dac5fce4d73f_l3.png "Rendered by QuickLaTeX.com") and the sum of exponential random variables is given by ![y = E_i(t^*_i) \sim \Gamma(\alpha= n, \beta= \lambda_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8e1a622f23c20f25f25da6e55139c7a1_l3.png "Rendered by QuickLaTeX.com"), thus

(4)    ![\begin{eqnarray*}\mathbb{E}\left(\hat{\lambda}_i\right)= &\int_0^\infty \frac{n}{y}\frac{\lambda_i^n}{\Gamma(n)}y^{n-1}e^{-\lambda_i y}dy = \frac{n \lambda_i^{n}_i \Gamma(n-1)}{\Gamma(n) \lambda_i^{n-1}} = \frac{n}{n-1} \lambda_i. \\Var\left(\hat{\lambda}_i\right)= &\int_0^\infty \left(\frac{n}{y}\right)^2 \frac{\lambda_i^n}{\Gamma(n)}y^{n-1}e^{-\lambda_i y}dy = \frac{n^2}{(n-1)^2(n-2)} \lambda_i^2.\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b331bf35fb8479937ca861d49ab78571_l3.png "Rendered by QuickLaTeX.com")

\
Therefore the estimator ![\mathbb{E}(\frac{n-1}{n} \hat{\lambda}_i ) = \lambda_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3a3ffd27a1c780325838db79ccd807d4_l3.png "Rendered by QuickLaTeX.com") is unbiased while the MSE is given by ![\mathbb{E}(\hat{\lambda}_i - \lambda_i)^2 = \frac{\lambda_i^2 (n+2)}{(n-1)(n-2)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fb41c1d682a5e009265952fdb943f48_l3.png "Rendered by QuickLaTeX.com"). Which reflects the well-known dichotomy between unbiasedness and minimal MSE.

For the general case\

(5)    ![\begin{eqnarray*}\mathbb{E}\left(\frac{S_i(t)-1}{S_i(t)} \hat{\lambda}_i |S_i(t)>0  \right) = \sum_{m=1}^n \int_0^\infty \frac{m-1}{m} \frac{m}{y} \frac{\lambda_i^m y^{m-1}}{\Gamma(m)}  e^{-\lambda_i y}   \mathbb{P}\left(S_i(t)=m\right) dy \\= \lambda_i \left(1- \mathbb{P}\left(S_i(t)=0\right)   \left) = \lambda_i \left(1 - \left(\sum_{k=0}^i C_{k,i} e^{-\lambda_k t} \right)^{n} \right)\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-667dd67b17f4502aecf46eaa73a51735_l3.png "Rendered by QuickLaTeX.com")

\
thus we face a slight bias, the cause of which is when there are too few observations available.

[1] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1007/0-8176-4487-3_11 "View document in publisher site") H. N. Nagaraja, “Order statistics from independent exponential random variables and the sum of the top order statistics,” in Advances in distribution theory, order statistics, and inference, N. Balakrishnan, J. M. Sarabia, and E. Castillo, Eds., Boston, MA: Birkhäuser boston, 2006, p. 173–185. \
 [[Bibtex]](javascript:void(0))

```
@Inbook{Nagaraja2006,
author="Nagaraja, H. N.",
editor="Balakrishnan, N.
and Sarabia, Jos{\'e} Mar{\'i}a
and Castillo, Enrique",
title="Order Statistics from Independent Exponential Random Variables and the Sum of the Top Order Statistics",
bookTitle="Advances in Distribution Theory, Order Statistics, and Inference",
year="2006",
publisher="Birkh{\"a}user Boston",
address="Boston, MA",
pages="173--185",
abstract="Let X(1)<...
```