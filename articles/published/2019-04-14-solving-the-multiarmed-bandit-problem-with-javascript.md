---
categories:
- All Articles
- Coding
- Fundamentals
- Introduction
- JavaScript
date: '2019-04-14'
slug: solving-the-multiarmed-bandit-problem-with-javascript
status: publish
tags: []
title: Solving the Multiarmed Bandit problem with JavaScript
wp_id: 1663
wp_modified: '2026-06-11T18:47:37'
---

## 1. Formulation of the Multiarmed Bandit Problem

Consider the following problem: A gambler enters a casino with ![K \in \mathbb{N}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8de398f1b4558ab45b9096f50a5fa5c5_l3.png "Rendered by QuickLaTeX.com") slot machines. The probability to receive a reward ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com") for each slot machine follows different, unknown probabilities, e.g. we are facing a set of unknown distributions ![\{\Pi_{1},\dots , \Pi _{K}\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3f17b7cdc71b0e8bcaf5878962e93d08_l3.png "Rendered by QuickLaTeX.com") with associated expected values ![\{\mu_{1},\dots ,\mu_{K}\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f091e7e6f514741d0b2a8a465402eaa9_l3.png "Rendered by QuickLaTeX.com") and variances ![\{\sigma^2_{1},\dots ,\sigma^2_{K}\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2c8823ba2784fef92c8ccb8eec656293_l3.png "Rendered by QuickLaTeX.com").

In each turn ![t=1, \dots, T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-68767a68d09a41745ed560b5d273044a_l3.png "Rendered by QuickLaTeX.com") the gambler can play the lever of one slot machine ![j(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e8d0bd935186e2675af3eae80da5fe8a_l3.png "Rendered by QuickLaTeX.com") and observes the associated reward ![r(t) \sim  \Pi _{j(t)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4930c9ac35e66b9f22b197b600ce0810_l3.png "Rendered by QuickLaTeX.com"). The objective is now with which strategy the gambler should play to maximize his earning ( or minimizing his losses in case he has to pay a fee to pull a lever 😉 ).

If the distributions are known, then one would simply play all the times at the machine with the highest probability of winning. The average reward following this strategy will then be ![\mu^*=max_{i=1,\dots,K} \mu_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-56b74e9ef2766870ba57a10bc7a6edc3_l3.png "Rendered by QuickLaTeX.com").

\
Since the probabilities are unknown, a naive solution would for example to play several times, say ![\frac{T}{2K}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4a97b75585d863704f976db4c2f1c14b_l3.png "Rendered by QuickLaTeX.com"), at the fist machine, then several times at the second and so on to get a decent estimator idea which machine is the best one and then keep playing. However there are certain drawbacks with this approach, first of all one will play at least ![\frac{(K-1)T}{2K}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-787f6a2bcf4a2899bbc1e2b8dc474a8d_l3.png "Rendered by QuickLaTeX.com") times at an inferior machine and secondly one can end up choosing the wrong machine in the end. The chance ending up with the wrong machine can be decreased by raising the number of turn played at each machine, but then one will play even more often at a inferior machine. To measure the performance of a certain strategy we introduce the concept of *total expected regret*, defined by

     ![\[R_T = T \mu^* - \sum_{t=1}^{T} r(t).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3daa876f24289811101365e7947715ac_l3.png "Rendered by QuickLaTeX.com")

[[1](#paperkey_26)] states that regret grows at least logarithmically. Therefore an algorithm is said to solve the multi-armed bandit problem if it can match this lower bound such that ![R_T = \mathcal{O}(log(T))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dbdaf65983a8854901187004569d1489_l3.png "Rendered by QuickLaTeX.com"). For the naive solutions we thus can derive that:

Play each machine with an uniform random propability:

     ![\[ E(R_T)= T \mu^* - \frac{T}{K} \sum_{i=1}^K \mu_i = T(\mu^* - K^{-1}  \sum_{i=1}^K \mu_i) = \mathcal{O}(T)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e33fec695a1f00035e5ae51aef501582_l3.png "Rendered by QuickLaTeX.com")

Play each machine ![M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10ebb71bad275c1815a8f2a8c5dea0be_l3.png "Rendered by QuickLaTeX.com") times, play infinitely the machine giving the highest payoff:

     ![\[ E(R_T)=T \mu^* - \frac{M}{K} \sum_{i=1}^K \mu_i - \frac{T-M}{K} \sum_{i=1} ^K \sum_{i \neq k} P( \hat{\mu_i}(M) >  \hat{\mu_k}(M)) \mu_i  \]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a7aab709a47268a10cfe7a64f0dfc537_l3.png "Rendered by QuickLaTeX.com")

     ![\[   =  \mathcal{O}(1) + T(\mu^* - K^{-1} \sum_{i=1} ^K \sum_{i \neq k} P( \hat{\mu_i}(M) >  \hat{\mu_k}(M)) \mu_i)  =  \mathcal{O}(T)  \]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-763cead6c315f28092df0297e2a63742_l3.png "Rendered by QuickLaTeX.com")

where ![\hat{\mu_i}(M)=\frac{1}{n_i} \sum_{t=1}^M r(t) \mathbf{I}(j(t)=i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-549ded562d60ef8d06413211648da11b_l3.png "Rendered by QuickLaTeX.com") is the average winning of machine ![i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-695d9d59bd04859c6c99e7feb11daab6_l3.png "Rendered by QuickLaTeX.com") at time ![M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10ebb71bad275c1815a8f2a8c5dea0be_l3.png "Rendered by QuickLaTeX.com").

In Blog post we will discuss the Upper Confidence Bounds (UCB1) algorithm proposed by [[2](#paperkey_27)] . UCB1 is the simplest algorithm out of the UCB family. The idea of the algorithm is to initially try each lever once. Record the reward gained from each machine as well as the times the machine has been played. At each turn ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com") select the machine

     ![\[j(t) = argmax_{i=1,\dots K} \left( \hat{\mu_i}(t) +  \sqrt{\frac{2 log(t)}{n_i} } \right)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cffc168d762a35b82428e26d15ff6055_l3.png "Rendered by QuickLaTeX.com")

which depends on the average winning ![\hat{\mu_i}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-61644c558d12a87ae0da72a0e98a1b6b_l3.png "Rendered by QuickLaTeX.com") as well as the number ![n_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1ffdddde68452977938ddffe328f4b78_l3.png "Rendered by QuickLaTeX.com") the machine has been played, and the trial number ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"). \
[[2](#paperkey_27)] show that for UCB1

     ![\[E(R_T) \leq 8 \sum_{\mu_i<\mu^*} \frac{log(T)}{\mu^*-\mu_i} + \mathcal{O}(1) .\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-373080c5f0cfcd273328c9a8bb277b48_l3.png "Rendered by QuickLaTeX.com")

Hence UCB1 achieves the optimal regret and is said to solve the multi-armed bandit problem.

An advantage of UCB1 is that the algorithm is easy to implement. In the following we present an implementation of UCB1 using JavaScript. An advantage of JavaScript is that is a functional programming language. This means that we can pass functions as arguments of functions. In terms of the multi armed bandit algorithm this allows us to pass entire sample functions to the algorithm.

```
  /*
--Bandit.js
-This Program computes an optimal lever and average return of the multiarmed bandit problem
--Input
f=[f_1(x),...,f_K(x)]       -An Array of size K containing functions given a certain reward r eg. binomial or a normal distribution with different means
T                           -Runs to retrieve the decision (the first, t or  N  will terminate the algorithm)
--Output
sum \mu                     -the average revenue
x_out
--Heiko Wagner 2019
*/

bandit = function(f, T) {
    //pull each lever once
    var x_out = f.map((x) => [x(), 1])
    var a;
    for (var t = 0; t < T; t++) {
        //determine the position with the highest value
        var j = x_out.map((x) => x[0] / x[1] + Math.sqrt((2 * Math.log(t)) / x[1]))
        a = j.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)
        //pull maximum lever
        x_out[a] = [x_out[a][0] + f[a](), x_out[a][1] + 1]
    }
    return [x_out.map((x)=>x[0]).reduce( (a,b) =>a+b)/T, x_out]
}

//Example
var K = 10

var f = []
for (var k = 0; k < K; k++) {
    f.push(eval('() => Math.random()*' + k))
}

bandit(f, 10000)
```

## Multistage Mulitarmed Bandit

Suppose now the gambler has not only to choose the machine, but prior he has to choose one out of ![K' \in \mathbb{N}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-853414dba226148f84139ab6a2577310_l3.png "Rendered by QuickLaTeX.com") casinos. The question here is which casino is the best. From a theoretical point of view this setup is not very interesting because the because it can be reformulated to a classical one stage multiarmed bandit problem. However from an implementation point of view, especially if we add more stages with an complicated possible unknown structure, we are facing a demanding problem. Here the functional programming approach of JavaScript plays out its strengths. In the following we will thus present an example solving the multiarmed bandit problem with two stages.

```
//Let's define a Casino Class
class Casino {
    constructor(K, m) {
        this.K = K;
        this.m = m;
    }
    levers() {
        var f = []
        for (var k = 0; k < this.K; k++) {
            f.push(eval('() => Math.random()*' + k * this.m))
        }
        return f
    }
}

var K_dash = 5
var K = 10

//To build a two stage bandit problem we build 

var f_2 = []
for (var k = 1; k <= K_dash; k++) {
    f_2.push(eval('() => { return bandit(new Casino(' + K + ',' + k + ').levers() ,1000)[0] }'))
}

bandit(f_2, 1000)
```

[1] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/https://doi.org/10.1016/0196-8858(85)90002-8 "View document in publisher site") T. L. Lai and H. Robbins, “Asymptotically efficient adaptive allocation rules,” Advances in applied mathematics, vol. 6, iss. 1, pp. 4-22, 1985. \
 [[Bibtex]](javascript:void(0))

```
@article{LAI19854,
title = "Asymptotically efficient adaptive allocation rules",
journal = "Advances in Applied Mathematics",
volume = "6",
number = "1",
pages = "4 - 22",
year = "1985",
issn = "0196-8858",
doi = "https://doi.org/10.1016/0196-8858(85)90002-8",
url = "http://www.sciencedirect.com/science/article/pii/0196885885900028",
author = "T.L Lai and Herbert Robbins"
}
```

[2] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1023/A:1013689704352 "View document in publisher site") P. Auer, N. Cesa-Bianchi, and P. Fischer, “Finite-time analysis of the multiarmed bandit problem,” Machine learning, vol. 47, iss. 2, p. 235–256, 2002. \
 [[Bibtex]](javascript:void(0))

```
@Article{Auer2002,
author="Auer, Peter
and Cesa-Bianchi, Nicol{\`o}
and Fischer, Paul",
title="Finite-time Analysis of the Multiarmed Bandit Problem",
journal="Machine Learning",
year="2002",
month="May",
day="01",
volume="47",
number="2",
pages="235--256",
abstract="Reinforcement learning policies face the exploration versus exploitation dilemma, i.e. the search for a balance between exploring the environment to find profitable actions while taking the empirically best action as often as possible. A popular measure of a policy's success in addressing this dilemma is the regret, that is the loss due to the fact that the globally optimal policy is not followed all the times. One of the simplest examples of the exploration/exploitation dilemma is the multi-armed bandit problem. Lai and Robbins were the first ones to show that the regret for this problem has to grow at least logarithmically in the number of plays. Since then, policies which asymptotically achieve this regret have been devised by Lai and Robbins and many others. In this work we show that the optimal logarithmic regret is also achievable uniformly over time, with simple and efficient policies, and for all reward distributions with bounded support.",
issn="1573-0565",
doi="10.1023/A:1013689704352",
url="https://doi.org/10.1023/A:1013689704352"
}
```