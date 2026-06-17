---
categories:
- All Articles
date: '2022-04-15'
slug: estimating-the-extrema-of-noisy-curves-and-optimization-using-spline-surface-approximation
status: publish
tags: []
title: Estimating the extrema of noisy curves and optimization using spline surface
  approximation
wp_id: 3145
wp_modified: '2023-10-01T10:19:23'
---

Estimating **maxima** and **minima** of a noisy curve turns out to be very hard and to a large part is still an open question. In this blog post we will discover some strategies to encounter the problem. Another interpretation is given in the context of optimization. Consider an optimization problem where the (smooth) objective function is only evaluated at some, maybe random and noisy, points or due to computational issues can only be sparsely evaluated. Then this algorithm will give a fast estimate of the optimal values.

## 1. Estimation based on Splines

We assume that a smooth at least two times differentiable curve ![X(t) \in \mathbb{R}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a52988369739657f205fe9decc7349ad_l3.png "Rendered by QuickLaTeX.com") is observed at independent randomly-distributed points ![t_{k} \in [0,1], \; k=1,\dots, T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7030b3d1e4772481ee5bd55542ed687e_l3.png "Rendered by QuickLaTeX.com") contaminated with additional noise. Our model is then given by\

(1)    ![\begin{equation*} Y(t_{k})=X(t_{k}) + \epsilon_{k}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9ce5379d27abf2761ae2055eb0912dcf_l3.png "Rendered by QuickLaTeX.com")

\
where ![\epsilon_{k}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6a73ce66b01132aee7db6cf26a6969f2_l3.png "Rendered by QuickLaTeX.com") are i.i.d. random variables with ![\mathbf{E}\left[\varepsilon_{k}|X\right]=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a129ee5e69b947d55c08ed620548b922_l3.png "Rendered by QuickLaTeX.com"), ![Var\left(\epsilon_{k}|X\right)= \sigma^2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0b0a93c15ad7036522724f03765bd1e4_l3.png "Rendered by QuickLaTeX.com") and ![\epsilon_{k}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6a73ce66b01132aee7db6cf26a6969f2_l3.png "Rendered by QuickLaTeX.com") is independent of ![X= X(t_1),\dots, X(t_k)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5dc4eb816214633778f1afa63edeb356_l3.png "Rendered by QuickLaTeX.com"). Our goal is to determine all ![t_0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4f748b339328872e9bd17f31810a92d_l3.png "Rendered by QuickLaTeX.com") such that the derivative \

(2)    ![\begin{equation*} \frac{\partial X(t)}{\partial t}(t_0)=0 \text{ and } \frac{\partial X(t)}{\partial t^2}(t_0) \neq 0.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d21bdd3521dd64f5433bc252602debb2_l3.png "Rendered by QuickLaTeX.com")

### 1.1 Natural cubic splines

Consider the following minimization problem, among all functions with two continuous derivatives find ![f \in C^{2}( [0,1] )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fe5789b6d06785d52224d9d095a6f009_l3.png "Rendered by QuickLaTeX.com") such that

(3)    ![\begin{equation*} \sum_{i=1}^T \{ Y_i - m(t_i) \}^2 + \lambda \int\{m^{''}(t) \}^2 dt\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3dcefa12d0c489725ee50defe410e601_l3.png "Rendered by QuickLaTeX.com")

is minimized. where ![\lambda](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b5c45836864531b8e37025dabadd24a_l3.png "Rendered by QuickLaTeX.com") is a fixed smoothing parameter and ![Y_i := Y(t_{i})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d8988797257e6457fe32a01666820e23_l3.png "Rendered by QuickLaTeX.com"). It can be shown [[1](#paperkey_15)], that ([3](#id1619897285)) has an unique minimizer which is a particular natural cubic spline. More generally a natural cubic spline with knots ![\zeta_1<\dots<\zeta_K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-29104320cbfbad18c2bfaaaf145d8820_l3.png "Rendered by QuickLaTeX.com") is a piecewise polynomial of order 4, with additional constrains such that the the function is linear beyond the boundary knots, represented with ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") Basis functions ![N_1(t),\dots, N_K(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dffbdae0b0ee3ef52458b7e212a01d23_l3.png "Rendered by QuickLaTeX.com"). When the knots are given by ![\zeta_i=t_i, i=1,\dots,T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e22c876fc048a07013a7b7380de303a7_l3.png "Rendered by QuickLaTeX.com") the natural cubic spines solves ([3](#id1619897285)) in that case an optimal solution for [3](#id1619897285) is given by ![m(t)=\sum_{j=1}^T N_j(t) \theta_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6164f20e9bc80a59f4fd803f2ec5fe69_l3.png "Rendered by QuickLaTeX.com").

Let

     ![\begin{equation*} \textbf{N}= \begin{bmatrix} N_1(t_1)& N_2(t_1) &\dots & N_K(t_1)\\ N_1(t_2)& N_2(t_2) & \dots & N_K(t_2)\\ \vdots & \vdots & \ddots & \vdots \\ N_1(t_T)& N_2(t_T) & \dots & N_K(t_T)\\ \end{bmatrix}, \Omega= \begin{bmatrix} \int N^{''}_1(t)N^{''}_1(t)dt &\dots & \int N^{''}_K(t)N^{''}_1(t)dt\\ \int N^{''}_1(t)N^{''}_2(t)dt & \dots & \int N^{''}_K(t)N^{''}_2(t)dt\\ \vdots & \ddots & \vdots \\ \int N^{''}_1(t)N^{''}_K(t)dt & \dots & \int N^{''}_K(t)N^{''}_K(t)dt\\ \end{bmatrix}  \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-be4a88f7df01479b5a94ce14cff0ff25_l3.png "Rendered by QuickLaTeX.com")

the solution to the minimization problem using ![\textbf{Y}=(Y_1,\dots,Y_T)^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f15cdac5eb56d61dd6e90f0d5cfeed32_l3.png "Rendered by QuickLaTeX.com") is thus given by

(4)    ![\begin{equation*} \hat{\theta}}= (\textbf{N}^T \textbf{N} +T \lambda \Omega)^{-1} \textbf{N}^T \textbf{Y} \mathop{=}\limits^{\text{#def}} \textbf{K} \textbf{Y}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9cacaa01f9e56ebf220a5c078b262eff_l3.png "Rendered by QuickLaTeX.com")

A popular basis choice is derived from the truncated power series and given by

(5)    ![\begin{equation*} N_1(t)= 1,\; N_1(t)= t,\; N_{k+2}(t)= d_k(t)-d_{K-1}(t)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-462083362b6f0e8208c106cf1578dc40_l3.png "Rendered by QuickLaTeX.com")

where

(6)    ![\begin{equation*} d_k(t) = \frac{(t-\zeta_k)^3_+ - (t-\zeta_K)^3_+}{\zeta_K-\zeta_k}.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-69616ce6b54228acae1df72eb63bb527_l3.png "Rendered by QuickLaTeX.com")

\
\
We will use this basis as illustration for our method from here on. An important inside is that for a fixed interval limited by the nodes ![t \in [\zeta_k, \zeta_{k+1}]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e6303c863d0c94281bc1fc58efb0a6fc_l3.png "Rendered by QuickLaTeX.com"), ![f(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-59d54ba73238a26eb8acae54cb83607e_l3.png "Rendered by QuickLaTeX.com") can be represented using a cubic function (see [[2](#paperkey_16)]). In particular

(7)    ![\begin{equation*}\hat{m}_k(t)=  \sum_{l=1}^{k} \frac{\theta_{l+2} }{\zeta_K - \zeta_l}  t^3 +  \sum_{l=1}^{k} \frac{- 3 \theta_{l+2} \zeta_l}{\zeta_K - \zeta_l}  t^2 +  \left( \theta_2 + \sum_{l=1}^{k} \frac{3\theta_{l+2} \zeta_l^2}{\zeta_K - \zeta_l} \right) t + \left( \theta_1 + \sum_{l=1}^{k} \frac{-\theta_{l+2} \zeta_l^3}{\zeta_K - \zeta_l} \right)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5cfb80b520789bf92747b570bbe42780_l3.png "Rendered by QuickLaTeX.com")

\

[![](https://www.thebigdatablog.com/wp-content/uploads/2022/02/plot_zoom-1024x768.png)](https://www.thebigdatablog.com/wp-content/uploads/2022/02/plot_zoom.png)

*The figure shows an example with ![X(t)=sin(10t)+t, \; -0.5\leq t \leq0.5](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-15c8e48061aa2f9cdb747824ab86e54f_l3.png "Rendered by QuickLaTeX.com") the grey dots show the observed Y while the black dots indicate the estimated extrema by the algorithm. The spline (brown curve) is estimated using K=5, the rainbow colored curves are the representation of the spline using a polynomial of order 3 between a sector delimited by two neighbor knots.*

\
Accordingly,\

(8)    ![\begin{equation*}  \hat{m} _k^{'}(t)= \underbrace{ \sum_{l=1}^{k} \frac{3 \theta_{l+2}}{\zeta_K - \zeta_l} }_{A_k} t^2 + \underbrace{ \sum_{l=1}^{k} \frac{- 6 \theta_{l+2} \zeta_l}{\zeta_K - \zeta_l} }_{B_k} t + \underbrace{ \theta_2 + \sum_{l=1}^{k} \frac{3\theta_{l+2} \zeta_l^2}{\zeta_K - \zeta_l} }_{C_k} \text{ and }  \hat{m} _k^{''}(t)= \sum_{l=1}^{k} \frac{ \theta_{l+2} ( - 6 \zeta_l + 6  t )}{ \zeta_K - \zeta_l }\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-948a6f732b45d35a7f7f812b34e60607_l3.png "Rendered by QuickLaTeX.com")

For ![B_k^2- 4 A_kC_k>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6d02e3e1d5dbea4c8d15d5afeafe95f8_l3.png "Rendered by QuickLaTeX.com"), the real possible extrema ![a_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-eb74c1c8b6fc6cb7def31be6478a4ac5_l3.png "Rendered by QuickLaTeX.com") of ![\hat{m}_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8a96d7b19705ade74098c71287e260d6_l3.png "Rendered by QuickLaTeX.com") are thus given by\

(9)    ![\begin{equation*} a_k = - \frac{B_k}{2A_k} \pm \frac{\sqrt{B_k^2- 4 A_kC_k}}{2A_k}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-52507c6b9d517dddfbe7c0d7f3af03bb_l3.png "Rendered by QuickLaTeX.com")

\
this will then be an extrema of ![\hat{m}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad8fdc193bca6bcfe73bebae2b1d7497_l3.png "Rendered by QuickLaTeX.com") if ![a_k \in [\zeta_k, \zeta_{k+1}]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e5986668ed1e76bb5c6247b3e107089c_l3.png "Rendered by QuickLaTeX.com") and ![\hat{m}^{''}(a_k) \neq 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c91773bfe1422d8d120624b24013a1ad_l3.png "Rendered by QuickLaTeX.com").

### 1.2 Estimation and Asymptotic

To estimate the extrema we replace the spline coefficients ![\theta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-356a08e839ab6974a16448e16e56745d_l3.png "Rendered by QuickLaTeX.com") by ![\hat{\theta}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d3dde62ae04424aff5b121ab818b896e_l3.png "Rendered by QuickLaTeX.com"), their estimated counterpart, as specified in ([4](#id2845888992)) to derive ![\hat{A}_k, \hat{B}_k, \hat{C}_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d95d1d8ccf26229571bd5f7ac8de10d0_l3.png "Rendered by QuickLaTeX.com") and ![\hat{a}_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4a56be557db7e8b70ff2250458d541b_l3.png "Rendered by QuickLaTeX.com") according to ([8](#id581603872)) and ([9](#id3023121662)). First verify that for fixed ![\lambda](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b5c45836864531b8e37025dabadd24a_l3.png "Rendered by QuickLaTeX.com"), ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com")\

(10)    ![\begin{equation*}E(\hat{\theta}|X)  - \theta= ((\textbf{N}^T \textbf{N} +T \lambda \Omega)^{-1} - (\textbf{N}^T \textbf{N})^{-1}) \textbf{N}^T \textbf{N} \theta\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cc55f7ed1dfe258de4bffd08d458e28d_l3.png "Rendered by QuickLaTeX.com")

\
and\

(11)    ![\begin{equation*}Var(\hat{\theta}|X) = \sigma^2 (\textbf{N}^T \textbf{N} +T \lambda \Omega)^{-1} \textbf{N}^T \textbf{N} (\textbf{N}^T \textbf{N} +T \lambda \Omega)^{-1} = \sigma^2 \textbf{K} \textbf{K}^T\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-222d2ac93cc15ae91978c7d159befcca_l3.png "Rendered by QuickLaTeX.com")

\
therefore\

(12)    ![\begin{equation*}E(\hat{A}_k|X) - A_k= \iota^A_k ( E(\hat{\theta}|X) - \theta), \; Var(\hat{A}_k|X) = \iota_k^A Var(\hat{\theta}|X) (\iota_k^A)^T\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c7cd3b210fe68c681d0689e19358d4ca_l3.png "Rendered by QuickLaTeX.com")

\

(13)    ![\begin{equation*}E(\hat{B}_k|X) - B_k= \iota^B_k( E(\hat{\theta}|X) - \theta), \; Var(\hat{B}_k|X) = \iota_k^B Var(\hat{\theta}|X) (\iota_k^B)^T\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0a1eb67dfc0d80da64972faaf3acbce2_l3.png "Rendered by QuickLaTeX.com")

\

(14)    ![\begin{equation*}E(\hat{C}_k|X) - C_k= \iota^C_k( E(\hat{\theta}|X) - \theta),\; Var(\hat{C}_k|X) = \iota_k^C Var(\hat{\theta}|X) (\iota_k^C)^T\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-51eb9d161dc7deaccf70fd86905dad12_l3.png "Rendered by QuickLaTeX.com")

\
 where ![\iota^A_k=(0,0,\frac{3}{\zeta_K - \zeta_1},\dots,\frac{3}{\zeta_K - \zeta_k}, \underbrace{\dots,0}_{K-k -2 } )^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-eb5d56cb8cdeb94ca9015bb46ffcfff5_l3.png "Rendered by QuickLaTeX.com"), ![\iota^B_k=(0,0,\frac{-6 \zeta_1}{\zeta_K - \zeta_1},\dots,\frac{-6\zeta_k}{\zeta_K - \zeta_k},  \underbrace{\dots,0}_{ K-k -2 } )^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cd4fd7efcb4baa013220419fbe6e57b4_l3.png "Rendered by QuickLaTeX.com") ,![\iota^C_k=(0,1,\frac{3 \zeta_1^2}{\zeta_K - \zeta_1},\dots,\frac{3 \zeta_k^2}{\zeta_K - \zeta_k},  \underbrace{\dots,0}_{ K-k-2 } )^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8137eac797b55c55ed8dbbcc2aac2919_l3.png "Rendered by QuickLaTeX.com").

\
After using a Taylor ([see here for example](http://www.stat.cmu.edu/~hseltman/files/ratio.pdf)) expansion and some calculus we can derive\

(15)    ![\begin{equation*} \begin{split}E(\hat{a_k}|X)= a_k +( a'_{kA_k} \iota^A_k  +   a'_{kB_k} \iota^B_k +   a'_{kC_k} \iota^C_k ) ( E(\hat{\theta}|X) - \theta) \\ +  ( a''_{kA_k A_k } \iota^A_k  +   a'_{kB_k} \iota^B_k +   a'_{kC_k} \iota^C_k )   Var(\hat{\theta}|X)  ( \iota^A_k + \iota^B_k ) + o(\frac{1}{T})\end{split}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3ea12ba6d28444e02474a66e0fcd5038_l3.png "Rendered by QuickLaTeX.com")

\
The first order Taylor expansion of the variance is given by\

(16)    ![\begin{equation*}Var(\hat{a}|X) \approx E([ ( a'_{kA_k} \iota^A_k  +   a'_{kB_k} \iota^B_k +   a'_{kC_k} \iota^C_k ) ( E(\hat{\theta}|X) - \theta) ]^2)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-57843132b8f89fa61c74894f9f61579a_l3.png "Rendered by QuickLaTeX.com")

\
where

(17)    ![\begin{equation*}a'_A= \frac{1}{2} (\frac{6AC+B^2}{\sqrt{4AC+B^2}}-B)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f796fde557a9d60242a68b5c051fd392_l3.png "Rendered by QuickLaTeX.com")

\

(18)    ![\begin{equation*}a'_B=\frac{1}{2} A (\frac{B}{\sqrt{4AC-B^2}}-1)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7ba40ebbd7befd9ee4146a4d7c7c7fc2_l3.png "Rendered by QuickLaTeX.com")

(19)    ![\begin{equation*}a'_C=\frac{A^2}{\sqrt{4AC+B^2}}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-595e7d9c698196219134aec6aba36e27_l3.png "Rendered by QuickLaTeX.com")

\

(20)    ![\begin{equation*}a^{''}_{AA}=\frac{A^2}{\sqrt{4AC+B^2}}\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-68074314947a4803e97a4cfb2f3b4e38_l3.png "Rendered by QuickLaTeX.com")

## 2. White noise representation

The white noise version, as descibed in [[3](#paperkey_17)], of ([1](#id3910124194)) is\

(21)    ![\begin{equation*}y_t=m(t) + e_t\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e120e438c57c058c41e1c4eae6597e28_l3.png "Rendered by QuickLaTeX.com")

\
where the noise term ![e_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-55fab20148ce43e79a675c0f64098330_l3.png "Rendered by QuickLaTeX.com") can be interpreted as ![n^{-1/2} v(t)^{1/2} DW(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-12daef418f69fc00a8b298888e099366_l3.png "Rendered by QuickLaTeX.com") and ![v(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bf6f3f032e9eb6084265f06791454342_l3.png "Rendered by QuickLaTeX.com") is the error variance when the design point equals ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"), and ![D W(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b429e6a9f8f70ab7c7833f0e6181f85a_l3.png "Rendered by QuickLaTeX.com") can be figuratively represented as a ‘derivative’ of standard Brownian motion, in the sense\
that ![DW(t)dt = dW(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9a657c22dadbff83c761e17892fad8fb_l3.png "Rendered by QuickLaTeX.com").

In the white noise case, the corresponding equivalent basis to is given by ![\phi(t|s)=(t-s)^3_{+}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5ff16037a689d17a3e53d2f4e0e17f85_l3.png "Rendered by QuickLaTeX.com") with the knot density ![\rho(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-522e6eb600c8cb0a208d1c2788ee7047_l3.png "Rendered by QuickLaTeX.com") then \

(22)    ![\begin{equation*}\hat{m}(t)=\sum_{k=1}^4 \theta_k t^{k-1} + \int_0^1 \theta(s) \rho(s) \phi(t|s)ds\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b5a728b9d2da17c2b3f47a5e26f37d54_l3.png "Rendered by QuickLaTeX.com")

\
\
Then the continuous analogue to ([8](#id581603872)) is given by\

(23)    ![\begin{equation*}A(s)= \int_0^s \frac{3(  \theta_3+  \theta_4 + \theta(s)\rho(s) ) } {1 - s}  ds\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2df31d1fd7c1b902c5aab9fba6d74164_l3.png "Rendered by QuickLaTeX.com")

\

(24)    ![\begin{equation*}B(s)= \int_0^s  \frac{- 6 ( \theta_3+  \theta_4 +   \theta(s)\rho(s)) s}{1 - s}  ds\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6591cd79d1495c3ab2fc670046e84618_l3.png "Rendered by QuickLaTeX.com")

\

(25)    ![\begin{equation*}C(s) = \theta_2 +  \int_0^s \frac{3 ( \theta_3+  \theta_4 +   \theta(s)\rho(s)s^2}{1 - s} ds\right\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5937ce86cf308d4b603e2e104782e4ea_l3.png "Rendered by QuickLaTeX.com")

Accordingly ![a](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5c53d6ebabdbcfa4e107550ea60b1b19_l3.png "Rendered by QuickLaTeX.com") is an extrema of ![\hat{m}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad8fdc193bca6bcfe73bebae2b1d7497_l3.png "Rendered by QuickLaTeX.com") if and only if\

(26)    ![\begin{equation*}a = - \frac{B(a)}{2A(a)} \pm \frac{\sqrt{B(a)^2- 4 A(a)C(a)}}{2A(a)} \;\text{and} \; m^{''}(a) \neq 0\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cf618d6f1f19ef924c6e006c4c3d3203_l3.png "Rendered by QuickLaTeX.com")

\
therefore an extrema is observed if ![a](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5c53d6ebabdbcfa4e107550ea60b1b19_l3.png "Rendered by QuickLaTeX.com") is a fix point.

[1] P. Craven and G. Wahba, “Smoothing noisy data with spline functions,” Numerische mathematik, vol. 31, pp. 377-403, 1978. \
 [[Bibtex]](javascript:void(0))

```
@article{Wahba1979,
title={Smoothing noisy data with spline functions},
author={Peter Craven and Grace Wahba},
journal={Numerische Mathematik},
year={1978},
volume={31},
pages={377-403}
}
```

[2] C. H. Reinsch, “Smoothing by spline functions,” Numerische mathematik, vol. 10, pp. 177-183, 1967. \
 [[Bibtex]](javascript:void(0))

```
@article{Reinsch1967,
title={Smoothing by spline functions},
author={Christian H. Reinsch},
journal={Numerische Mathematik},
year={1967},
volume={10},
pages={177-183}
}
```

[3] P. Hall and J. D. Opsomer, “Theory for penalised spline regression,” Biometrika, vol. 92, iss. 1, p. 105–118, 2005. \
 [[Bibtex]](javascript:void(0))

```
@article{Hall92,
ISSN = {00063444},
URL = {http://www.jstor.org/stable/20441169},
abstract = {Penalised spline regression is a popular new approach to smoothing, but its theoretical properties are not yet well understood. In this paper, mean squared error expressions and consistency results are derived by using a white-noise model representation for the estimator. The effect of the penalty on the bias and variance of the estimator is discussed, both for general splines and for the case of polynomial splines. The penalised spline regression estimator is shown to achieve the optimal nonparametric convergence rate established by Stone (1982).},
author = {Peter Hall and J. D. Opsomer},
journal = {Biometrika},
number = {1},
pages = {105--118},
publisher = {[Oxford University Press, Biometrika Trust]},
title = {Theory for Penalised Spline Regression},
urldate = {2022-04-16},
volume = {92},
year = {2005}
}
```