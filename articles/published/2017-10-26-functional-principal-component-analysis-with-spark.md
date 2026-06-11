---
categories:
- All Articles
- Coding
- Functional Data Analysis with Spark
- Python
- Spark
date: '2017-10-26'
slug: functional-principal-component-analysis-with-spark
status: publish
tags: []
title: Functional Principal Component Analysis with Spark
wp_id: 1099
wp_modified: '2026-06-11T18:47:13'
---

## 1.) Functional Principal Component Analysis

Let ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") be a centered smooth random function in ![L^2([0,1])](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-120329f0cbd6d46f7911f558d5da7836_l3.png "Rendered by QuickLaTeX.com"), with finite second moment ![\int_{[0,1]} \EE\left[X(u)^2 \right]du < \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8949ff714d7487cfcbd54f4f54050c39_l3.png "Rendered by QuickLaTeX.com"). Without loss of generality we assume ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com") instead of some arbitrary compact interval and only consider centered functions. If non-centered curves are assume than the curves can be centered by subtracting ![E(X)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-592d20f54789f59923f4cfee3134e813_l3.png "Rendered by QuickLaTeX.com").

The underlying dependence structure can be characterized by the covariance function ![\sigma(t,v)\stackrel{\operatorname{def}}{=}E\left[X(t)X(v)\right]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8eaf2776270146070980bb4f5fe8821f_l3.png "Rendered by QuickLaTeX.com") and\
the corresponding covariance operator ![\Gamma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4f420945e64069f30b66c3d17e2f98ac_l3.png "Rendered by QuickLaTeX.com")\

(1)    ![\begin{equation*} (\Gamma \vartheta)(t)=\int_{[0,1]}\sigma(t,v)\vartheta(v)dv. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2208aed411cf7805955a14e812c21505_l3.png "Rendered by QuickLaTeX.com")

Let ![\lambda_1\geq \lambda_2\geq \dots](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-285387a70fe02c65edd661f1849916f6_l3.png "Rendered by QuickLaTeX.com") denote the ordered eigenvalues of ![\sigma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1c9cc40f96a1492e298e7da85a2c1692_l3.png "Rendered by QuickLaTeX.com") and let ![\gamma_1,\gamma_2,\dots](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8312a12fe0ba4f24a195cf8a26765223_l3.png "Rendered by QuickLaTeX.com") be a corresponding system of orthonormal\
eigenfunctions (functional principal components) s.t. ![\sigma(t,v)= \sum_{r=1}^\infty \lambda_r \gamma_r(t) \gamma_r(v)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e13c38c52e08a4b2c24f7e966764b3dd_l3.png "Rendered by QuickLaTeX.com"). The Karhunen-Loeve decomposition states that the random functions ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") can be represented in the form\

(2)    ![\begin{equation*}  X(t)=\sum_{r=1}^{\infty} \delta_{r} \gamma_r(t) \qquad \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9a985788f6aaaad734a27c97e820f6e_l3.png "Rendered by QuickLaTeX.com")

where the loadings ![\delta_{r}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd3e7f915104fc87e882f4aab2044be0_l3.png "Rendered by QuickLaTeX.com") are random variables defined as ![\delta_{r}\stackrel{\operatorname{def}}{=} \int_{[0,1]} X(t) \gamma_r(t) du](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d3f31d3dc3aeacc5a4f940e8f1d075b0_l3.png "Rendered by QuickLaTeX.com") that satisfy ![E \left(\delta_{r}^2\right)=\lambda_r](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-858ad4f578428e1499d4d0208d01ef8f_l3.png "Rendered by QuickLaTeX.com"), as well as ![E \left(\delta_{r}\delta_{s}\right)=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-49ed2fde95522b06233dff104d29857f_l3.png "Rendered by QuickLaTeX.com") for ![r\neq s](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3940c580d59e4b9cee90cea62f682eab_l3.png "Rendered by QuickLaTeX.com"). ![\gamma_r(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f15a8a4c8d7c8933c4eeaeaafb2d11ec_l3.png "Rendered by QuickLaTeX.com") are denoted as functional principal components and ![\delta_{r}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dd3e7f915104fc87e882f4aab2044be0_l3.png "Rendered by QuickLaTeX.com") the corresponding principal scores.

### 1.1) Example: Brownian motion

A nice analytical example where we can actually calculate the principal components is the brownian motion. Let ![X(t)=W_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c02461365032df409a739aa4bcbfa08_l3.png "Rendered by QuickLaTeX.com") be a brownian motion on ![t \in [0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-71cb59b47162bcfb713d829c70c6278a_l3.png "Rendered by QuickLaTeX.com"), then its probability density function is given by ![f_{W_t} (x)= \frac{1}{\sqrt{2 \pi t} }e^{-x^2/(2t)}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fe7762db06d8aa59a0856aa7c99e7e64_l3.png "Rendered by QuickLaTeX.com"). Accordingly ![E(W_t)=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-243f69b8f79336e896f5a082a8abee18_l3.png "Rendered by QuickLaTeX.com") and ![Var(W_t)= E(W_t^2)-E^2(W_t)=E(W_t^2)=t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-337f725cd7f16bfdb519bc1b8d486303_l3.png "Rendered by QuickLaTeX.com"). The covariance function with ![t<s](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-73d656a03c3f41c74354f12063e73744_l3.png "Rendered by QuickLaTeX.com")  is then given by

     ![\[\sigma(t,s)= E( W_t W_s)=E(W_t ( (W_s -W_t)  )  +E(W_t^2) =  E(W_t- W_0) E (W_s -W_t  )  +E(W_t^2)=t\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7f1240733122080269f87c70b8f9fe0f_l3.png "Rendered by QuickLaTeX.com")

since for ![0 \leq s_1<t_1\leq t_2<s_2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-94e374d428b2266f8db6077100050093_l3.png "Rendered by QuickLaTeX.com"), ![W_{t_1}-W_{s_1}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0a766baa143bb9202dcbc50b00e3514a_l3.png "Rendered by QuickLaTeX.com") and ![W_{s_2}-W_{t_2}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-178d103376495f83847e99b3d94e0c84_l3.png "Rendered by QuickLaTeX.com")  are independent random variables. Thus  ![\sigma(t,s)= min(t,s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ce42ea267f79893f9500140954029360_l3.png "Rendered by QuickLaTeX.com") and we have to solve the following eigenvalue problem

     ![\[ \int_{[0,1]}min(t, s) \vartheta(s)_r ds = \lambda_r \vartheta_r (t)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6cbc5fba0d481395d8885cc67d0682a7_l3.png "Rendered by QuickLaTeX.com")

wich can be rewritten as

     ![\[ \int_{[0,t]}min(t, s) s \vartheta_r(s) ds + t \int_{[t,1]}min(t, s) \vartheta_r(s) ds = \lambda_r \vartheta_r (t)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4ea115dec2a27aa4ff8399be7dceb8f7_l3.png "Rendered by QuickLaTeX.com")

. Differentiating once leads to ![\int_{[t,1]}min(t, s) \vartheta_r(s) ds = \lambda_r \vartheta_r'(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fb6f443b52fc473889a43690b0441f44_l3.png "Rendered by QuickLaTeX.com") this gives us two boundary conditions given by ![\vartheta_r(0)=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1e306b4eabe12e424df6a5e9f9840939_l3.png "Rendered by QuickLaTeX.com") and ![\vartheta'_r(1)=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-df8e58153fa66eaf36462e503fe17b57_l3.png "Rendered by QuickLaTeX.com"). Differentiating again leads to ![- \vartheta_r(t) =\lambda_r \vartheta''_r(t).](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ec9368885700aaca48cca50f991e9737_l3.png "Rendered by QuickLaTeX.com") In fact this is the standart example from basic math curses introducing [Sturm-Liouville](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_theory) and a solution is given by

     ![\[\lambda_r=  \left(\frac{1}{(r-\frac{1}{2} )\pi} \right)^2 , \vartheta_r(t)=\sqrt{2} sin\left((r-\frac{1}{2} )\pi t \right).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-84414bd751430f06bc55082a2181a43b_l3.png "Rendered by QuickLaTeX.com")

Using that ![E \left(\delta_{r}^2\right)= \left(\frac{1}{(r-\frac{1}{2} )\pi} \right)^2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a0eb2c99bf5bb096f96fa9b33f992978_l3.png "Rendered by QuickLaTeX.com") with ![Z_r \sim N(0,1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3b2e9add073d6ebad519e72a496d386a_l3.png "Rendered by QuickLaTeX.com") the Karhunen-Loeve decomposition is given by

     ![\[W_t=\sqrt{2} \sum_{r=1}^\infty \frac{Z_r}{(r-\frac{1}{2} )\pi}   sin\left((r-\frac{1}{2} )\pi t \right).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-860d5830f28e89d76ca38ab6680e0d13_l3.png "Rendered by QuickLaTeX.com")

## 2.) A Spark implementation

Usually a sample of ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") curves is observed, in addition Spark is not able to handle functions but is only able to process discrete data. To model these issues, let ![X_1,\dots, X_N \in L^2([0,1])](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b80aff427cc0d0d11a5e9d4d947f90b2_l3.png "Rendered by QuickLaTeX.com") be an i.i.d. sample of smooth curves with continuous covariance function, we assume that each curve in the sample is observed at an equidistant grid ![(t_1, \dots, t_T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-47d3f1244d059b5dd5822d04519746b8_l3.png "Rendered by QuickLaTeX.com"). We will thus use empirical approximation of the covariance function is then given by the sample covariance matrix

     ![\[\hat{\sigma}(t_j,t_k) = \frac{1}{N} \sum_{i=1}^N X_i(t_j) X_i(t_k).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d029fedf469df0112744815ac3ea9634_l3.png "Rendered by QuickLaTeX.com")

to derive an estimator for the functional components one will usually rely on an eigenvalue decomposition of ![\{\hat{\sigma}(t_j,t_k)\}_{i,j=1,\dots,T}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9fc9bca47db9edfb6b0c4492feb99390_l3.png "Rendered by QuickLaTeX.com"). For the Spark implementation, let us focus now on an alternative way to estimate the Karhunen-Loeve decomposition based on the duality relation between row and column space. Let ![M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10ebb71bad275c1815a8f2a8c5dea0be_l3.png "Rendered by QuickLaTeX.com") be the dual matrix consisting of entries\

(3)    ![\begin{equation*} M_{ij}= \sum_{k=1}^T X_i(t_k) X_j(t_k). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7e0d4653174ed8cf785889034bd75246_l3.png "Rendered by QuickLaTeX.com")

The eigenvectors ![p_r=(p_{1r}, \ldots, p_{Nr})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e23b51eaaae53a28c41779bdfea696bc_l3.png "Rendered by QuickLaTeX.com") and eigenvalues ![l_r](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0d82b1c0d0a2db75d997d1bd8c3f1da8_l3.png "Rendered by QuickLaTeX.com") of the matrix ![M](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10ebb71bad275c1815a8f2a8c5dea0be_l3.png "Rendered by QuickLaTeX.com") are connected to the empirical ![\hat{\gamma}_r](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-72b55b9b08df1e94ec4c0f1f31f207eb_l3.png "Rendered by QuickLaTeX.com"), ![\hat{\lambda}_r](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-381fbc1b265a73d1302e40c8450b98de_l3.png "Rendered by QuickLaTeX.com") and ![\hat{ \delta }_{r}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f0e4ab5d806a6dc18b99d920e46fe79c_l3.png "Rendered by QuickLaTeX.com"), resulting in replacing the expectation in![\sigma(t,v)\stackrel{\operatorname{def}}{=}E\left[X(t)X(v)\right]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8eaf2776270146070980bb4f5fe8821f_l3.png "Rendered by QuickLaTeX.com") with the empirical counterpart and the integral in ([1](#id289926050)) by a rieman sum, by ![\hat{\gamma}_r(t)= \frac{1}{ \sqrt{l_r} } \sum_{i=1}^N p_{ir} X_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-03684c60c113d83d0d7c434ced2a9574_l3.png "Rendered by QuickLaTeX.com"), ![\hat{\lambda}_r=\frac{1}{N} l_r](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-acd67c568419ceeab02baf1a082c2c16_l3.png "Rendered by QuickLaTeX.com")  and ![\hat{ \delta }_{r}=\sqrt{l_r}p_{ir}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3c748286d6b4139c0cb464fc072952ae_l3.png "Rendered by QuickLaTeX.com")

### 2.1) Test the Algorithm using the Brownian Motion

[![](https://www.thebigdatablog.com/wp-content/uploads/2017/10/figure_1-300x225.png)](https://www.thebigdatablog.com/wp-content/uploads/2017/10/figure_1.png)

The figure shows the first two true principal components of a brownian motion and the estimates from the presented algorithm

Let ![Z_m \sim N(0,1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1b865c7bf34f6cdbf95370fae4d23f05_l3.png "Rendered by QuickLaTeX.com"), we simulate a standard Brownian Motion at points ![(0, \frac{1}{T}, \frac{2}{T},\dots,\frac{T-1}{T} ,1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cf15b809c1ec5ad446563a8cedb52e6d_l3.png "Rendered by QuickLaTeX.com") with ![m \leq T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bc53b787e1562553e528ff0828e74f89_l3.png "Rendered by QuickLaTeX.com") by

     ![\[X_T \left( \frac{m}{T} \right) = \frac{1}{ \sqrt{T} } \sum_{1<k \leq  m } Z_k.\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a2c07c90db902f3768b951f27b5b7d76_l3.png "Rendered by QuickLaTeX.com")

Using [Donsker’s theorem](https://en.wikipedia.org/wiki/Donsker%27s_theorem) one can then show that for ![T \rightarrow \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b57896efc7f80db13d8f1b5da96baea7_l3.png "Rendered by QuickLaTeX.com"),  ![X_T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2c5ebc56cc78e759ba288500d4138da6_l3.png "Rendered by QuickLaTeX.com") converges in distribution to a standard brownian motion ![W](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4caed22919a1780df1b6310b338b904e_l3.png "Rendered by QuickLaTeX.com"). To test the algorithm we sample ![N=400](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d8b43b6a7bfa632b76fee63b4cd24c86_l3.png "Rendered by QuickLaTeX.com") curves ![X_{T,i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297685994a92a554ae1703101e12b275_l3.png "Rendered by QuickLaTeX.com") at ![T=10000](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2f4798e04b246a24a6385eed34f5b63e_l3.png "Rendered by QuickLaTeX.com") equidistant timepoints.

### 2.2) Implementation

As an primary example and to check if our algorithm works the way we intended, we will sample a set of ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") curves from the space of brownian motions. These curves where computed at the master and then be transfered to the spark cluster where the Spark-FPCA is performed. The functional principal components  are then transferred back to the master where we compare our estimates with the true functional principal components  derived in the previous sections.

```

#We start with a sample of brownian motions
import matplotlib.pyplot as plt
from numpy import *
from pyspark.mllib.linalg import *
from pyspark.mllib.linalg.distributed import *
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry

def spark_FPCA( matrix , L):
    N = matrix.numRows()  
    T = matrix.numCols()  
    scale =CoordinateMatrix(sc.parallelize(range(N)).map(lambda i: MatrixEntry(i, i, 1./sqrt(T) )), N, N).toBlockMatrix()
    # Compute the top L singular values and corresponding singular vectors.
    svd = scale.multiply(matrix).transpose().toIndexedRowMatrix().computeSVD(L)
    s = svd.s       # The singular values are stored in a local dense vector.
    Va=svd.V.toArray()
    Vl = list();
    for i in range(0, len(Va)):
        Vl.append( IndexedRow(i, Va[i] ))
    V=IndexedRowMatrix( sc.parallelize(Vl) )
    S=DenseMatrix( L,L, diag(s).flatten().flatten().tolist() )
    Si=DenseMatrix( L,L, diag(1./(s)).flatten().flatten().tolist() )
    scores=V.multiply(S)
    components= matrix.transpose().multiply( V.multiply(Si).toBlockMatrix() )
    #reduced FPCA decomposition
    FPCA= components.multiply(scores.toBlockMatrix().transpose() )
    return (components, scores, FPCA, s)

def reuse_FPCA( matrix , components):
    N = matrix.numRows()  
    T = matrix.numCols()  
    scaler=CoordinateMatrix(sc.range(N).map(lambda i: MatrixEntry(i, i, 1./T)), N, N).toBlockMatrix()
    scores=scaler.multiply(matrix).multiply( components )
    FPCA= components.multiply(scores.transpose() )
    return (components, scores.toIndexedRowMatrix(), FPCA)




##EXAMPLE USING A BROWNIAN MOTION

T=10000
N=400
L=2

data = list();
for i in range(0, N):
    data.append( IndexedRow(i, array( cumsum(random.normal(0,sqrt(true_divide(1,T)),T)) ) ) )

#convert the data to spark
sc_data= sc.parallelize( data )
matrix = IndexedRowMatrix(sc_data).toBlockMatrix().cache()

result=spark_FPCA(matrix, 3)

FPCA=result[2].toLocalMatrix()
comp=result[0].toLocalMatrix()
scores_old=result[1].rows.collect()


#Component plots
times=true_divide( arange(0,T),T )
true_comp=list();
for i in range(1, L+1):
    true_comp.append( sin( (i-0.5)*pi*times) )

for i in range(0,len(true_comp)):
    plt.plot(times, true_comp[i])

for i in range(1,len(comp.toArray()[1,:])+1):
    plt.plot(times, 0.7*comp.toArray()[:,(i-1)]) ##I have no idea where the scaling diff comes from... :(

plt.show()


##Construct new Brownian motion to reuse principal components
data = list();
for i in range(0, N):
    data.append( IndexedRow(i, array( cumsum(random.normal(0,sqrt(true_divide(1,T)),T)) ) ) )

plt.plot(times, array( cumsum(random.normal(0,sqrt(true_divide(1,T)),T)) ) ) 
plt.show()

#convert the data to spark
sc_data= sc.parallelize( data )
matrix2 = IndexedRowMatrix(sc_data).toBlockMatrix().cache()
result2=reuse_FPCA(matrix2, result[0])

##New Scores
result2[1].rows.collect()
```