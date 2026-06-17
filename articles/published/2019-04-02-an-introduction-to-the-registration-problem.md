---
categories:
- All Articles
- Fundamentals
- Introduction
date: '2019-04-02'
slug: an-introduction-to-the-registration-problem
status: publish
tags: []
title: An introduction to the Registration Problem
wp_id: 1512
wp_modified: '2026-06-11T18:47:33'
---

\
[![](https://www.thebigdatablog.com/wp-content/uploads/2019/01/Rplot02-1-300x212.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2019/01/Rplot02-1.jpg)

**Figure 1:** Pinch Force ![x_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3bbf0a52e4b9b71aa782e71a2b9ec63a_l3.png "Rendered by QuickLaTeX.com") measured over time ![t=[0,0.3]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-30034172b14274bfa576bf83c9f8d10f_l3.png "Rendered by QuickLaTeX.com") seconds for subjects ![i=1,\dots,20](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-37b47637fc5e7f6b15b74850d9128229_l3.png "Rendered by QuickLaTeX.com"). The blue curve shows the mean ![\bar{x}(t) := \sum_{i=1}^{20} x_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c427d67e1bfdcfd9ac6698ca07e9cb17_l3.png "Rendered by QuickLaTeX.com").

To explain the registration problem i will start with an example. In Figure 1 the [pinch force dataset](https://rdrr.io/cran/fda/man/pinch.html) is shown, to collect the data a group of 20 subjects were asked to press a button as hard if they can after they hear a sound signal. The pressure was then recorded every 2 milliseconds, resulting in 151 observations. Since reaction times of the subjects differ we can clearly see some shift in the curves reflecting the pressure. The problem with this kind of shifted data is now that even very simple statistical measures, like mean or variance, are not meaningful. To see this take a look at the blue curve which is the sample mean ![\hat{x}(t)=\sum_{i=1}^N x_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a527e92c2b8ed1e034f061ea50989e7c_l3.png "Rendered by QuickLaTeX.com"). It is visible, that the mean curve does not reflect the shape of the sample curves and even worse the highest point of this curve is smaller than the smallest sample curve. To obtain information about the mean pressure this curve is therefore a bad measure. In case of the pinch fore data an obvious way to fix this problem is to align the curves at certain landmarks, for example the peaks of each curve. This is landmark registration is for example covered by [[1](#paperkey_28), [2](#paperkey_29)], [[3](#paperkey_30)] or [[4](#paperkey_31)]. However, Landmark registration has certain drawbacks. Considering more complex problems defining the Landmarks becomes ugly very fast, especially when working with more than one spatial dimension. It is also not clear how to choose the Landmarks, consider for example curves where some are wider than others, in this case sometimes also inflection points are used as landmarks. This then leads to a methods which rely on minimizing a distance ![d(x_i \circ h_i ,\gamma)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3f68427a260a7eb21f66460a51113ab7_l3.png "Rendered by QuickLaTeX.com") between registered functions ![y_i (t) = x_i (h_i (t))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1563bd8e4a3973fa392ef1d544db7e67_l3.png "Rendered by QuickLaTeX.com") and a template ![\gamma(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f1694b647ab256b7735228b2879d9a58_l3.png "Rendered by QuickLaTeX.com"), for example one curve out of the sample. See [[5](#paperkey_32)], [[6](#paperkey_33)], [[7](#paperkey_34)], or [[8](#paperkey_35)] for more insights. This strategy works very well in many situations but also has severe problems. Consider for example a sample of curves where some curve have one peak while others have two. A registration method that minimizing a distance between the curves and a one peaked template, will then then to pinch the curves with two peaks, see [[6](#paperkey_33)].

[![](https://www.thebigdatablog.com/wp-content/uploads/2019/01/Rplot03-1-300x212.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2019/01/Rplot03-1.jpg)

**Figure 2:** Registered curves ![x_i(h_i(t))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8025ea769b8da992777bb61316058d13_l3.png "Rendered by QuickLaTeX.com") using landmark registration. The structural mean ![\bar{x}_h(t) := \sum_{i=1}^{20} x_i(h_i(t))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-41629f1aaa2633d6bd614788adb58691_l3.png "Rendered by QuickLaTeX.com") now reflects the characteristics of the sample curves

An alternative approach was developed by [[9](#paperkey_36)] and [[10](#paperkey_37)]. Where registration was considered as a tool for statistical analysis. Whenever the random functions ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") possess “bounded shape variation”, then there exists a finite ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") and warping functions ![h_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c59cfc50326c96eff701e9f2dda48f94_l3.png "Rendered by QuickLaTeX.com") such that with probability 1

(1)    ![\begin{eqnarray*}  x_i(h_i(t)) = \sum_{j=1}^K a_{ij} \gamma_j(t) \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b7fb8a927a76ecf6c3ed1a40bb069785_l3.png "Rendered by QuickLaTeX.com")

for some basis functions ![\gamma_1,\dots,\gamma_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9f3425a02169d7ab20d1ab2d696e748_l3.png "Rendered by QuickLaTeX.com") and individually different coefficients ![a_{i1},\dots,a_{iK}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-176431cf64850a38d0d764655fb7111c_l3.png "Rendered by QuickLaTeX.com"). An advantage of this way to look at the registration problem that it allows curves to be registered with a more complex structure than the curves displayed in figure 1. Traditional registration procedures can be understood as a registration with ![K=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6e4ce6e34549ac1c10ab9f8832c52ed3_l3.png "Rendered by QuickLaTeX.com") and are troubled with curves as displayed in figure 3. Decomposition [1](#id695865007) is unfortunately not unique if ![K\geq 2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6738afa544c251532ec697e3f89a9b16_l3.png "Rendered by QuickLaTeX.com"). There will then exist different sets of basis functions ![\gamma_1,\dots,\gamma_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9f3425a02169d7ab20d1ab2d696e748_l3.png "Rendered by QuickLaTeX.com") and ![\gamma_1,\dots,\gamma_K^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1b142eb856a330288f8e2e7353be8cb5_l3.png "Rendered by QuickLaTeX.com") such that

(2)    ![\begin{eqnarray*} x_i(h_i(t))=\sum_{j=1}^Ka_{ij}\gamma_j(t)\quad\text{ and } x_i(h_i^*(t))=\sum_{j=1}^Ka_{ij}^*\gamma_j^*(t)\quad\text{ for } h_i\neq h_i^* \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e4be61e7a4e4fcbade894f88187fb84f_l3.png "Rendered by QuickLaTeX.com")

The corresponding spaces ![{\cal L}_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e04a74de688fa466206a992c808b4494_l3.png "Rendered by QuickLaTeX.com") and ![{\cal L}_K^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d2dda44f7c6de91d10b89c80e3bf3def_l3.png "Rendered by QuickLaTeX.com") spanned by ![\gamma_1,\dots,\gamma_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9f3425a02169d7ab20d1ab2d696e748_l3.png "Rendered by QuickLaTeX.com") and ![\gamma^*_1,\dots,\gamma_K^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9f3da92003da35b980d7b008fedbf5e2_l3.png "Rendered by QuickLaTeX.com"), respectively, may be structurally very different from each other. As an example consider continuous periodic functions with period length equal to 1, and assume that in each period every curve just possesses one local maximum and one minimum. Registration is driven by the succession of local extrema (shape features) in each of the functions ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com"). For any continuous function ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com") one can determine locations ![0<\tau^x_1<\tau^x_2<\dots< \tau^x_{q(x)}<1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-235777c7ac15815836360a3d93c3bbc3_l3.png "Rendered by QuickLaTeX.com") and heights ![x(\tau^x_1),\dots,x(\tau^x_{q(x)})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c3d75c10dde70d43678a0a077da3f5b1_l3.png "Rendered by QuickLaTeX.com") of all isolated local extrema in the interior of ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com"). This means that for all ![j=1,\dots,q(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e52efe944aaf72a7178bc1f53e53f5b1_l3.png "Rendered by QuickLaTeX.com") there exists an open neighborhood ![U(\tau^x_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d5ecd72f156d52801a897951e8c2fc84_l3.png "Rendered by QuickLaTeX.com") of ![\tau^x_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dde08832efa39ccf3b9d07c115bf052f_l3.png "Rendered by QuickLaTeX.com") such that either ![x(t)\geq x(\tau^x_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e5bedf13d64fd3a229cb4254500b7644_l3.png "Rendered by QuickLaTeX.com") for all ![t\in U(\tau^x_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-93d8f754ca17ee25eba22d3bce63a2a2_l3.png "Rendered by QuickLaTeX.com") or ![x(t)\leq x(\tau^x_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-06e91550b562906d0063993be4cc26b4_l3.png "Rendered by QuickLaTeX.com") for all ![t\in U(\tau^x_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-93d8f754ca17ee25eba22d3bce63a2a2_l3.png "Rendered by QuickLaTeX.com"). If ![q(x)<\infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5edc0448810c51b266c1179f460d6a24_l3.png "Rendered by QuickLaTeX.com") let ![p(x)=q(x)+2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-07120d7d6b3529b2f18340a934a95b84_l3.png "Rendered by QuickLaTeX.com"), and let ![P(x)=(x(0),x(\tau^x_1),\dots,x(\tau^x_{q(x)}),x(1))^T\in\mathbb{R}^{p(x)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ac68fc8310754cc27b1340f1c8932a35_l3.png "Rendered by QuickLaTeX.com") denote the corresponding ![p(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-281d25eadace5f1ac42638e934e3eff1_l3.png "Rendered by QuickLaTeX.com")-dimensional vector of heights of local extrema (including starting and end points). When analyzing such functions ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") on the interval ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com"), periodicity just means that ![x_i(0)=x_i(1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43724dac4331034bc1ea88c835ec9c4c_l3.png "Rendered by QuickLaTeX.com"), ![i=1,\dots,n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-54e678223c7fb91ffd9b5e77cc1d1e6b_l3.png "Rendered by QuickLaTeX.com"). If each of the curves just has one maximum and one minimum, then ![p(x_1)=\dots=p(x_n)=4](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c4ed89e7dd20c39aa09adb125cddc214_l3.png "Rendered by QuickLaTeX.com"), and by ![x_i(0)=x_i(1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43724dac4331034bc1ea88c835ec9c4c_l3.png "Rendered by QuickLaTeX.com"). It is indeed simple to construct a 3 dimensional space ![{\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-24778e6171be8fc25089203670d3aef4_l3.png "Rendered by QuickLaTeX.com") analytically. For example, let ![\gamma_1(t)\equiv 1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-de29cccb3fdf0ee2fd02864a76c56a2b_l3.png "Rendered by QuickLaTeX.com"), ![\gamma_2(t)=\sin(2\pi t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c5853558b6ccfb0450132f2b80bc1f92_l3.png "Rendered by QuickLaTeX.com"), ![\gamma_3(t)=\cos(2\pi t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8e12b6c030a69e4bd5537bcdea865c5d_l3.png "Rendered by QuickLaTeX.com"), and ![{\cal L}_3:=span\{ \gamma_1,\gamma_2,\gamma_3\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-67d15dcb52bdf57e19ead9da3d87a7b0_l3.png "Rendered by QuickLaTeX.com"). Quite obviously, for any ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") there exists a unique element ![y_i\in {\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d753735e942cf37d0f7c7b7e3ed5a38b_l3.png "Rendered by QuickLaTeX.com") with ![p(x_i)=p(y_i)=4](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-529096615032d6be6ae48de572a07e76_l3.png "Rendered by QuickLaTeX.com") and ![P(x_i)=P(y_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cd62562c2335bdf5d7506045e426a417_l3.png "Rendered by QuickLaTeX.com"). We can thus conclude that there are unique warping functions ![h_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c59cfc50326c96eff701e9f2dda48f94_l3.png "Rendered by QuickLaTeX.com") and unique coefficients ![a_{ij}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-41d4a89db3722950dc94351832a1bcd9_l3.png "Rendered by QuickLaTeX.com") such that

(3)    ![\begin{eqnarray*} y_i(t):=x_i(h_i(t)) = a_{i1}+a_{i2}\sin(2\pi t)+a_{i3}\cos(2\pi t), \quad t\in[0,1], \ i=1,\dots,n. \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-04f7223b21b47b528d2d88f75a526a06_l3.png "Rendered by QuickLaTeX.com")

Note that the functions ![y\in {\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b715259ddfa544ac5613655e84b4646_l3.png "Rendered by QuickLaTeX.com") have their local extrema at different locations, depending on ![a_{i2}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9f5193b57efcbfc80639d1e1483bbb88_l3.png "Rendered by QuickLaTeX.com") and ![a_{i3}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-977f8492312bf667961d6b80d24a3430_l3.png "Rendered by QuickLaTeX.com"). Registration to ![{\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-24778e6171be8fc25089203670d3aef4_l3.png "Rendered by QuickLaTeX.com") therefore does not lead to an alignment of shape features. But ![{\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-24778e6171be8fc25089203670d3aef4_l3.png "Rendered by QuickLaTeX.com") is not the only possible candidate space. Consider the space ![{\cal L}_3^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7b1004364957a8b0a345e1d7b37864c0_l3.png "Rendered by QuickLaTeX.com") of all polynomials ![y_{b_1,\dots,b_5}(t)=\sum_{j=1}^5 b_j t^{j-1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6fc10f0067d18182386cad8208d7feb0_l3.png "Rendered by QuickLaTeX.com") of order 5 satisfying the constraints ![y_{b_1,\dots,b_5}(0)= y_{b_1,\dots,b_5}(1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-05361a4b35e7a7873d3454160f1fd693_l3.png "Rendered by QuickLaTeX.com") as well as ![y_{b_1,\dots,b_5}'(0)= y_{b_1,\dots,b_5}'(1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-631de3b401f39818070210b974e09328_l3.png "Rendered by QuickLaTeX.com"). This is again a three dimensional space of functions with identical starting and end points, while the ![y_{b_1,\dots,b_5}'(0)= y_{b_1,\dots,b_5}'(1)\ne 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3e131e96c880fe742a3b613a7c41924b_l3.png "Rendered by QuickLaTeX.com") generates functions with one local maximum and one minimum in the interior of ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com"). There thus exists a set of warping functions ![\{h_i^*\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c027c57df9fb37553109183fccdfef04_l3.png "Rendered by QuickLaTeX.com") such that ![x_i\circ h_i^*\in {\cal L}_3^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b37a257cf0b09cf393685dbb15d5c06_l3.png "Rendered by QuickLaTeX.com"). The two spaces ![{\cal L}_3^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7b1004364957a8b0a345e1d7b37864c0_l3.png "Rendered by QuickLaTeX.com") and ![{\cal L}_3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-24778e6171be8fc25089203670d3aef4_l3.png "Rendered by QuickLaTeX.com") are not identical. As a matter of fact one can construct arbitrary many candidate spaces ![{\cal L}_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e04a74de688fa466206a992c808b4494_l3.png "Rendered by QuickLaTeX.com") by pre-chosen an arbitrary set of basis functions ![\gamma_1,\dots,\gamma_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9f3425a02169d7ab20d1ab2d696e748_l3.png "Rendered by QuickLaTeX.com") as long as there exists a ![\gamma\in \Lcal_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a6045d3e675167dfc83b35a7a3f1f946_l3.png "Rendered by QuickLaTeX.com") with ![Q(\gamma)=Q(x_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b173ab51db2b743c8f506ae0cbead776_l3.png "Rendered by QuickLaTeX.com"). A central question which space ![{\cal L}_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e04a74de688fa466206a992c808b4494_l3.png "Rendered by QuickLaTeX.com") can be considered as the “best”. [[10](#paperkey_37)] answered this question by selecting the linear subspace where the least amount of warping is necessary.

[![](https://www.thebigdatablog.com/wp-content/uploads/2019/04/k2curves-1024x594.jpg)](https://www.thebigdatablog.com/wp-content/uploads/2019/04/k2curves-scaled.jpg)

**Figure 3:** The curves shown in the left picture are registered using K=2 (middle figure) and K=1 (right figure). The bottom left figure shows the eigenvalues of the covariance operator while the middle and right figure shows the corresponding warping functions for the K=2 registration and the K=1 registration respectively.

### References

[1] F. L. Bookstein, Morphometric tools for landmark data: geometry and biology, Cambridge university press, 1997. \
 [[Bibtex]](javascript:void(0))

```
@book{bookstein1997morphometric,
title={Morphometric Tools for Landmark Data: Geometry and Biology},
author={Bookstein, F.L.},
isbn={9780521585989},
lccn={lc91039063},
series={Geometry and Biology},
url={http://books.google.co.in/books?id=amwT1ddIDwAC},
year={1997},
publisher={Cambridge University Press}
}
```

[2] F. L. Bookstein, The measurement of biological shape and shape change, Springer, 1978. \
 [[Bibtex]](javascript:void(0))

```
@book{bookstein1998,
AUTHOR = "Bookstein, F.L.",
TITLE = "The Measurement of Biological Shape and Shape Change",
PUBLISHER = "Springer",
YEAR = "1978",
BIBSOURCE = "http://www.visionbib.com/bibliography/describe448.html#TT52072"}
```

[3] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1214/aos/1176348769 "View document in publisher site") A. Kneip and T. Gasser, “Statistical tools to analyze data representing a sample of curves,” The annals of statistics, vol. 20, iss. 3, p. 1266–1305, 1992. \
 [[Bibtex]](javascript:void(0))

```
@article{kneip1992,
ajournal = "Ann. Statist.",
author = "Kneip, Alois and Gasser, Theo",
doi = "10.1214/aos/1176348769",
journal = "The Annals of Statistics",
month = "09",
number = "3",
pages = "1266--1305",
publisher = "The Institute of Mathematical Statistics",
title = "Statistical Tools to Analyze Data Representing a Sample of Curves",
url = "http://dx.doi.org/10.1214/aos/1176348769",
volume = "20",
year = "1992"
}
```

[4] T. Gasser and A. Kneip, “Searching for structure in curve sample,” Journal of the american statistical association, vol. 90, iss. 432, pp. 1179-1188, 1995. \
 [[Bibtex]](javascript:void(0))

```
@article{gasser:95,
ISSN = {01621459},
URL = {http://www.jstor.org/stable/2291510},
abstract = {The shape of a regression curve can to a large extent be characterized by the succession of structural features like extrema, inflection points, and so on. When analyzing a sample of regression curves, it is often important to know at an early stage of data analysis which structural features are occurring consistently in each curve of the sample. Such a definition is usually not easy due to substantial interindividual variation both in the x and the y axis and due to the influence of noise. A method is proposed for identifying typical features without relying on an a priori specified functional model for the curves. The approach is based on the frequencies of occurrence of structural features, as, for example, maxima in the curve sample along the x axis. Important tools are nonparametric regression and differentiation and kernel density estimation. Apart from a theoretical foundation, the usefulness of the method is documented by application to two interesting biomedical areas: growth and development, and neurophysiology.},
author = {Gasser, Theo and Kneip, Alois },
journal = {Journal of the American Statistical Association},
number = {432},
pages = {1179-1188},
publisher = {Taylor & Francis, Ltd.},
title = {Searching for Structure in Curve Sample},
volume = {90},
year = {1995}
}
```

[5] H. Sakoe and S. Chiba, “Dynamic programming algorithm optimization for spoken word recognition,” Acoustics, speech and signal processing, ieee transactions on, vol. 26, iss. 1, p. 43–49, 1978. \
 [[Bibtex]](javascript:void(0))

```
@article{sakoe1978,
abstract = {This paper reports on an optimum dynamic progxamming (DP) based time-normalization algorithm for spoken word recognition. First, a general principle of time-normalization is given using time-warping function. Then, two time-normalized distance definitions, called symmetric and asymmetric forms, are derived from the principle. These two forms are compared with each other through theoretical discussions and experimental studies. The symmetric form algorithm superiority is established. A new technique, called slope constraint, is successfully introduced, in which the warping function slope is restricted so as to improve discrimination between words in different categories. The effective slope constraint characteristic is qualitatively analyzed, and the optimum slope constraint condition is determined through experiments. The optimized algorithm is then extensively subjected to experimental comparison with various DP-algorithms, previously applied to spoken word recognition by different research groups. The experiment shows that the present algorithm gives no more than about two-thirds errors, even compared to the best conventional algorithm.},
author = {Sakoe, H. and Chiba, S. },
booktitle = {Acoustics, Speech and Signal Processing, IEEE Transactions on},
citeulike-article-id = {3496861},
journal = {Acoustics, Speech and Signal Processing, IEEE Transactions on},
keywords = {dtw, litreview, thesis},
number = {1},
pages = {43--49},
posted-at = {2008-11-08 22:11:03},
priority = {0},
title = {Dynamic programming algorithm optimization for spoken word recognition},
url = {http://ieeexplore.ieee.org/xpls/abs\_all.jsp?arnumber=1163055},
volume = {26},
year = {1978}
}
```

[6] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1111/1467-9868.00129 "View document in publisher site") J. O. Ramsay and X. Li, “Curve registration,” Journal of the royal statistical society: series b (statistical methodology), vol. 60, iss. 2, p. 351–363, 1998. \
 [[Bibtex]](javascript:void(0))

```
@article {Ramsay19982,
author = {Ramsay, J. O. and Li, Xiaochun},
title = {Curve registration},
journal = {Journal of the Royal Statistical Society: Series B (Statistical Methodology)},
volume = {60},
number = {2},
publisher = {Blackwell Publishers Ltd.},
issn = {1467-9868},
url = {http://dx.doi.org/10.1111/1467-9868.00129},
doi = {10.1111/1467-9868.00129},
pages = {351--363},
keywords = {Dynamic time warping, Geometric Brownian motion, Monotone functions, Spline, Stochastic time, Time warping},
year = {1998},
}
```

[7] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1111/1467-9868.00130 "View document in publisher site") J. O. Ramsay, “Estimating smooth monotone functions,” Journal of the royal statistical society: series b (statistical methodology), vol. 60, iss. 2, p. 365–375, 1998. \
 [[Bibtex]](javascript:void(0))

```
@article {Ramsay1998,
author = {Ramsay, J. O.},
title = {Estimating smooth monotone functions},
journal = {Journal of the Royal Statistical Society: Series B (Statistical Methodology)},
volume = {60},
number = {2},
publisher = {Blackwell Publishers Ltd.},
issn = {1467-9868},
url = {http://dx.doi.org/10.1111/1467-9868.00130},
doi = {10.1111/1467-9868.00130},
pages = {365--375},
keywords = {Convex functions, Density estimation, Generalized additive model, Linear differential equation, Monotonicity, Nonparametric regression, Regression spline, Spline smoothing},
year = {1998},
}
```

[8] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.2307/3315251.n "View document in publisher site") A. Kneip, X. Li, K. B. MacGibbon, and J. O. Ramsay, “Curve registration by local regression,” Canadian journal of statistics, vol. 28, iss. 1, p. 19–29, 2000. \
 [[Bibtex]](javascript:void(0))

```
@article{KneipGib2000,
abstract = {{Functional data analysis involves the extension of familiar statistical procedures such as principal-components analysis, linear modelling and canonical correlation analysis to data where the raw observation is a function x, (t). An essential preliminary to a functional data analysis is often the registration or alignment of salient curve features by suitable monotone transformations hi(t). In effect, this conceptualizes variation among functions as being composed of two aspects: phase and amplitude. Registration aims to remove phase variation as a preliminary to statistical analyses of amplitude variation. A local nonlinear regression technique is described for identifying the smooth monotone transformations hi, and is illustrated by analyses of simulated and actual data.}},
address = {Facult\'{e} des sciences \'{e}conomiqu.es, sociales etpolitiques Universit\'{e} catholique de Louvain, Place Montesquieu 4 B-1348 Louvain-la-Neuve, Belgium; no e-mail address available 700 North Alabama Street, Indianapolis, IN 46204, USA; D\'{e}p. de math\'{e}matiques, Universit\'{e} du Qu\'{e}bec \`{a} Montr\'{e}al C. P. 8888 Succursale centre-ville, Montr\'{e}al (Quebec), Canada H3C 3P8; Dept. of Psychology, McGill University 1205 avenue Docteur-Penfield, Montreal (Quebec), Canada H3A 1B1},
author = {Kneip, A. and Li, X. and MacGibbon, K. B. and Ramsay, J. O.},
citeulike-article-id = {6101184},
citeulike-linkout-0 = {http://dx.doi.org/10.2307/3315251.n},
citeulike-linkout-1 = {http://www3.interscience.wiley.com/cgi-bin/abstract/122439952/ABSTRACT},
doi = {10.2307/3315251.n},
issn = {1708-945X},
journal = {Canadian Journal of Statistics},
keywords = {alignment},
number = {1},
pages = {19--29},
posted-at = {2009-11-12 12:34:54},
priority = {2},
title = {{Curve registration by local regression}},
url = {http://dx.doi.org/10.2307/3315251.n},
volume = {28},
year = {2000}
}
```

[9] A. Kneip and J. O. Ramsay, “Combining registration and fitting for functional models,” Journal of the american statistical association, vol. 103, iss. 483, pp. 1155-1165, 2008. \
 [[Bibtex]](javascript:void(0))

```
@ARTICLE{Kneip2008,
title = {Combining Registration and Fitting for Functional Models},
author = {Kneip, Alois and Ramsay, James O},
year = {2008},
journal = {Journal of the American Statistical Association},
volume = {103},
number = {483},
pages = {1155-1165},
url = {http://EconPapers.repec.org/RePEc:bes:jnlasa:v:103:i:483:y:2008:p:1155-1165}
}
```

[10] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/https://doi.org/10.1016/j.csda.2019.03.004 "View document in publisher site") H. Wagner and A. Kneip, “Nonparametric registration to low-dimensional function spaces,” Computational statistics & data analysis, 2019. \
 [[Bibtex]](javascript:void(0))

```
@article{WAGNER2019,
title = "Nonparametric registration to low-dimensional function spaces",
journal = "Computational Statistics & Data Analysis",
year = "2019",
issn = "0167-9473",
doi = "https://doi.org/10.1016/j.csda.2019.03.004",
url = "http://www.sciencedirect.com/science/article/pii/S0167947319300714",
author = "Heiko Wagner and Alois Kneip",
keywords = "Amplitude variation, Genes, Dimension reduction, Functional data analysis, Functional principal components, Low dimensional linear function spaces, Phase variation, Registration, Time warping",
abstract = "Registration aims to decompose amplitude and phase variation of samples of curves. Phase variation is captured by warping functions which monotonically transform the domains. Resulting registered curves should then only exhibit amplitude variation. Most existing methods assume that all sample functions exhibit a typical sequence of shape features like peaks or valleys, and registration focuses on aligning these features. A more general perspective is adopted which goes beyond feature alignment. A registration method is introduced where warping functions are defined in such a way that the resulting registered curves span a low dimensional linear function space. The approach may be used as a tool for analyzing any type of functional data satisfying a structural regularity condition called bounded shape variation. Problems of identifiability are discussed in detail, and connections to established registration procedures are analyzed. The method is applied to real and simulated data."
}
```