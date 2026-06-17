---
categories:
- All Articles
- Coding
- Functional Data Analysis with Spark
- Python
- Spark
date: '2018-08-29'
slug: nonparametric-density-estimation-using-spark
status: publish
tags: []
title: Nonparametric Density estimation using Spark
wp_id: 1359
wp_modified: '2026-06-11T18:47:23'
---

## 1. A Nonparametric Density implementation in Spark

[![](https://www.thebigdatablog.com/wp-content/uploads/2018/08/Download-300x200.png)](https://www.thebigdatablog.com/wp-content/uploads/2018/08/Download.png)

The red curve shows the true density while the blue dots show the estimated density evaluated using an equidistant grid.

One of my previous [blog post](https://www.thebigdatablog.com/kernel-based-estimators-for-multivariate-densities-and-functions/) concerns about nonparametric density estimation. In this post i presented some Matlab code. An advantage of this Spark implementation is that the estimation is totally parallel since we only use build-in Spark procedures. Let ![X_1,\dots, X_N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-977313cb2a8fe7a57d9548785c0535a3_l3.png "Rendered by QuickLaTeX.com") be a random sample drawn from some distribution with an unknown density ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com"). The key is to use *data.cartesian(random\_grid)* which creates pairs ![\{ (x_j,X_i) \}_{i=1,\dots,N ; j=1,\dots T}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-aad9f8fbf55f9f78a052b58334dae805_l3.png "Rendered by QuickLaTeX.com") where ![x_1, \dots, x_T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d33f57429f699f4c508698795dc23c20_l3.png "Rendered by QuickLaTeX.com") is a predefined grid. Then using *map* together with an Epanechnikov kernel ![K(u)=max(0,\frac{3}{4}(1-u^2))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bb0910cc4f8273f0cfd6452416ab2248_l3.png "Rendered by QuickLaTeX.com") we get ![K_h(x_j-X_i)=h^{-1}K((x_j-X_i)/h)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-90439524a398a0ef30661d0779626302_l3.png "Rendered by QuickLaTeX.com"). The final ![\hat{f}_h(x_j)= \frac{1}{N} \sum_{i=1}^N K_h(x_j-X_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e9720da5518696895b3265c585301ee2_l3.png "Rendered by QuickLaTeX.com") is then evaluated using *reduceByKey*.

```

###A Spark-Function to derive a non-parametric kernel density

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import StandardScaler
import matplotlib.pyplot as plt
from numpy import *

##1.0 Simulated Data
N=15000
mu, sigma = 2, 3 # mean and standard deviation
rdd = sc.parallelize( random.normal(mu,sigma,N) )

##2.0 The Function
#2.1 Kernel Function

def spark_density(data, Nout, bw):
    def epan_kernel(x,y,b):
        u=true_divide( (x-y), b)
        return max(0, true_divide( 1, b)*true_divide(3,4)*(1-u**2))     

    #derive the minia and maxi used for interpolation
    mini=data.takeOrdered(1, lambda x: x )
    maxi=data.takeOrdered(1, lambda x: -1*x )
    #create an interpolation grid (in fact NOT random this time)
    random_grid = sc.parallelize( linspace(mini, maxi, num=Nout)   )
    Nin=data.count()
    #compute K(x-xi) Matrix
    kernl=data.cartesian(random_grid).map(lambda x:( float(x[1]),true_divide(epan_kernel(array(x[0]),array(x[1]),bw),Nin) ) )
    #sum up 
    return kernl.reduceByKey( lambda y, x:  y+x )

##3.0 Results

density= spark_density(rdd, 128, 0.8).collect()
dens=array(density).transpose()

anzahl=array(anz).transpose()
#Plot the estimate
plt.plot(dens[0], dens[1], 'bo')

axis2=linspace(-10, 10, num=128)
#plot the true density
plt.plot(axis2, 1/(sigma * sqrt(2 * pi)) *exp( - (axis2 - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
plt.show()
```