---
categories:
- All Articles
- Coding
- Functional Data Analysis with Spark
- Python
- Spark
date: '2017-12-08'
slug: functional-regression-with-spark
status: publish
tags: []
title: Functional Regression with Spark
wp_id: 1208
wp_modified: '2026-06-11T18:47:19'
---

# 1. Functional Regression

Let the covariate ![X= (X(t), t \in [0,1])](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-75e2983a5e08dba202a6c03e9723948e_l3.png "Rendered by QuickLaTeX.com") be an at least twice continuously differentiable random function defined wlog. on an interval ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com") and ![Y \in \mathbb{R}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e0359cd9111b54530a1a8797a0bde70b_l3.png "Rendered by QuickLaTeX.com") the corresponding the response. For simplicity we assume centered random variables, i.e. ![E(X)=0, E(Y)=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-07dcbb93fe4ffdcb4ef653ccf60d2269_l3.png "Rendered by QuickLaTeX.com") beside we require bounded second moments ![E(Y^2)< \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-75bcf6402bf367d78646362c5be79389_l3.png "Rendered by QuickLaTeX.com"), ![\int_0^1 E(X(t)^2)< \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b833cf07a5034c64b20d488110861c59_l3.png "Rendered by QuickLaTeX.com"). We assume that there exists some ![\beta \in L^2[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e806b3b1fd92dca87be10f1f800a77a1_l3.png "Rendered by QuickLaTeX.com") that satisfies\

(1)    ![\begin{align*} Y= \int_0^1 \beta(t) X( t ) dt. \end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fec280321772b05b6c74cd3391072630_l3.png "Rendered by QuickLaTeX.com")

We define cross-covariance functions of X and Y given by\

(2)    ![\begin{align*} g(t)= E ( Y X )(t). \end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2d13ded4d527168a9ff6932646d37474_l3.png "Rendered by QuickLaTeX.com")

Let ![\Gamma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4f420945e64069f30b66c3d17e2f98ac_l3.png "Rendered by QuickLaTeX.com") be the covariance operator of ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") as defined in [this post](https://www.thebigdatablog.com/functional-principal-component-analysis-with-spark/) with ordered eigenvalues ![\lambda_1, \lambda_2, \dots](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ef3c24db3f62684db0798341bf606d4d_l3.png "Rendered by QuickLaTeX.com") and corresponding eigenfunctions ![\gamma_1(t),\gamma_2(t), \dots](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad0f4be7f3c2d8ecddd0bc0254af193e_l3.png "Rendered by QuickLaTeX.com"), then ![\beta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b6a7605b1bcca8f1b416eaf733f34e08_l3.png "Rendered by QuickLaTeX.com") statisfies ([1](#id2256955701)) if and only if\

(3)    ![\begin{align*} (\Gamma \beta)(t) = g(t). \end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-282b7b7eb4f3da7c56172f54adc5e5af_l3.png "Rendered by QuickLaTeX.com")

([3](#id3348370790)) has a solution if and only if ![\Gamma](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4f420945e64069f30b66c3d17e2f98ac_l3.png "Rendered by QuickLaTeX.com") is invertible, for ![\lambda_i>0 \; \forall i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-31f9fa92f49ce0a0e94f7ec089ef0309_l3.png "Rendered by QuickLaTeX.com") the unique solution is then given by\

(4)    ![\begin{align*} \beta(t)= \int_0^1 \sum_{i=1}^\infty \lambda_i^{-1} \gamma_i(t) \gamma_i(s) g(s) ds. \end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-73a0551fe5f32514e896555d54d779b4_l3.png "Rendered by QuickLaTeX.com")

However this solution is unstable as to be seen by a simple example. Consider some ![\epsilon >0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-947854770f83d0b76b95eaac0c514357_l3.png "Rendered by QuickLaTeX.com"), and define ![g^{\epsilon}(t):= g(t) + \epsilon \gamma_i(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ddd9d361482cd8527582fa1e2acb713e_l3.png "Rendered by QuickLaTeX.com"). Then as ![i \rightarrow \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b879c13d4e95015c54ac37a206994e0e_l3.png "Rendered by QuickLaTeX.com")\

(5)    ![\begin{align*} ||\int_0^1 \sum_{i=1}^\infty \lambda_i^{-1} g(s) \gamma_i(s) \gamma_i(t) ds - \int_0^1 \sum_{i=1}^\infty \lambda_i^{-1} g^{\epsilon}(s) \gamma_i(s) \gamma_i(t) ds || = \lambda_i^{-1} \epsilon \rightarrow \infty. \end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4a17d052b5dad79d281f436027a3861a_l3.png "Rendered by QuickLaTeX.com")

This means that small pertubations in ![g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d208fd391fa57c168dc0f151de829fee_l3.png "Rendered by QuickLaTeX.com") leads to a large variation (even infinite) in ![\beta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b6a7605b1bcca8f1b416eaf733f34e08_l3.png "Rendered by QuickLaTeX.com"). There are various ways to tackle this problem, the key idea is to trade the uniqness for the stabilty of the a solution. This is archieved by reducing the dimensionality of the covariance operator. By doing so we do not solve the same problem but another one that is somewhat close to the original problem.\
A popular approach is to smooth the regression or to truncate the expansion after some ![L](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66a9f474fc3c52efdfb0ba6a70199ee8_l3.png "Rendered by QuickLaTeX.com"). This truncation approach will be the foundation of our spark implementation.

## 1.1 Simulation

[![](https://www.thebigdatablog.com/wp-content/uploads/2017/12/figure_2-300x225.png)](https://www.thebigdatablog.com/wp-content/uploads/2017/12/figure_2.png)

The figure shows the true regression function beta(t) and the estimate from the algorithm.

For our simulation we will again assume a brownian motion ![X(t)=W_t](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c02461365032df409a739aa4bcbfa08_l3.png "Rendered by QuickLaTeX.com") on ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com") and ![\beta(t)= sin(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-05d3563ded424a77d419d62072354c6e_l3.png "Rendered by QuickLaTeX.com"). For the simulation we sample ![N=800](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-705cb21b1bbfb4fcb69decb8d6a46b39_l3.png "Rendered by QuickLaTeX.com") curves and approximate ![W_{t,i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f2225c7966a5947b6dc56d57ec2719b5_l3.png "Rendered by QuickLaTeX.com") as proposed in [this post](https://www.thebigdatablog.com/functional-principal-component-analysis-with-spark/) with ![X_{T,i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297685994a92a554ae1703101e12b275_l3.png "Rendered by QuickLaTeX.com") at ![T=5000](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-832d5b32de764c6b3fbb78e27d778fd7_l3.png "Rendered by QuickLaTeX.com") timepoints ![(t_1,\dots,t_T)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-def80c76058ddf59ca1872c3994bb55e_l3.png "Rendered by QuickLaTeX.com"), accordingly ![Y_{i,T}=\sum_{j=1}^T sin(t_j) X_{T,i}(t_j)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e1d0472e03c7a087bbcb95b41cd09c61_l3.png "Rendered by QuickLaTeX.com").

## 1.2 Implementation in Spark

Our implementation is based on the FPCA Algorithm presented in [this post](https://www.thebigdatablog.com/functional-principal-component-analysis-with-spark/). We use the estimated first ![L](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66a9f474fc3c52efdfb0ba6a70199ee8_l3.png "Rendered by QuickLaTeX.com") eigenfunctions ![\hat{\gamma}_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e68dd4694afe1087769751f5cfd7245f_l3.png "Rendered by QuickLaTeX.com") and corresponding eigenvalues ![\hat{\lambda}_j \; j=1,\dots,L](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b5978b33eb60865feddce7e975b501fe_l3.png "Rendered by QuickLaTeX.com") to construct an estimator based on [5](#id4027515020) for ![\beta(t)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5f929b00e0212707fe88d8d83988c33e_l3.png "Rendered by QuickLaTeX.com") for ![k=1,\dots,T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-031e0916438ea7db50959676acecfab9_l3.png "Rendered by QuickLaTeX.com") with

     ![\[\hat{\beta}(t_k)= \frac{1}{T} \sum_{j=1}^T \sum_{i=1}^L \hat{\lambda}_i^{-1} \hat{\gamma}_i(t_k) \hat{\gamma}_i(s_j) g(s_j).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e7c97f649744cd93931e928fadf6475e_l3.png "Rendered by QuickLaTeX.com")

```
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

def spark_FReg( Xmatrix ,Ymatrix , L):
    fpca=spark_FPCA( Xmatrix , L)
    T = matrix.numCols()
    components=fpca[0]
    s=fpca[3]*fpca[3]
    #reconstruct beta
    Si=DenseMatrix( L,L, diag(1./(s*T)).flatten().flatten().tolist() )
    beta_est=Ymatrix.transpose().multiply( Xmatrix ).multiply(components).toIndexedRowMatrix().multiply(Si).toBlockMatrix().multiply(components.transpose())
    return (beta_est)

##EXAMPLE
T=5000
N=800

#define beta(t), the score function
time=2*pi*true_divide(arange(0,T),T )
beta= sin( time)
#betamat=DenseMatrix( T,N, np.repeat(beta,N) )
betamat=DenseMatrix( T,1, beta )
scaleMat=DenseMatrix( T,T, diag(1/T).flatten().flatten().tolist() )

#plt.plot(time,beta)
#plt.show()

data = list();
for i in range(0, N):
	data.append( IndexedRow(i, array( cumsum(random.normal(0,sqrt(true_divide(1,T)),T)) ) ) )

#convert the data to spark
sc_data= sc.parallelize( data )
matrix = IndexedRowMatrix(sc_data).toBlockMatrix().cache()

scale=CoordinateMatrix(sc.range(N).map(lambda i: MatrixEntry(i, i, 1./T)), N, N).toBlockMatrix()
Ymatrix=scale.multiply(IndexedRowMatrix(sc_data).multiply(betamat).toBlockMatrix()).cache()

##Plot the Input data
#plt.plot( Ymatrix.toLocalMatrix().toArray().flatten() )
#plt.show()

#reconstruct beta
beta_est=spark_FReg(matrix, Ymatrix, 12).toLocalMatrix()

times=true_divide( arange(0,T),T )
plt.plot(times, beta_est.toArray().flatten())

plt.plot(times,beta )
plt.show()
```
```