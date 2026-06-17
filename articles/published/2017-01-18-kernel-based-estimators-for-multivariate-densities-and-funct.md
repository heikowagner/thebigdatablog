---
categories:
- All Articles
- Coding
- Matlab
date: '2017-01-18'
slug: kernel-based-estimators-for-multivariate-densities-and-functions
status: publish
tags: []
title: Kernel based Estimators for Multivariate Densities and Functions
wp_id: 635
wp_modified: '2026-06-11T18:46:25'
---

## 1. Kernel Functions

In general, a kernel ![K: \mathbb{R}^g \rightarrow \mathbb{R}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-09df18c30e1d49eba5d2af959244b6ff_l3.png "Rendered by QuickLaTeX.com")  is an integrable function  satisfying

1. ![\int_{\mathbb{R}^g} K(u) du =1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0abf14ea5d308ac6018a146cab939541_l3.png "Rendered by QuickLaTeX.com")
2. ![K(u)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-67c857a18d2b6a109e301374fa806db3_l3.png "Rendered by QuickLaTeX.com") is symmetric (e.g. ![K(u)=K(-u)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ec740d080e6e4d57bd03f0ec776ff85e_l3.png "Rendered by QuickLaTeX.com") if ![g=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9399e5db11b9844c4ff7dbdc24160267_l3.png "Rendered by QuickLaTeX.com"))
3. ![K(u) \geq 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-baa11e4c783482a96a8ac46bcbe099b3_l3.png "Rendered by QuickLaTeX.com").

Popular univariate (![g=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9399e5db11b9844c4ff7dbdc24160267_l3.png "Rendered by QuickLaTeX.com")) kernel functions:

- Uniform: ![K(u)= \frac{1}{2} \textbf{1}_{ \{|u|\leq 1 \} }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-708dbbebf4bdfa454d73e20f22b9467d_l3.png "Rendered by QuickLaTeX.com")
- Epanechnikov: ![K(u)= \frac{3}{4} (1-u^2)\textbf{1}_{ \{|u|\leq 1 \} }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6d8ec1da636b2598d7aaa46c4814d181_l3.png "Rendered by QuickLaTeX.com")
- Gaussian:  ![K(u)={\frac {1}{\sqrt {2\pi }}}e^{-{\frac {1}{2}}u^{2}}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-861cf6121c85de6143ebd191866dc98d_l3.png "Rendered by QuickLaTeX.com")

An easy way to construct a multivariate (g>1) kernel from an univariate kernel is to construct a product kernel. Let ![u=(u_1, \dots, u_g)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-557f90d36e5f766fe3180c25adcdd68b_l3.png "Rendered by QuickLaTeX.com") and ![K_u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2052f0451b8a57868de81a4685fde467_l3.png "Rendered by QuickLaTeX.com") be an univariate kernel then\

     ![\[K(u) = \prod_{i=1}^g K_u(u_i).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d92242cd97e77329bf918b83560183ea_l3.png "Rendered by QuickLaTeX.com")

An important feature is to scale kernel functions by a parameter matrix ![\textbf{H}=\{h_{ij}\}_{i,j=1,\dots,g}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4ab7584d01eb87c5178433dda31f4a5f_l3.png "Rendered by QuickLaTeX.com") with ![K_\textbf{H}(u)=|\textbf{H}|^{-1} K(\textbf{H}^{-1} u )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-388ba52c1f5dda4384592c474488efcb_l3.png "Rendered by QuickLaTeX.com").

## 2. Kernel Density Estimation

A famous application for kernels is to estimate the underlining density functions of a given independent and identically distributed ![g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d208fd391fa57c168dc0f151de829fee_l3.png "Rendered by QuickLaTeX.com")-variate random vectors ![(X_1,\dots, X_n)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd0a34c0e5709d3adfebd3713495c79e_l3.png "Rendered by QuickLaTeX.com") drawn from some distribution with an unknown density ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com"). A kernel based density estimator is then given by\

     ![\[\hat{f}_h(u)= \frac{1}{n} \sum_{i=1}^n K_\textbf{H}(u-X_i)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5d742e72f1b171227bf35c737b7a21a1_l3.png "Rendered by QuickLaTeX.com")

A naive Matlab implementation is straightforward:

```
```
% ------------------------------------------------------------------------------ 
% Description: g-Dimensional Density Estimator
%
% ------------------------------------------------------------------------------ 
% Usage:       - 
% ------------------------------------------------------------------------------ 
% Inputs Simulation:      
%X    - observations (Dimension: Txg)
%x    - g dimensional output coordinates (Dimension: T_outxg)
%H    - Bandwidth matrix (Dimension: gxg)
%type - Kernel choice, 'Gauss' for gaussian kernel, Epanechnikov else.
 
% ------------------------------------------------------------------------------ 
%Output:      
%fit  - Estimated Density
  
% ------------------------------------------------------------------------------ 
% Keywords:    kernel, density estimation
% ------------------------------------------------------------------------------ 
% See also:    -  
% ------------------------------------------------------------------------------ 
% Author:      Heiko Wagner, 2017/01/18
% ------------------------------------------------------------------------------ 
 
 
 
  
function [fit] = density(X,x,H,k_type)
T = size(X,1);
T_out = size(x,1);
 
%% Epanechnikov Kernel function
function [k]=epan(t);
k= 3/4*(1-t.^2);
   k((abs(t)-1)&gt;0)=0;
end
 
%%Construct Productkernel
function [A]=kernel(Xn)
g=size(Xn,2);
A=1;
    if(strcmp(k_type,'Gauss')==1)   %Use Gaussian Kernel
        for (m=1:g)
           A= A.*normpdf(Xn(:,m))  ;
        end
    else                            %Use Epanechnikov Kernel
        for (m=1:g)
           A= A.*epan(Xn(:,m))  ;
        end
    end   
end
 
Xn=zeros( size(X) ); 
function [f_j]=getpoint(x_j)
    %%%Construct g dimensional grid around point j, at this pint you can improve the code if you use the Epanechnikov Kernel by only selecting certain observations
    Xn = X - repmat( x_j,T,1 );  
    f_j= 1/T*det(H)^(-1)* sum( kernel(Xn*H^(-1)) )
end
%%%To estimate not just a single point we estimate the function for an entire set of g dimensional output coordinates (x) 
 
[out]=arrayfun(@(s) getpoint( x(s,:) ), 1:T_out , 'UniformOutput', false);
fit=[out{:}]';
end
```
```

The run time of this an algorithm in ![\mathcal{O}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-44dad1c4e1052d7a8f304c6031db469e_l3.png "Rendered by QuickLaTeX.com")-notation, that evaluates the density at ![m](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6b41df788161942c6f98604d37de8098_l3.png "Rendered by QuickLaTeX.com") points, is then given by ![\mathcal{O}(mn)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-470555de7746522969e5b44980050df0_l3.png "Rendered by QuickLaTeX.com"). Can we do better? [Yes, we can.](https://www.youtube.com/watch?v=uWRmBjFxttc&feature=youtu.be&t=1m10s) A smarter way is to make [use of the fast-fourier transformation](https://www.thebigdatablog.com/fast-kernel-density-estimation-using-the-fast-fourier-transform/) (FFT) introduced by [[1](#paperkey_38)].

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