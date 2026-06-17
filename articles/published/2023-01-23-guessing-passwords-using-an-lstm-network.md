---
categories:
- Coding
- Introduction
- Passwords
- Python
- Python
date: '2023-01-23'
slug: guessing-passwords-using-an-lstm-network
status: publish
tags: []
title: Guessing Passwords using an LSTM Network
wp_id: 3904
wp_modified: '2023-01-30T20:18:25'
---

## Introduction

A while ago I applied NLP strategies to implement an algorithm that is capable to guess a password. Since then a new method called transformer was developed and successfully used in many NLP tasks. Before transformers were the method of choice, LSTM Models dominated the field. In this article we will lay down a setup for such an LSTM Model to guess passwords and derive why a network might be better suited than the Markov chain model presented in this post. \
\
A shot recap of our notation: Let ![X \in \mathbb{X} \, ,X=x_1 x_2 x_3 \dots x_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-91e7a99d4236a049010d0b0734289f36_l3.png "Rendered by QuickLaTeX.com") be a password and the random variables ![x_i \in \mathbb{A}, E \in \mathbb{N}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-81c618a31cc1f5fe91ad7fd66a31224d_l3.png "Rendered by QuickLaTeX.com") the corresponding letters and password length. ![\mathbb{X}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0a912bd9abe1e6796446fdfedc0ca07c_l3.png "Rendered by QuickLaTeX.com") is the space of all passwords and ![\mathbb{A}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fdb36901bfeee1bb4b059305c252e86_l3.png "Rendered by QuickLaTeX.com") corresponds to the used alphabet, for example if we allow only for lower case letters then ![\mathbb{A} =\{a,b,c, \dots, y,z \}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b6ca4ae7b57a6cdb35d8c4d25a91077d_l3.png "Rendered by QuickLaTeX.com"). As usual this forms a discrete probability space given by ![(\mathbb{X}, P)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f7039d9bf15342da0a6a9586280cb3dc_l3.png "Rendered by QuickLaTeX.com"). The task to solve is to derive ![P(x_i|x_{i-1},\dots,x_{1})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f42f8569442b1311959445f0a9ee24fa_l3.png "Rendered by QuickLaTeX.com").\
\
In the Markov chain example it is assumed that ![P(x_i|x_{i-1},\dots,x_{1}) = P(x_i|x_{i-1})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ff8b039b2e1c86bd633a08088054b1e0_l3.png "Rendered by QuickLaTeX.com") which obviously falls short. Our strategy to overcome this problem was to use “![n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b170995d512c659d8668b4e42e1fef6b_l3.png "Rendered by QuickLaTeX.com")-grams”, therefore one can look at sequences of length ![n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b170995d512c659d8668b4e42e1fef6b_l3.png "Rendered by QuickLaTeX.com") instead of a single letter. However with raising ![n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b170995d512c659d8668b4e42e1fef6b_l3.png "Rendered by QuickLaTeX.com") a major problem is that the possibility to observe a each sequence in the training set decreases which will lead to an underestimation of the probability for such sequences. This is where Recurrent Neuronal Networks (RNN) step in (LSTM is a specific RNN). \

## The terminology of neuronal networks

To start with, we will first have a brief look at more simple networks. There has been a great deal of hype surrounding\
neural networks, making them seem magical and mysterious. However, they are just nonlinear statistical models [[1](#paperkey_12)]. In particular, a neuronal network is a class of functions mapping a random variable ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") ![f: X \rightarrow Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e1c7e5f73db7b3234648b93f62cebaa3_l3.png "Rendered by QuickLaTeX.com"). However the terminology in the literature is quiet different. [[2](#paperkey_13)] gave the following translation:\

- **variables** are called *features*
- **independent** variables are called *inputs*
- **predicted values** are called *outputs*
- **dependent variables** are called *targets* or *training values*
- **residuals** are called *errors*
- **estimation** is called *training, learning, adaptation*, or *self-organization*
- an **estimation criterion** is called an *error function, cost function*, or *Lyapunov function*
- **observations** are called *patterns* or *training pairs*
- **parameter estimates** are called (synaptic) *weights*
- **interactions** are called *higher-order neurons*
- **transformations** are called *functional links*
- **regression and discriminant analysis** are called s*upervised learning or heteroassociation*
- **data reduction** is called *unsupervised learning, encoding*, or *autoassociation*
- **cluster analysis** is called *competitive learning* or *adaptive vector quantization*

The statistical terms **sample** and **population** do not seem to have Neuronal Network equivalents. However, the data are often divided into a *training set* and *test set* for cross-validation.

## Feed-Forward Neuronal Networks

\
Our next work guessing task can be understood like as a classification problem where the number of classes corresponds to the size of ![K=|\mathbb{A}|](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fdc0ef30a648d08696485e914813fcb0_l3.png "Rendered by QuickLaTeX.com"). Our target in this case is to predict the actual letter ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") based on the previously observed letter ![x_{i-1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-123fc114013084611bd9def214d3992a_l3.png "Rendered by QuickLaTeX.com"). Since neuronal nets can not deal with letters directly we have to convert them into an input vector ![\mathbf{x}_{i-1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9105a6acb8f74bcca88563a8ace22040_l3.png "Rendered by QuickLaTeX.com") with ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") components and a target vector ![\mathbf{x}_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ecf030f940f517787145a85f7a90f283_l3.png "Rendered by QuickLaTeX.com") which has also ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") components (in general the size of the vectors can differ). Both vectors are dummy variables (one-hot encoding) such that the ![j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43c82d5bb00a7568d935a12e3bd969dd_l3.png "Rendered by QuickLaTeX.com")-th component of ![\mathbf{x}_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ecf030f940f517787145a85f7a90f283_l3.png "Rendered by QuickLaTeX.com") is ![1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4868771cbc422b5818f85500909ce433_l3.png "Rendered by QuickLaTeX.com") if the observed letter ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") is at the ![j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43c82d5bb00a7568d935a12e3bd969dd_l3.png "Rendered by QuickLaTeX.com")-th position of the alphabet ![\mathbb{A}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fdb36901bfeee1bb4b059305c252e86_l3.png "Rendered by QuickLaTeX.com") and ![0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a5e437be25f29374d30f66cd46adf81c_l3.png "Rendered by QuickLaTeX.com") else. \
Additionally we construct ![M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10ebb71bad275c1815a8f2a8c5dea0be_l3.png "Rendered by QuickLaTeX.com") derived features ![Z_m](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5cdc407753eaa4e52094bfba1608f610_l3.png "Rendered by QuickLaTeX.com"), these features can be compared to a linear basis generated from the data. ![\mathbf{Z}=Z_1,\dots, Z_M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1cbdb72998ee750f004368dae05a7d2a_l3.png "Rendered by QuickLaTeX.com") is called the hidden layer, since the outputs of ![\mathbf{Z}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6269ace06802a01edf92fa0c7ab28acc_l3.png "Rendered by QuickLaTeX.com") are not directly observed. Adding more then one hidden layer enables the network to capture interactions. Thus each component ![k=1,\dots,K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-01dfb9c1b06c1afb8945451605627b33_l3.png "Rendered by QuickLaTeX.com")for the estimator ![\hat{\mathbf{x}}_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a1975c50d9e3ff1089be3b0bb283224c_l3.png "Rendered by QuickLaTeX.com") of ![\mathbf{x}_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ecf030f940f517787145a85f7a90f283_l3.png "Rendered by QuickLaTeX.com") is modeled by ![f_k(\mathbf{x}_{i-1})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e849c36f02e1a9f856158e404aae0a1c_l3.png "Rendered by QuickLaTeX.com") as a linear combination of ![Z_m](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5cdc407753eaa4e52094bfba1608f610_l3.png "Rendered by QuickLaTeX.com"):\

     ![\[\arraycolsep=1.4pt\def\arraystretch{2.2}\begin{array}{l}Z_m= \sigma( \alpha_{0m} + \alpha^T_{m} \mathbf{x}_{i-1}), m=1,\dots, M \\T_k= \beta_{0k}+\beta^T_{k}\mathbf{Z}, k=1,\dots,K \\f_k(\mathbf{x}_{i-1})=g_k(\mathbf{T}),k=1,\dots,K\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cbe12e4f7f12b8990c485f3a20593d40_l3.png "Rendered by QuickLaTeX.com")

\
where ![\mathbf{T}=T_1,\dots,T_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e0ddecaaae888c7d8a8a0d2407d7f358_l3.png "Rendered by QuickLaTeX.com"). A popular choice for ![g_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-835de27920507b720f80782dbc8fffb7_l3.png "Rendered by QuickLaTeX.com") is the softmax function ![g_k(\mathbf{T})=\frac{e^{T_k}}{\sum_{l=1}^Ke^{T_l}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-31ea739d0fc35e3a1d11e487f6ef5ff6_l3.png "Rendered by QuickLaTeX.com") which ensures that ![f_k(\mathbf{x}_{i-1})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e849c36f02e1a9f856158e404aae0a1c_l3.png "Rendered by QuickLaTeX.com") is between [0,1]. In a regression setup frequently ![g_k(\mathbf{T})=T_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f15c1c34bb0ee261279f65d7968f6cf9_l3.png "Rendered by QuickLaTeX.com") is used. ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com") is an “activation function, popular choices are ![\sigma(x)=tanh(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c348239cf53bc5e07328121a73506561_l3.png "Rendered by QuickLaTeX.com") or the sigmoid function ![\sigma(x)=\frac{1}{1+e^{-x}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-16f6c3a3e35b316ac818835a33003b27_l3.png "Rendered by QuickLaTeX.com").\
The system of equations has unknown variables ![\theta=(\alpha, \beta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-54d2639b6d31aad5af32a3b6d19fb6cf_l3.png "Rendered by QuickLaTeX.com") where ![\alpha \in \mathbb{R}_{M \times K+1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8af46db137f5352f085c877b3af46179_l3.png "Rendered by QuickLaTeX.com"), ![\beta \in \mathbb{R}_{K+1 \times M}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7aab23d499bf13580e57eb9df0ab165d_l3.png "Rendered by QuickLaTeX.com") to be estimated from the data.\
Assume that we observe ![j=1,\dots,N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2a5074cc6ab34d750ae4432c6a668f23_l3.png "Rendered by QuickLaTeX.com") passwords with length ![E_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-83ecb550a2c9629881ccf5808cd5d643_l3.png "Rendered by QuickLaTeX.com") resulting in pairs consisting of ![(\mathbf{x}_{i-1j},\mathbf{x}_{ij})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b0369fcfc6c89efb057678d2d07b7f23_l3.png "Rendered by QuickLaTeX.com"). To fit the network we have to define a suitable loss function, since we deal with a classification problem we use the cross-entropy loss function ![R(\theta) = - \sum_{j=1}^N \sum_{i=2}^{E_j} \mathbf{x}_{ij}^T log(f(\mathbf{x}_{i-1j}, \theta))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7435f5cab24e9521070a808ceb83e7ba_l3.png "Rendered by QuickLaTeX.com") minimized over ![\theta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-356a08e839ab6974a16448e16e56745d_l3.png "Rendered by QuickLaTeX.com"). \

## Recurrent Neuronal Networks and LSTM

By construction the Feed-Forward network suffers from the same issue as Markov-Chain attempt, we only look at the previous letter ignoring the entire prior sequence. To model such time dependent sequences RNN steps in. We will therefore extend our network, allowing to use previous letters of the password sequences by altering the hidden layer such that an estimator for ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") is given by\

     ![\[\arraycolsep=1.4pt\def\arraystretch{2.2}\begin{array}{l}Z_{im}= \sigma( \alpha_{0m} + \alpha^T_{m}\mathbf{x}_{i-1}+ w^T_{m} \mathbf{Z}_{i-1}), m=1,\dots, M \\T_{ik}= \beta_{0k}+\beta^T_{k}\mathbf{Z}_i, k=1,\dots,K \\f_k(\mathbf{x}_{1}, \dots, \mathbf{x}_{i-1})=g_k(\mathbf{T}_i),k=1,\dots,K\end{array}\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6ca0c6f2b8b27b737dc84bfaf36d9d87_l3.png "Rendered by QuickLaTeX.com")

\
This model now consists of unknown variables ![\alpha \in \mathbb{R}_{M \times K+1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8af46db137f5352f085c877b3af46179_l3.png "Rendered by QuickLaTeX.com"), ![\beta \in \mathbb{R}_{K+1 \times M}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7aab23d499bf13580e57eb9df0ab165d_l3.png "Rendered by QuickLaTeX.com"), ![w \in \mathbb{R}_{M \times M}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-93d3391cb8bb1f36147501d5790fad83_l3.png "Rendered by QuickLaTeX.com") to be estimated from the data. Assume again that we observe ![j=1,\dots,N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2a5074cc6ab34d750ae4432c6a668f23_l3.png "Rendered by QuickLaTeX.com") passwords with length ![E_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-83ecb550a2c9629881ccf5808cd5d643_l3.png "Rendered by QuickLaTeX.com"). To train the network we use all possible subsequences ![(\mathbf{x}_{1j}, \mathbf{x}_{2j})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-35c157ce01d82435da339a144db67191_l3.png "Rendered by QuickLaTeX.com"), ![(\mathbf{x}_{1j}\mathbf{x}_{2j}, \mathbf{x}_{3j})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8a6bb9b7171e4c9ce32081e20253a079_l3.png "Rendered by QuickLaTeX.com"), … .\
\
An RNN works well to handle sequential data but runs into problems if influential letters are far away. This is not much a problem of the network itself, but rather of the methods used to train it. Neuronal Networks where fitted using [backpropagation](https://en.wikipedia.org/wiki/Backpropagation), the problem concerning RNN are vanishing/exploding gradients [[3](#paperkey_14)] LSTM (to a major part) solves this issue by allowing to connect letters which are far away. This is archived with having a shortcut in ![C_{im}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-db662678310fae1c34127aaac54abc59_l3.png "Rendered by QuickLaTeX.com") to connect the LSTM cells ![C_{jm}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1d8f8785293cf2b644fb1a11dec9e33c_l3.png "Rendered by QuickLaTeX.com") of different letters . \

     ![\[\arraycolsep=1.4pt\def\arraystretch{2.2}\begin{array}{l}I_{im} = \sigma_1 ( \alpha^A_{0m} + \alpha^A^T_{m}\mathbf{x}_{i-1}+ w^A^T_m \mathbf{Z}_{i-1} ), m=1,\dots, M\\F_{im} = \sigma_2 ( \alpha^F_{0m} + \alpha^F^T_{m}\mathbf{x}_{i-1}+ w^F^T_m \mathbf{Z}_{i-1} ), m=1,\dots, M\\O_{im} = \sigma_3 ( \alpha^O_{0m} + \alpha^O^T_{m}\mathbf{x}_{i-1}+ w^O^T_m \mathbf{Z}_{i-1} ), m=1,\dots, M\\\tilde{C}_{im} = \sigma_4 ( \alpha^G_{0m} + \alpha^G^T_{m}\mathbf{x}_{i-1}+ w^G^T_m \mathbf{Z}_{i-1} ), m=1,\dots, M\\C_{im}= C_{i-1 m} F_{im} +I_{im} \tilde{C}_{im}, m=1,\dots, M\\Z_{im}=O_{im} \sigma_5(C_{im}) , m=1,\dots, M\\T_{ik}= \beta_{0k}+\beta^T_{k}\mathbf{Z}_i, k=1,\dots,K \\f_k(\mathbf{x}_{1}, \dots, \mathbf{x}_{i-1})=g_k(\mathbf{T}_i),k=1,\dots,K\end{array}\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b9e78c2fd7c7e400c71e16421aa2668c_l3.png "Rendered by QuickLaTeX.com")

\
In the literature ![\sigma_4](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-01cd282186f933c8734c834cf9a393ab_l3.png "Rendered by QuickLaTeX.com") and ![\sigma_5](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-51d7be2069eeadd5f38ef1d17cc5708a_l3.png "Rendered by QuickLaTeX.com") are represented by ![tanh(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0954237e86c5a66d4691a73b7e6e98cb_l3.png "Rendered by QuickLaTeX.com"), while the choice of ![\sigma_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-465f83ac90ca1844a03b41e8ca8d99b1_l3.png "Rendered by QuickLaTeX.com") to ![\sigma_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-17eeed9c0e5cec2cbce46f06add406bf_l3.png "Rendered by QuickLaTeX.com") is usually a sigmoid function.

## Results

The proposed methods where used to fit a Feedforward, a Recurrent Neuronal net as well as a Long-Short-Term-Memory net. To train the network the 10.000.000 most popular passwords where used. The fitted models can be found in my [github repo](https://github.com/heikowagner/thebigdatablog/tree/master/jupyter_notebooks/neuronalnets/models) the corresponding code can be found [here](https://github.com/heikowagner/thebigdatablog/blob/master/jupyter_notebooks/neuronalnets/train_and_predict.ipynb). Figure 1-3 represent the probabilities for the next letter if “lov” was observed. We can see that while LSTM and RNN predict “e” as the most probable letter the Feedforward net prefers “eof” which means that the passwords ends. This misjudgment is not surprising, since all passwords have in common that they end at some point. Because the FF network does not know the length of the password, the best guess is the end of the password. RNN and LSTM do not make this mistake. It is noticeable that the probabilities look similar, but in the LSTM network the probabilities concerning “e” are more pronounced.

[![](https://www.thebigdatablog.com/wp-content/uploads/2023/01/ff-1024x264.png)](https://www.thebigdatablog.com/wp-content/uploads/2023/01/ff.png)

**Figure 1:** Probabilities predicted by the FF Net after the sequence “lov” was observed.

[![](https://www.thebigdatablog.com/wp-content/uploads/2023/01/rnn-1024x264.png)](https://www.thebigdatablog.com/wp-content/uploads/2023/01/rnn.png)

**Figure 2:** Probabilities predicted by the RNN after the sequence “lov” was observed.

[![](https://www.thebigdatablog.com/wp-content/uploads/2023/01/lstm-1024x264.png)](https://www.thebigdatablog.com/wp-content/uploads/2023/01/lstm.png)

**Figure 3:** Probabilities predicted by the LSTM Net after the sequence “lov” was observed.

[1] T. Hastie, R. Tibshirani, and J. Friedman, The elements of statistical learning, New York, NY, USA: Springer new york inc., 2001. \
 [[Bibtex]](javascript:void(0))

```
@book{hastie01statisticallearning,
added-at = {2008-05-16T16:17:42.000+0200},
address = {New York, NY, USA},
author = {Hastie, Trevor and Tibshirani, Robert and Friedman, Jerome},
biburl = {https://www.bibsonomy.org/bibtex/2f58afc5c9793fcc8ad8389824e57984c/sb3000},
interhash = {d585aea274f2b9b228fc1629bc273644},
intrahash = {f58afc5c9793fcc8ad8389824e57984c},
keywords = {ml statistics},
publisher = {Springer New York Inc.},
series = {Springer Series in Statistics},
timestamp = {2008-05-16T16:17:43.000+0200},
title = {The Elements of Statistical Learning},
year = 2001
}
```

[2] W. Sarle, “Neural networks and statistical models.” 1994. \
 [[Bibtex]](javascript:void(0))

```
@inproceedings{Sarle1994NeuralNA,
title={Neural Networks and Statistical Models},
author={Warren Sarle},
year={1994}
}
```

[3] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural computation, vol. 9, pp. 1735-1780, 1997. \
 [[Bibtex]](javascript:void(0))

```
@article{Hochreiter1997LongSM,
title={Long Short-Term Memory},
author={Sepp Hochreiter and J{\"u}rgen Schmidhuber},
journal={Neural Computation},
year={1997},
volume={9},
pages={1735-1780}
}
```