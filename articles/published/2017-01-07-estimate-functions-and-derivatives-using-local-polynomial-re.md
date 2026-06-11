---
categories:
- All Articles
- Coding
- Matlab
date: '2017-01-07'
slug: estimate-functions-and-derivatives-using-local-polynomial-regression-with-multivariate-domains-in-matlab-using-the-gpu
status: publish
tags: []
title: Estimating Multivariate Functions and Derivatives using Local Polynomial Regression
  in Matlab
wp_id: 494
wp_modified: '2023-10-01T10:13:31'
---

## 1. Theoretical Background

I want to start with some theory which will in the end lead us to the Matlab coding. If you are not interested how to derive the estimator in detail, feel free to skip this section. If you are interested in a detailed discussion about local polynomial regression I recommend to have a look into [Fan and Gijbles (1996).](https://www.amazon.de/Local-Polynomial-Modelling-Its-Applications/dp/0412983214/ref=sr_1_1?ie=UTF8&qid=1483642767&sr=8-1&tag=addonsdeaddonssh)

We assume that a smooth curve ![X(t) \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c0be693365510f29947884542b73c10_l3.png "Rendered by QuickLaTeX.com") is observed at independent randomly-distributed points ![t_{k} \in [0,1]^g, \; k=1,\dots, T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1eaf5854ea4686e5e92a7ebd2df11935_l3.png "Rendered by QuickLaTeX.com") contaminated with additional noise. Our model is then given by\

(1)    ![\begin{equation*}  Y(t_{k})=X(t_{k}) + \epsilon_{k} \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-84eb8f7c4e2f0c21550b358da2e8c128_l3.png "Rendered by QuickLaTeX.com")

where ![\epsilon_{k}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6a73ce66b01132aee7db6cf26a6969f2_l3.png "Rendered by QuickLaTeX.com") are i.i.d. random variables with ![\mathbf{E}\left[\varepsilon_{k}\right]=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8f6558af68aa91a272e82851f098d9a4_l3.png "Rendered by QuickLaTeX.com"), ![\var\left(\epsilon_{k}\right)= \sigma^2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad3a49ff8ae5dc879acdfc22bce23a92_l3.png "Rendered by QuickLaTeX.com") and ![\epsilon_{k}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6a73ce66b01132aee7db6cf26a6969f2_l3.png "Rendered by QuickLaTeX.com") is independent of ![X= X(t_1),\dots, X(t_k)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5dc4eb816214633778f1afa63edeb356_l3.png "Rendered by QuickLaTeX.com").

Our goal is then to estimate partial derivatives  which are denoted using a vector ![d=(d_1,\dots,d_g)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2d3306de29c9800d4f5b52b28ddef02d_l3.png "Rendered by QuickLaTeX.com")

(2)    ![\begin{equation*} X^{(d)}(t) \stackrel{\operatorname{def}}{=} \frac{\partial^{d_1} }{\partial t_1^{d_1} } \cdots \frac{\partial^{d_g} }{\partial t_g^{d_g} } X(t_1,\dots,t_g). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0e4407428455b549788182e9dd1a89f_l3.png "Rendered by QuickLaTeX.com")

For the following a little notation is needed. For any vectors ![a,b \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-73fedacc2f781ce77d8928449ff870a6_l3.png "Rendered by QuickLaTeX.com")  we define ![|a|\stackrel{\operatorname{def}}{=}\sum_{j=1}^g |a_j|](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-33e13ea8e7ce9aeae13e55df70352176_l3.png "Rendered by QuickLaTeX.com"), ![a^b\stackrel{\operatorname{def}}{=}a_1^{b_1} \times \dots \times a_g^{b_g}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-19e52c669f8917bcd5b38f03eb633996_l3.png "Rendered by QuickLaTeX.com"). Let ![k=(k_1,\dots, k_g)^{\top}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-667d54b50f2819d02bf03d49a38f27a3_l3.png "Rendered by QuickLaTeX.com"), ![k_l \in \mathbb{N}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fe4043f7eaf278ee1360e5242bc54585_l3.png "Rendered by QuickLaTeX.com") and consider a multivariate local polynomial estimator of order ![\rho](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-da039068127cf2ec5fc05123d4d3546f_l3.png "Rendered by QuickLaTeX.com") for a point ![t \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9058333516e99e10fd782d5557b71286_l3.png "Rendered by QuickLaTeX.com") given by ![\hat{\beta}(t) \in \mathbb{R}^\rho](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-beaa283119291bf31826fe255201fe6a_l3.png "Rendered by QuickLaTeX.com") that solves\

(3)    ![\begin{equation*} \underset{\beta(t)}{\operatorname{min}} \sum_{l=1}^{T} \left[ Y(t_{l}) - \sum_{0 \leq |k| \leq \rho} \beta_{k}(t) (t_{l}-t)^k \right]^2 K_{B} (t_{l}-t). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-490d704c75efa52288303055e7a62d65_l3.png "Rendered by QuickLaTeX.com")

![K_B](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f84e77833b3d8867b78717f6c2056f91_l3.png "Rendered by QuickLaTeX.com") is any non-negative, symmetric and bounded  multivariate kernel function and ![B](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-770fd1447ccf2fc229801b486b0d8f8a_l3.png "Rendered by QuickLaTeX.com") a ![g \times g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8f5f25b5f8da1aa28ef943187d4c2cef_l3.png "Rendered by QuickLaTeX.com") bandwidth matrix. For simplicity, we assume that ![B](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-770fd1447ccf2fc229801b486b0d8f8a_l3.png "Rendered by QuickLaTeX.com") has main diagonal entries ![b=(b_1,\dots,b_g)^{\top}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-57fef08b2f3cb9c9b3b61d07083a8141_l3.png "Rendered by QuickLaTeX.com") and zero elsewhere. Remember that ![\hat{\beta}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2082eaf04f0572beba55413565117c02_l3.png "Rendered by QuickLaTeX.com") is a vector of size ![\rho](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-da039068127cf2ec5fc05123d4d3546f_l3.png "Rendered by QuickLaTeX.com"), the desired estimates are then given by ![\hat{X}^{(d)}(t) = |d|! \hat{\beta}_c(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7e7c7089d536b90845d637a3a607d0e2_l3.png "Rendered by QuickLaTeX.com") where ![c](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-41a04eeea923a1a0c28094a8a4680525_l3.png "Rendered by QuickLaTeX.com") is the position in the vector which is dependent on the ordering of the polynomials in ([3](#id1376896768)).

To code the estimator in Matlab we will write down the estimator using matrices. Let ![\tilde{t}_l=(t_{l}-t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dffd6a2f899d0bc0131f5e4beb6271f3_l3.png "Rendered by QuickLaTeX.com"),

     ![\begin{equation*} \textbf{Z}(t)= \begin{bmatrix} 1/g& \tilde{t}_{11} & \tilde{t}_{12} & \dots & \tilde{t}_{11}  \tilde{t}_{12} & \dots & \tilde{t}_{1g}^\rho\\ 1/g& \tilde{t}_{21} & \tilde{t}_{22} & \dots & \tilde{t}_{21}  \tilde{t}_{22} & \dots & \tilde{t}_{2g}^\rho\\ \vdots & \vdots & \vdots & \ddots & \vdots & \ddots & \vdots\\ 1/g& \tilde{t}_{T1} & x_{T2} & \dots & \tilde{t}_{T1}  \tilde{t}_{T2} &\dots & \tilde{t}_{Tg}^\rho \end{bmatrix} , \textbf{A}(t) = \begin{bmatrix} K_{B} (\tilde{t}_{1}) & 0 & \dots & 0 \\ 0& K_{B} (\tilde{t}_{2}) & \dots & 0 \\ \vdots &  \vdots & \ddots & \vdots \\ 0 & 0 & \dots & K_{B} (\tilde{t}_{T}) \end{bmatrix} \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8645d9f15b4dc53fe4280fa094d28f09_l3.png "Rendered by QuickLaTeX.com")

using this notation together with ![\textbf{Y}=( Y(t_1),\dots,Y(t_T) )^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-829f4a7205dd2ace016a69a438955c01_l3.png "Rendered by QuickLaTeX.com") , ([3](#id1376896768)) can then be rewritten as\

(4)    ![\begin{equation*} min_{\beta(t)} \textbf{Z}(t)^T \textbf{A}(t) \textbf{Y} - \beta(t) \textbf{Z}(t)^T \textbf{A}(t) \textbf{Z}(t) \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8124f99078222d6f8541404e5c656b50_l3.png "Rendered by QuickLaTeX.com")

([4](#id2219898318)) looks very much like a least squares problem, and under some regularity assumptions the solution is given by\

(5)    ![\begin{equation*} \hat{\beta}(t)= \left( \textbf{Z}(t)^T \textbf{A}(t) \textbf{Z}(t) \right)^{-1} \textbf{Z}(t)^T \textbf{A}(t) \textbf{Y}. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a549f3b315c171fa447e322a67d791fb_l3.png "Rendered by QuickLaTeX.com")

This expression is then indeed easy to code.

## 2. Implementation using Matlab

The implementation is based on product kernels of a Gaussian and an Epanechnikov kernel. For running a kernel regression on very large data sets bounded kernels like the Epanechnikov kernel are of particular interest because a lot of entries in ([4](#id2219898318)) will become zero if ![t_l](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-85faaa5839427ee5cd0247a4b226490e_l3.png "Rendered by QuickLaTeX.com") is far from ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com"). A conscientious programmer will thus chose only a certain window based on ![t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4e3cbf5d4c5c6d9b702dd139f14c147_l3.png "Rendered by QuickLaTeX.com") and bandwidth ![b](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f56d50c26583f9a035ff6b4e3c0ca5c0_l3.png "Rendered by QuickLaTeX.com") of observations to construct ![\textbf{Z}(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a4c865d0b1b6f484dc0e71a728f50819_l3.png "Rendered by QuickLaTeX.com") and compute to ([5](#id883904433)). Since I am not a conscientious programmer and I chose to keep the implementation simple this time, in this implementation this speed-up opportunity is omitted 😉

```

% ------------------------------------------------------------------------------ 
% Description: g-Dimensional local polynomial estimator 
%
% ------------------------------------------------------------------------------ 
% Usage:       - 
% ------------------------------------------------------------------------------ 
% Inputs Simulation:      
%X - g dimensional inputcoordinate (Dimension: Txg)
%Y - function value (Dimension: Tx1) 
%x - g dimensional output coordinates (Dimension: T_outxg)
%b - g dimensional vector of  bandwiths (Dimension: 1xg) 
%p - degree of polynomial (rho)
  
% ------------------------------------------------------------------------------ 
%Output:      
%fit  - Smoothed curves and derivatives
 
% ------------------------------------------------------------------------------ 
% Keywords:    local polynomial surface estimator, derivatives
% ------------------------------------------------------------------------------ 
% See also:    -  
% ------------------------------------------------------------------------------ 
% Author:      Heiko Wagner, 2017/01/18
% ------------------------------------------------------------------------------ 



 
function [fit] = multilocpoly(X,Y,x,b,p,kernel)

%% Epanechnikov Kernel function
function [k]=epan(t);
%t=(-100:100)/50
k= 3/4*(1-t.^2);
   k((abs(t)-1)>0)=0;
end


g= size(X,2) ;
T = size(X,1);
T_out = size(x,1);
dummy=permn(0:p,g);             %%%Get all possible combinations
k=dummy( sum(dummy,2)<p+1,:);
pp=size(k,1);    
Z = zeros( T, pp );   

function [beta_j]=getpoint(x_j)
    %%%Construct g dimensional grid around point j, at this pint you can improve the code if you use the Epanechnikov Kernel by only selecting certain observations
    Xn = X -  repmat( x_j,T,1 );  
     
    %%%Construct polynomials
    for m=1:pp
        Z(:,m)= prod( Xn.^repmat(k(m,:),T,1) ,2);
    end
     
    %%%Construct g-dimensional product kernel
    A=1;
    if(strcmp(kernel,'Gauss')==1)   %Use Gaussian Kernel
        for (m=1:g)
           A= A.*normpdf(Xn(:,m)/b(m))/b(m)  ;
        end
    else                            %Use Epanechnikov Kernel
        for (m=1:g)
           A= A.*epan(Xn(:,m)/b(m))/b(m)  ;
        end
    end
    A=diag(A); 
    
    %%%Solve for beta_j
    beta_j = inv(Z' * A * Z) * Z' * A * Y; 
end
%%%To estimate not just a single point we estimate the function for an entire set of g dimensional output coordinates (x) 
[out]=arrayfun(@(s) getpoint( x(s,:) ), 1:T_out , 'UniformOutput', false);
fit=[out{:}]'*diag(max(1,factorial( sum(k,2) )));
end
end
```