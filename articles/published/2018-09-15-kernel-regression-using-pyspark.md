---
categories:
- All Articles
- Coding
- Functional Data Analysis with Spark
- Projects
- Python
- Spark
date: '2018-09-15'
slug: kernel-regression-using-pyspark
status: publish
tags: []
title: Kernel Regression using Pyspark
wp_id: 1374
wp_modified: '2023-10-01T10:12:17'
---

## 1. Kernel Regression using Pyspark

[![](https://www.thebigdatablog.com/wp-content/uploads/2018/09/Download-2-300x200.png)](https://www.thebigdatablog.com/wp-content/uploads/2018/09/Download-2.png)

The red curve shows the true function m(x) while the green dots show the estimated curve evaluated using an random grid. The blue points are the simulated ![Y_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1ce9a015a804a13965be499e5d05726c_l3.png "Rendered by QuickLaTeX.com"). A well known problem of the estimation method concerning boundary points is clearly visible.

In a previous [article](https://www.thebigdatablog.com/nonparametric-density-estimation-using-spark/) I presented an implementation of a kernel denisty estimation using pyspark. It is thus not difficult to modify the algorithm to estimate a kernel regression. Suppose that there exits some function ![m(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0e924afd014df9ad4d7373d0d836552_l3.png "Rendered by QuickLaTeX.com"), an example for such functions are for instance temperature curves which measure the temperature during a day. In practice, such functions ![m(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0e924afd014df9ad4d7373d0d836552_l3.png "Rendered by QuickLaTeX.com") will often not be directly observed, but one will have to deal with discrete, noisy observations contaminated with some error. The purpose of kernel regression is then to estimate the underlying true function.

In the following I will only consider a simple, standard error model: For ![T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9ed275b0bf1633b7ee83b78fcc28273_l3.png "Rendered by QuickLaTeX.com") design points\
![X_1,\dots,X_T\in [0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-38196254294e29449b28cf816b50a776_l3.png "Rendered by QuickLaTeX.com") there are noisy observations ![Y_{l}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b8213a43a24661fc1a92daf115878bb_l3.png "Rendered by QuickLaTeX.com") such that

(1)    ![\begin{eqnarray*} Y_{l}=m(X_l)+\epsilon_{l},\quad l=1,\dots,T, \end{eqnarray*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a2171ac8a2e66cb98a5ff6139c0c9e71_l3.png "Rendered by QuickLaTeX.com")

for i.i.d. zero mean error terms ![\epsilon_{l}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9fd0301934bd0ab874bb444829414f38_l3.png "Rendered by QuickLaTeX.com") with finite variance ![\sigma^2>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-abf779e4971f6af7bc215b9594cb81fe_l3.png "Rendered by QuickLaTeX.com") and ![\mathbb{E}(\epsilon_{l}^4)<\infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-51d6903e877be5d6b5c3e51aae205cd3_l3.png "Rendered by QuickLaTeX.com").

To estimate ![m(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0e924afd014df9ad4d7373d0d836552_l3.png "Rendered by QuickLaTeX.com") I stick to the Nadaraya-Watson-Estimator given by

     ![\[\hat{m}(x) = \frac{\sum_{i=1}^T Y_i K_h(x-X_i) }{\sum_{i=1}^T K_h(x-X_i) }\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6803f42b1fad36ea641461f87475ad13_l3.png "Rendered by QuickLaTeX.com")

where ![K_h(u)=h^{-1}K(u/h)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-96b896e9c965ff1594e096761d65912f_l3.png "Rendered by QuickLaTeX.com") is a kernel as described [here](https://www.thebigdatablog.com/kernel-based-estimators-for-multivariate-densities-and-functions/), in the implementation again an Epanechnikov kernel ![K(u)=max(0,\frac{3}{4}(1-u^2))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bb0910cc4f8273f0cfd6452416ab2248_l3.png "Rendered by QuickLaTeX.com") is used. The reader might recognize that ![\sum_{i=1}^T K_h(x-X_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fc4e11e65a7b275abdcea4b950fead28_l3.png "Rendered by QuickLaTeX.com") is just the density (scaled by ![T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9ed275b0bf1633b7ee83b78fcc28273_l3.png "Rendered by QuickLaTeX.com")) already implemented [here](https://www.thebigdatablog.com/nonparametric-density-estimation-using-spark/), while ![\sum_{i=1}^T Y_i K_h(x-X_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5d5385a919b0df4c2e18e270e002a387_l3.png "Rendered by QuickLaTeX.com") is just a weighted version of it. Implementation should therefore be very similar leading to the following algortihm:

```
###A Spark-Function to derive a non-parametric kernel regression
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import StandardScaler
import matplotlib.pyplot as plt
from numpy import *

##1.0 Simulated Data
T=1500

time=sort( random.uniform(0,1,T) )   ##Sorting is not required, i did it to have less trouble with the plots
true = sin( true_divide( time, 0.05*pi)  )
X= true + random.normal(0,0.1,T)

data= sc.parallelize(  zip(time,X)  )

plt.plot(time,true, 'bo')
plt.plot(time,X, 'bo')
plt.show()

##2.0 The Function
#2.1 Kernel Function

def spark_regression(data, Nout, bw):
    def epan_kernel(x,y,b):
        u=true_divide( (x-y), b)
        return max(0, true_divide( 1, b)*true_divide(3,4)*(1-u**2))     

    #derive the minia and maxi used for interpolation
    mini=data.map(lambda x: x[0]).takeOrdered(1, lambda x: x )
    maxi=data.map(lambda x: x[0]).takeOrdered(1, lambda x: -1*x )
    #create an interpolation grid (in fact this time it's random)
    random_grid = sc.parallelize(  random.uniform(maxi,mini,Nout)  )
    #compute K(x-xi) Matrix
    density=data.cartesian(random_grid).map(lambda x:( float(x[1]),epan_kernel(array(x[0][0]),array(x[1]),bw) ) )
    kernl=data.cartesian(random_grid).map(lambda x:( float(x[1]),x[0][1]*epan_kernel(array(x[0][0]),array(x[1]),bw) ) )

    mx= kernl.filter(lambda x: x&amp;gt;0).reduceByKey( lambda y, x:  y+x ).zip( density.filter(lambda x: x&amp;gt;0).reduceByKey( lambda y, x:  y+x ) )  ##added optional filter() does anyone know if this improves performance?
    return mx.map(lambda x: (x[0][0],true_divide(x[0][1],x[1][1]))  )

##3.0 Results

fitted= spark_regression(data, 128, 0.05).collect()
fit=array(fitted).transpose()

plt.plot(time,true, color='r')
plt.plot(fit[0], fit[1], 'bo')

plt.show()
```