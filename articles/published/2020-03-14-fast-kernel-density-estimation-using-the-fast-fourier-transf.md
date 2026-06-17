---
categories:
- All Articles
- Coding
- Python
date: '2020-03-14'
slug: fast-kernel-density-estimation-using-the-fast-fourier-transform
status: publish
tags: []
title: Fast Kernel Density Estimation using the Fast Fourier Transform
wp_id: 2121
wp_modified: '2026-06-11T18:47:58'
---

## 1. Setup

This Post is about how to speed up the computation kernel density estimators using the [FFT (Fast Fourier Transform)](https://www.thebigdatablog.com/fourier-transform/). Let be ![X_1, \dots, X_T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dc2cdef767a56be294b568540cec2b2f_l3.png "Rendered by QuickLaTeX.com") be a random sample drawn from an unknown distribution with density ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com"). [Remember](https://www.thebigdatablog.com/kernel-based-estimators-for-multivariate-densities-and-functions/), the kernel density estimator with bandwidth ![h](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-14b463d0ecd5b350ced6cf1d6a12eef3_l3.png "Rendered by QuickLaTeX.com") is then given by\

(1)    ![\begin{equation*}\hat{f}_h(u)= \frac{1}{T} \sum_{i=1}^T K_\textbf{h}(u-X_i)\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-62dad99323f5340dd2eada84cfae12e7_l3.png "Rendered by QuickLaTeX.com")

### 1.1 Convolution Theorem

In the following we will use the notation from a [previous article](https://www.thebigdatablog.com/fourier-transform/) where the convolution theorem for the Fourier Transform was introduced. Accordingly the discrete version of the convolution theorem is given by: Let ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com") and ![g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d208fd391fa57c168dc0f151de829fee_l3.png "Rendered by QuickLaTeX.com") be two functions defined at evenly spaced points, their convolution is given by: \

(2)    ![\begin{equation*}(f * g)_n:=\sum_{m=-\infty}^{m= \infty } f_m g_{n-m}.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-29052053859751093bb99b249aeadbe3_l3.png "Rendered by QuickLaTeX.com")

\
To speed up the kernel computation we will use a particular feature given by:\

(3)    ![\begin{equation*}\widetilde{ (f * g)_n }= \tilde{ f_n }  \cdot  \tilde{   g_n } \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-695b0b463e49279aac7187fe78dbcfb5_l3.png "Rendered by QuickLaTeX.com")

### 1.2 Using DFFT Convolution to estimate \hat{f}_h

Since the discrete convolution theorem requires functions observed at evenly spaced points we create a fine grid ![u \in (u_1, \dots u_{T'})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a08e33251585bb45626871a149105aae_l3.png "Rendered by QuickLaTeX.com") of length ![T'=2^k, k \in \mathbb{N}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-efa73b038dd36e0797bf0eecf811f72c_l3.png "Rendered by QuickLaTeX.com") where we want to evaluate the density. \
 

(4)    ![\begin{equation*}\hat{f}_h(u)= \frac{1}{T} \sum_{i=1}^{T} K_\textbf{h}(u- X_i )  =   \frac{1}{T} \sum_{i=1}^{T}  K_\textbf{h}(u) * \delta(u-  X_i )   \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0339d47cee6c84600e1c36eb526e645a_l3.png "Rendered by QuickLaTeX.com")

where ![\delta()](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-33f87a52d3db396356808e8cf6dd2fcc_l3.png "Rendered by QuickLaTeX.com") is the [dirac delta function](https://en.wikipedia.org/wiki/Dirac_delta_function). To derive the estimate for all points ![(u_1, \dots u_{T'})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6f2adf0c753ab39d4ef320344485ed3b_l3.png "Rendered by QuickLaTeX.com") the computer has to handle ![\mathcal{O}(T'T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fb2b9f6d4ebccfa746f171c6fc1b28e5_l3.png "Rendered by QuickLaTeX.com") operations.

Following [[1](#paperkey_25)], let the discrete Fourier transform of ![\hat{f}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-951d9dd89ec5b9234d00b1ec6f24bd53_l3.png "Rendered by QuickLaTeX.com") be denoted by ![\tilde{f}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8fe6551fcad8dbed6517f9c2ae95dde4_l3.png "Rendered by QuickLaTeX.com"). The Fourier transform of ([4](#id82495494)) for ![s \in   (u_1, \dots u_{T'})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2a982b86689977f4f72875fccb661788_l3.png "Rendered by QuickLaTeX.com") is then using convolution and translation given by \

(5)    ![\begin{equation*}\tilde{f}_h(s) = \frac{1}{T } \sum_{j=1}^{T}  \tilde{K}_\textbf{h}  (s) e^{i s X_j} =  \tilde{K}_\textbf{h}  (s) \tilde{u}(s) \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3776faf274f6245e7a77e30a7637a5fc_l3.png "Rendered by QuickLaTeX.com")

\
where ![\tilde{u}(s)=  \frac{1}{T }   \sum_{i=1}^{T}  e^{i s X_j}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-52b1a8f0f42d3bee8cb1a1c999a73297_l3.png "Rendered by QuickLaTeX.com") is the Fourier transform of the data. The result corresponding to ([4](#id82495494)) can then be obtained by applying the inverse DFFT. All these steps then involve only ![\mathcal{O}(T' log(T') )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9acfb1e544de5f67e6626d0b1a2d053a_l3.png "Rendered by QuickLaTeX.com") operations. ![\tilde{u}(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d619715c5dcd05955aa84d8b9a2ce05d_l3.png "Rendered by QuickLaTeX.com") is derived using a histogram on the observed data with binning boundaries defined by ![u_1, \dots u_{T'}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0c3e41a0a8de490c9a75d8198b0e8311_l3.png "Rendered by QuickLaTeX.com"), and then applying the Fast Fourier transform.

### 1.3 Implementation

To implement the method the fft function that comes with the numpy package was chosen. The numpy fft() function will return the approximation of the DFT from 0 to ![\pi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-26d6788550ffd50fe94542bb3e8ee615_l3.png "Rendered by QuickLaTeX.com"). Therefore fftshift() is needed to swap the output vector of the fft() right down the middle. So the output of fftshift(fft()) is then from ![-\pi/2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4a12d16db2ce3086d4772f6e2e52122c_l3.png "Rendered by QuickLaTeX.com") to ![\pi/2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c658187c700e99a5a8e304c146ee4f85_l3.png "Rendered by QuickLaTeX.com"). The computation using the fft was around 5 times faster.

```
import numpy as np
import matplotlib.pyplot as plt
import timeit
 
# Simulation
N=500
X=np.random.normal(-0,1.5,N)
 
plt.scatter(np.linspace(0,N,N), X, c="blue")
plt.xlabel('sample')
plt.ylabel('X')
plt.show()

# Presetting
Nout=2**7

def epan_kernel(u,b):
    u= u/b
    return max(0, 1./b*3./4*(1-u**2))   

# Usual estimation
def dens(s, X, h=0.5):
    return [epan_kernel((s-x)/h,1) for x in X]

start = timeit.default_timer()

grid =  np.linspace(-5, 5, num=Nout)   
density=[(1./X.size)*sum( dens(y, X) ) for y in grid] 
plt.plot(grid, density )
 
stop = timeit.default_timer()
print('Time: ', stop - start)  
 
# Estimation using FFT
start = timeit.default_timer()

to = np.linspace(-5, 5, Nout+1)
t = grid
h=0.5
kernel=[epan_kernel(x/h,1) for x in t]
kernel_ft=np.fft.fft(kernel)
hist,bins=np.histogram(X, bins=to)
density_tmp=kernel_ft.flatten()*np.fft.fft(  hist  )
denisty_fft=(1./X.size)*np.fft.fftshift( np.fft.ifft(density_tmp).real)
plt.plot(t, denisty_fft)
 
stop = timeit.default_timer() 
print('Time: ', stop - start)  
print(np.sqrt(sum((density-denisty_fft)**2)))
```

### References

[1] B. W. Silverman, “Algorithm as 176: kernel density estimation using the fast fourier transform,” Journal of the royal statistical society. series c (applied statistics), vol. 31, iss. 1, p. 93–99, 1982. \
 [[Bibtex]](javascript:void(0))

```
@article{Silverman1982,
ISSN = {00359254, 14679876},
URL = {http://www.jstor.org/stable/2347084},
author = {B. W. Silverman},
journal = {Journal of the Royal Statistical Society. Series C (Applied Statistics)},
number = {1},
pages = {93--99},
publisher = {[Wiley, Royal Statistical Society]},
title = {Algorithm AS 176: Kernel Density Estimation Using the Fast Fourier Transform},
volume = {31},
year = {1982}
}
```