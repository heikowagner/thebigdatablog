---
categories:
- All Articles
- Coding
- Python
date: '2020-10-10'
slug: kernel-regression-using-the-fast-fourier-transform
status: publish
tags: []
title: Kernel Regression using the Fast Fourier Transform
wp_id: 2340
wp_modified: '2025-03-08T13:28:39'
---

## 1. Setup

In a previous [post](https://www.thebigdatablog.com/fast-kernel-density-estimation-using-the-fast-fourier-transform/) it was shown how to speed up the computation of a kernel density using the [Fast Fourier Transform](https://www.thebigdatablog.com/fourier-transform/). Conceptually a kernel density is not that far away from kernel regression, accordingly this post is will cover using the FFT to improve the computation of a [kernel regression](https://www.thebigdatablog.com/kernel-regression-using-pyspark/). A popular estimator for the regression function ![E(X|Y)=m(X)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-33a22464ec1905f6194853e184839d0f_l3.png "Rendered by QuickLaTeX.com") given observed points ![(x_1, y_1),…,(x_T, y_T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-df2728e685cb18f5ba4032dff711af75_l3.png "Rendered by QuickLaTeX.com") is the Nadaraya–Watson estimator with [kernel function](https://www.thebigdatablog.com/nonparametric-density-estimation-using-spark/) ![K()](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cb9686009c7d11bbb1604ead2b4bd238_l3.png "Rendered by QuickLaTeX.com") and bandwidth ![h](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-14b463d0ecd5b350ced6cf1d6a12eef3_l3.png "Rendered by QuickLaTeX.com"):

(1)    ![\begin{equation*}\widehat {m}}_{h}(x)={\frac {\sum _{i=1}^{T}K_{h}(x-x_{i})y_{i}}{\sum _{j=1}^{T}K_{h}(x-x_{j})}}.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-52c20a621107301a09c23e2b486fe29b_l3.png "Rendered by QuickLaTeX.com")

The FFT requires a grid of with ![T^{'}=2^{k}, k \in \mathbb{N}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b25cdcffcc35b1d92e33761232a9d65_l3.png "Rendered by QuickLaTeX.com") design points. A meaningful choice in terms of asymptotic is ![k=\left \lceil{\frac{log(T)}{log(2)}}\right \rceil](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b7abb99e6ea6e9914cb8be960f2afb66_l3.png "Rendered by QuickLaTeX.com") . Then ![lim_{T\rightarrow \infty} \frac{2^k}{T} =1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-525c5669b49dd1afb58d6ab7e355250e_l3.png "Rendered by QuickLaTeX.com") which means that ![T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9ed275b0bf1633b7ee83b78fcc28273_l3.png "Rendered by QuickLaTeX.com") and ![T'](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd174da18862f6abe6800264db6390df_l3.png "Rendered by QuickLaTeX.com") are asymptotically equivalent. In a first step we have to interpolate ![y=(y_1,\dots,y_T), x=(x_1,\dots,x_T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3868e8105f808e18dd80fd94e6f54790_l3.png "Rendered by QuickLaTeX.com") to fit to an equidistant grid with ![T^'](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e05b6c31052146f6d3a44f52461d5be9_l3.png "Rendered by QuickLaTeX.com") points with

(2)    ![\begin{equation*}y^I=y_{a}+\left(y_{b}-y_{a}\right){\frac {x^I-x_{a}}{x_{b}-x_{a}}}{\text{ at the point }}\left(x^I,y^I\right)} .\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1cd102c1a7d744c5376a08f336c24e7f_l3.png "Rendered by QuickLaTeX.com")

Since we use an interpolation using an equidistant grid ![x^I=(x^I_1, \dots x^I_{T'})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c562239970bdd04dd3516b6c845a1b3_l3.png "Rendered by QuickLaTeX.com") ([1](#id1833639671)) becomes

(3)    ![\begin{equation*}\widehat {m}}^I_{h}(x)= \frac{max(x^I)-min(x^I)}{T^{'}} \sum _{i=1}^{T^{'}}K_{h}(x-x^I_{i})y^I_{i}} .\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-52bdb99a3644ee190b804d24653741a5_l3.png "Rendered by QuickLaTeX.com")

Let the discrete Fourier transform of ![\hat{m}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0ee796efdb7809c2a987cbeed52bf3f7_l3.png "Rendered by QuickLaTeX.com") be denoted by ![\tilde{m}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-90e33384f15325e5500c36b3b74530ee_l3.png "Rendered by QuickLaTeX.com"). The Fourier transform of ([3](#id2796547723)) for ![s \in (x^I_1, \dots x^I_{T'})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8866c8ad7f9ebd37184ffe8df8952cf5_l3.png "Rendered by QuickLaTeX.com") is then using convolution and translation given by\

(4)    ![\begin{equation*}\tilde{m}_h(s)= \frac{max(x^I)-min(x^I)}{T^{'}} \sum_{i=1}^{T^{'}} \tilde{K}_{h}(s) y^I_{i} e^{i s x^I_{i}}=\frac{max(x^I)-min(x^I)}{T^{'}}  \tilde{K}_{h}(s) \tilde{y}(s)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a8d4cc0833dc4016efc2f7564a9e8503_l3.png "Rendered by QuickLaTeX.com")

\
where ![\tilde{y}(s)= \frac{1}{T^{'}} \sum_{i=1}^{T^{'}} y^I_{i} e^{i s x^I_{i}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-09c48d652bee4b77dea17378c0a72236_l3.png "Rendered by QuickLaTeX.com") is the Fast Fourier transform of the interpolated data. ![\hat{m}^I](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-323627c70c1a51af5f7e07d6b4192674_l3.png "Rendered by QuickLaTeX.com") can then be obtained by applying the inverse DFFT to ([4](#id142768606)). All these steps then involve only ![\mathcal{O}(T' log(T') )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9acfb1e544de5f67e6626d0b1a2d053a_l3.png "Rendered by QuickLaTeX.com") operations instead of ![\mathcal{O}(T'T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fb2b9f6d4ebccfa746f171c6fc1b28e5_l3.png "Rendered by QuickLaTeX.com") operations when computing ([3](#id2796547723)) directly. Sorting, which may be required prior to the linear interpolation has a computational complexity of ![\mathcal{O}(T log(T) )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dbb03880aac6154651a39f559c02b800_l3.png "Rendered by QuickLaTeX.com") which has the same order of magnitude than estimating the FFT based estimator itself and thus does not impact the computational complexity.

## 2. Asymptotic Considerations

An important question is if the interpolation decline the asymptotic properties of the estimator. Another way to describe the regression setup is for ![T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9ed275b0bf1633b7ee83b78fcc28273_l3.png "Rendered by QuickLaTeX.com") design points ![x_1,\dots,x_T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b8cdd7a5a1b0ae4909f3026c223ff195_l3.png "Rendered by QuickLaTeX.com") in addition wlog for simplicity we require ![x_i \in [0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-34484407678f3ca35df58c402e1d4094_l3.png "Rendered by QuickLaTeX.com") there are noisy observations ![y_{l}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-75f10a10fef752344861c415fe6a85e4_l3.png "Rendered by QuickLaTeX.com") such that\

(5)    ![\begin{eqnarray*}y_{l}=m(x_l)+\epsilon_{l},\quad l=1,\dots,T,\end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-21d80394ea492697d0e42249c83446ef_l3.png "Rendered by QuickLaTeX.com")

\
for i.i.d. zero mean error terms ![\epsilon_{l}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9fd0301934bd0ab874bb444829414f38_l3.png "Rendered by QuickLaTeX.com") with finite variance ![\sigma^2>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-585f9c79e70290d07d0e051dd939fb6e_l3.png "Rendered by QuickLaTeX.com") and ![E(\epsilon_{l}^4)<\infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a1195465fbfde42c3d2ccf178140877c_l3.png "Rendered by QuickLaTeX.com"). Following [[1](#paperkey_23)], the Nadaraya–Watson estimator for an interior point ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com") we got a mean squared error of

     ![\[\operatorname {E} (({m}(x)-{\hat {m}}(x))^2) \approx \underbrace {h^{4}B^{2}} _{={\text{Bias}}^{2}}+\underbrace {{\frac {1}{Th}}V}_{={\text{Variance}}}}\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-722d9402d4022dd5ae2ae46595a1b567_l3.png "Rendered by QuickLaTeX.com")

while using a simple taylor extension, for neigbour points ![x_a,x_b](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-edf20fa94cd3892c6593ac1d1ced7492_l3.png "Rendered by QuickLaTeX.com") the error introduced by the interpolation is given by

     ![\[\operatorname {E} (|m^I(x)-m(x)|)\leq \operatorname {E} (C(x_{b}-x_{a})^{2}) = \mathcal{O}_p( T^{-2} )\quad {\text{where}}\quad C={\frac {1}{8}}\max _{r\in [x_{a},x_{b}]}|m''(r)|.}\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-33f18fc556f93665a069716e9e1afff7_l3.png "Rendered by QuickLaTeX.com")

Putting all together and using an appropriate bandwidth of order ![h^*= \mathcal{O}(T^{-1/5})=\mathcal{O}(T'^{-1/5})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9f184f3014a79fc5f7c71b96051e7a74_l3.png "Rendered by QuickLaTeX.com")

     ![\[\operatorname {E} ((m(x)-{\hat {m}^I}(x))^2)=\operatorname {E} ((\underbrace {m(x)-m^I(x)}_{\text{interpolation error}}+\underbrace {m^I(x)-{\hat {m}^I}(x)}_{\text{estimation error}} )^2) \]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5249c5f145cda6a70d21d53884cc86c6_l3.png "Rendered by QuickLaTeX.com")

using some straightforward calculations one can show that the interpolating error is dominated by the kernel regression error. A detailed proof and a extension allowing for multivariate ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") can be found in [[2](#paperkey_24)].

## 3. Python Code

To implement the method the fft function that comes with the numpy package was chosen. The numpy fft() function will return the approximation of the DFT from 0 to ![\pi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-26d6788550ffd50fe94542bb3e8ee615_l3.png "Rendered by QuickLaTeX.com"). Therefore fftshift() is needed to swap the output vector of the fft() right down the middle. So the output of fftshift(fft()) is then from ![-\pi/2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4a12d16db2ce3086d4772f6e2e52122c_l3.png "Rendered by QuickLaTeX.com") to ![\pi/2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c658187c700e99a5a8e304c146ee4f85_l3.png "Rendered by QuickLaTeX.com").

```
import numpy as np
import matplotlib.pyplot as plt
import timeit
from scipy.interpolate import interp1d

# Simulation
T = 500
X = np.linspace(-5, 5, T) 
Y= (X)**3 + np.random.normal(-0, 10, T)
plt.scatter(X, Y, c="blue")

plt.xlabel('sample')
plt.ylabel('X')

# Presetting
Tout = int( 2 ** np.floor(np.log(T)/np.log(2)) )
print(Tout)

# Interpolate Y
f = interp1d(X, Y)
grid = np.linspace(-5, 5, num=Tout)
Ynew=f(grid)

def epan_kernel(u, b):
    u = u / b
    return max(0, 1. / b * 3. / 4 * (1 - u ** 2))


# Estimation using FFT
start = timeit.default_timer()

t = grid
h= Tout**(-1/5)
kernel = [epan_kernel(x, h) for x in t]
kernel_ft = np.fft.fft(kernel)
func_tmp = kernel_ft.flatten() * np.fft.fft(Ynew)
m_fft = (max(X)-min(X))*np.fft.fftshift(np.fft.ifft(func_tmp).real)/Tout
plt.plot(t, m_fft)

stop = timeit.default_timer()
print('Time: ', stop - start)

plt.show()
```

### References

[1] {. Fan and {. Gijbels, Local polynomial modelling and its applications, London [u.a.]: Chapman & hall, 1996. \
 [[Bibtex]](javascript:void(0))

```
@book{Fan1996,
added-at = {2009-08-21T10:31:17.000+0200},
address = {London [u.a.]},
author = {Fan, {Jianqing} and Gijbels, {Irène}},
biburl = {http://www.bibsonomy.org/bibtex/23e163e04b09550b54a8067f0cbd97b7e/fbw_hannover},
interhash = {de68bea35adadb13da464f65107efce4},
intrahash = {3e163e04b09550b54a8067f0cbd97b7e},
isbn = {0412983214},
keywords = {Equations Mathematische_Statistik Polynomials Regression_analysis},
number = 66,
pagetotal = {XV, 341},
ppn_gvk = {19282144X},
publisher = {Chapman \& Hall},
series = {Monographs on statistics and applied probability series},
timestamp = {2009-08-21T10:31:17.000+0200},
title = {Local polynomial modelling and its applications},
url = {http://gso.gbv.de/DB=2.1/CMD?ACT=SRCHA&SRT=YOP&IKT=1016&TRM=ppn+19282144X&sourceid=fbw_bibsonomy},
year = 1996
}
```

[2] M. P. Wand, “Fast computation of multivariate kernel estimators,” Journal of computational and graphical statistics, vol. 3, iss. 4, p. 433–445, 1994. \
 [[Bibtex]](javascript:void(0))

```
@article{Wand1994,
ISSN = {10618600},
URL = {http://www.jstor.org/stable/1390904},
abstract = {Multivariate extensions of binning techniques for fast computation of kernel estimators are described and examined. Several questions arising from this multivariate extension are addressed. The choice of binning rule is discussed, and it is demonstrated that linear binning leads to substantial accuracy improvements over simple binning. An investigation into the most appropriate means of computing the multivariate discrete convolutions required for binned kernel estimators is also given. The results of an empirical study indicate that, in multivariate settings, the fast Fourier transform offers considerable time savings compared to direct calculation of convolutions.},
author = {M. P. Wand},
journal = {Journal of Computational and Graphical Statistics},
number = {4},
pages = {433--445},
publisher = {[American Statistical Association, Taylor & Francis, Ltd., Institute of Mathematical Statistics, Interface Foundation of America]},
title = {Fast Computation of Multivariate Kernel Estimators},
volume = {3},
year = {1994}
}
```