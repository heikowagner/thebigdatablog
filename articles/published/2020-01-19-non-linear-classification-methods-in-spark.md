---
categories:
- All Articles
- Coding
- Fundamentals
- Python
- Spark
date: '2020-01-19'
slug: non-linear-classification-methods-in-spark
status: publish
tags: []
title: Non-Linear Classification Methods in Spark
wp_id: 1942
wp_modified: '2023-10-01T10:11:43'
---

In a [previous post](https://www.thebigdatablog.com/non-linear-support-vector-machines-svm-in-spark/) I covered how to apply classical linear estimators like support vector machines or logistic regression to a non-linear dataset using the kernel method. This article can be considered as a second part. While the previous article concerns about the theoretical foundation this article is about implementation issues and examples.

## 1. Model fitting

Again consider multivariate data given by a pair ![(y,x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-57b6e6ee680857c53c52b227b4b67ad1_l3.png "Rendered by QuickLaTeX.com") where the explanatory variable ![x \in \mathbb{R}^p](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6baf5012ca650182746df3586c28b0cc_l3.png "Rendered by QuickLaTeX.com") and the group coding ![y \in \{-1,1\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-58a8e9ed4c534a8de9435be90c24a5b5_l3.png "Rendered by QuickLaTeX.com"). In the following we assume an iid. sample of size ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") given by ![(y_1,x_1),\dots,(y_N,x_N)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c9ab60a9220e8311c70b5c809278931f_l3.png "Rendered by QuickLaTeX.com"). Starting where the [previous post](https://www.thebigdatablog.com/non-linear-support-vector-machines-svm-in-spark/) ends our aim is to minimize \

(1)    ![\begin{equation*} min_\mathbf{\alpha} L(\mathbf{y}, \mathbf{K}  \mathbf{\alpha}) + \lambda  \mathbf{\alpha}^T \mathbf{K}  \mathbf{\alpha}. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a60196533a763d072a22b54e81e0f823_l3.png "Rendered by QuickLaTeX.com")

\
here ![\mathbf{y}=(y_1,\dots,y_N),\; \mathbf{\alpha}=(\alpha_1,\dots,\alpha_N)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fbff94eb6c236359a8dde0c7cc5b0440_l3.png "Rendered by QuickLaTeX.com") and ![\lambda](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2b5c45836864531b8e37025dabadd24a_l3.png "Rendered by QuickLaTeX.com") is a certain penalty term. ![\mathbf{K}_{ij} = K(x_i,x_j),\;i,j=1,\dots,N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-717b057f876b3791eaace68c09f896b4_l3.png "Rendered by QuickLaTeX.com") is a ![N \times N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4baf35605d041d4b70147e126302e8a7_l3.png "Rendered by QuickLaTeX.com") Matrix derived from a kernel function, a kernel can be understood as a function that measures a certain relation between ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") and ![x_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43ac7b8c02ebbeedbdb09ce539a0abb9_l3.png "Rendered by QuickLaTeX.com") (e.g. spacial location). An important role is played by the choice of ![L](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66a9f474fc3c52efdfb0ba6a70199ee8_l3.png "Rendered by QuickLaTeX.com"), it determines which method (eg. SVM, logit) is used. In general the problem lacks of an closed form solution, therefore we approximate the solution using the Newton-Raphson algorithm.

## 2. Newton-Raphson algorithm

For a given loss function ![L( \mathbf{y},    \mathbf{K}  \mathbf{\alpha}  )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-be6ac6997176584a70e7732dbd7dd6d5_l3.png "Rendered by QuickLaTeX.com") let the gradient error function be given by ![\nabla  E(\alpha) = \frac{\partial L( \mathbf{y},    \mathbf{K}  \mathbf{\alpha} )+  \mathbf{\alpha}^T \mathbf{K}  \mathbf{\alpha}    }{\partial  \alpha}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-283572bea1562ae2004061e70281ef84_l3.png "Rendered by QuickLaTeX.com") and the Hessian ![H (\alpha) =  \frac{\partial   L( \mathbf{y},    \mathbf{K}  \mathbf{\alpha}  ) +\mathbf{\alpha}^T \mathbf{K}  \mathbf{\alpha}   }{\partial  \alpha^2}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f11d55aa6d9b4f4c2189c9b74f25f299_l3.png "Rendered by QuickLaTeX.com"). The Newton-Raphson algorithm is then to start with some initial estimate ![\alpha^{0}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2eac803336b90e4787f75aa8b08aa344_l3.png "Rendered by QuickLaTeX.com") and update ![\alpha^{(m+1)}= \alpha^{(m)} - H^{-1}   \nabla  E(  \alpha ^{(m)}   )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-963f9b51597d23c877cf4269462aa5dd_l3.png "Rendered by QuickLaTeX.com") until convergence.

### 2.1 Examples

#### 2.1.1 Ridge Regression

To construct a ridge regression using ![(1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-93d60e3fa59910a72184d3a64b54d6b7_l3.png "Rendered by QuickLaTeX.com") we have to choose the squared loss function ![L(y, x)= (y-x)^2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-810e0aebdae406a12d13b32ed8e2bfde_l3.png "Rendered by QuickLaTeX.com") and thus \

(2)    ![\begin{equation*} min_\mathbf{\alpha}(  \mathbf{y}  - \mathbf{K}  \mathbf{\alpha}  )^T  (  \mathbf{y}  - \mathbf{K}  \mathbf{\alpha}  ) + \lambda  \mathbf{\alpha}^T \mathbf{K}  \mathbf{\alpha} . \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-94cc72c83cdfa84a4a1755590bdf4785_l3.png "Rendered by QuickLaTeX.com")

\
using Newton-Raphson notice we get ![\nabla E(\alpha)= -2  \mathbf{K}^T  (    \mathbf{y}   - \mathbf{K}  \alpha  )  +  2 \lambda     \mathbf{K}  \alpha](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b9de57ae7ff450d559222608cfb78801_l3.png "Rendered by QuickLaTeX.com") and ![H=2 \mathbf{K} ^T \mathbf{K} +2\lambda  \mathbf{K}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-09747f1a43a91d0997b116ac7c5ca285_l3.png "Rendered by QuickLaTeX.com"). Starting with ![\mathbf{\alpha}^{(0)}=(0,\dots,0)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-81860ffde03fe6e507cc229631ea196f_l3.png "Rendered by QuickLaTeX.com")\

(3)    ![\begin{equation*}   \mathbf{\alpha}^{(1)} = \mathbf{\alpha}^{(0)}  - (    2 \mathbf{K} ^T \mathbf{K} +2\lambda  \mathbf{K}   )^{-1} (  -2  \mathbf{K}^T  (    \mathbf{y}   - \mathbf{K}  \alpha ^{(0)}   )  +  2 \lambda     \mathbf{K}  \alpha ^{(0)}    ) =  ( \mathbf{K}  + \lambda \mathbf{I})^{-1} \mathbf{y} . \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f4d0f77c6660e034866e03fdc1d5c9f5_l3.png "Rendered by QuickLaTeX.com")

\
 Indeed, for the Ridge Regression case we can derive also an optimal solution analytically by simple taking the derivatives ![\nabla E(\alpha)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-623bac71fad232566cc217d0def6e9ef_l3.png "Rendered by QuickLaTeX.com") and equating them to zero which gives the same solution as the Newton-Raphson algorithm in one step. Fitted values are thus given by ![\hat{\mathbf{y}}=\mathbf{K}  \mathbf{\alpha}^{(1)} = ( \mathbf{I}  + \lambda \mathbf{K}^{-1})^{-1} \mathbf{y}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-45a247f6480f7bebb1a79148a6f44b6e_l3.png "Rendered by QuickLaTeX.com").

#### 2.1.2 Logistic Regression

To construct a logistic regression ![L()](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-874b95ce6f14eacf2de3b9f018fcd9a2_l3.png "Rendered by QuickLaTeX.com") has to be chosen as ![L(y,x) =log(1 + exp(- yx  ) )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b4ea8a587180cac1800688d2c1b95203_l3.png "Rendered by QuickLaTeX.com"). This lacks of an closed form solution, therefore we approximate the solution using the Newton-Raphson algorithm. Recall that we aim to minimize\

     ![\[  min_\mathbf{\alpha} \sum_{i=1}^N log(1 + exp(- y_i   \mathbf{K}  \mathbf{\alpha}  ) )  + \lambda  \mathbf{\alpha}^T \mathbf{K}  \mathbf{\alpha} . \]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c4c62b5b45360e0531a7700df0c01c2f_l3.png "Rendered by QuickLaTeX.com")

\
Therefore ![\nabla E(\alpha)_{j}=- \sum_{i=1}^N \frac{exp( - y_i \mathbf{K}  \mathbf{\alpha}  ) y_i \mathbf{K}_{ij}}{1 +exp( -  y_i     \mathbf{K}  \mathbf{\alpha} ) } +  2 \lambda  \sum_{j=1}^N   \mathbf{K}_{ij}     \mathbf{\alpha}_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ba94a7276fa052ce9a3fc52d0ea39b3a_l3.png "Rendered by QuickLaTeX.com") and the Hessian is given by\

     ![\[H_{ij}= \frac{\partial  \nabla E(\alpha)_i  }{ \partial \alpha_j}  +2\lambda \mathbf{K}_{ij}\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a66764d25339db78b7baa0c281ddbcb5_l3.png "Rendered by QuickLaTeX.com")

.

### 2.1 Computation

A computational problem using Newton-Raphson is to derive the Hessian since ![N  \times N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c29c660422c7ea59ddcc5f18f2f93fff_l3.png "Rendered by QuickLaTeX.com") cells has to be computed. A commonly used strategy is thus to approximate the Hessian for example using ![H(\alpha^{(m)}) \approx \frac{  \nabla  E(  \alpha ^{(m)})  -   \nabla  E(  \alpha ^{(m-1)} ) }{ \alpha ^{(m)} - \alpha ^{(m-1) }}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d1f3b4067a6327e727792d336a16cda7_l3.png "Rendered by QuickLaTeX.com"). Such Methods are called [quasi-newton Methods](https://en.wikipedia.org/wiki/Quasi-Newton_method). The Spark implementation to derive an support vector machine fitting for example make use of the [L-BFGS](https://en.wikipedia.org/wiki/Limited-memory_BFGS) method. Logit and Ridge Regression fitting rely on [Stochastic gradient descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) which does not use the Hessian at all and even approximates the gradient error function.

## 3. Prediction

Suppose a given fitted model ![\alpha^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cbcc67088f2cef10e188b5f04bee3721_l3.png "Rendered by QuickLaTeX.com") fitted using a training set of pairs ![(y_1,x_1),\dots,(y_N,x_N)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c9ab60a9220e8311c70b5c809278931f_l3.png "Rendered by QuickLaTeX.com"). Consider another set of data ![x^{'}_1, \dots, x^{'}_{N^'}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-768e0df6d529980bfaa05030602a155e_l3.png "Rendered by QuickLaTeX.com") which is often called test sample. In order to to reach a decision to which group these variables belong we use ![\hat{y}^{'}_j=\sum_i K(x_i, x^{'}_j) \alpha^{*}_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-215a71010efe05b81b085ef001168b22_l3.png "Rendered by QuickLaTeX.com"). This also gives a intuitive explanation how the prediction using the kernel method works. If observed test data ![x^{'}_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-79a5edb8e9468bf91daea2db132fe13d_l3.png "Rendered by QuickLaTeX.com") is close, in the kernel sense, to the training data ![x_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-01a7b7b5dca66cb33a1207e1f39c1140_l3.png "Rendered by QuickLaTeX.com") than these two observations likely belong to the same group.

## 4. Implementation

![](https://www.thebigdatablog.com/wp-content/uploads/2020/01/simulation.png)

Simulated 200 random samples using the described model.

The procedure is implemented in pySpark using the spark functions *SVMWithSGD, LogisticRegressionWithLBFGS, LinearRegressionWithSGD*. For curiosity also a Lasso implementation using *LassoWithSGD* was done, actually the model does not fit to the ones described above, because the error term looks different (L1 error norm). However using Lasso in the kernel context has an interesting effect, since lasso will not discard certain features but certain observations. To test the implementation train and test data is simulated using the following model: ![y \sim B(1, 0.5)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-aaf1437705659dab5081db03ba6276ca_l3.png "Rendered by QuickLaTeX.com") and with ![\phi  \sim \mathcal{N}(0,2\pi)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-24b8be3241e53082db5ddf5b63333d8a_l3.png "Rendered by QuickLaTeX.com"), ![x=  (0.5 (1 + y)  cos( \phi ) + \epsilon, 0.5 (1 + y )sin( \phi ) + \epsilon')](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-39a0a79b12b3f5b9bc3a64616c3775e1_l3.png "Rendered by QuickLaTeX.com") where ![\epsilon, \epsilon' \sim \mathcal{N}(0,0.1)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3a59988bd16596900b614fcf0bb1e41b_l3.png "Rendered by QuickLaTeX.com"). The whole simulation is a bit long therefore it is available as a zeppelin notebook [via github](https://github.com/heikowagner/thebigdatablog/blob/master/docker/zeppelin/notebook/2EYYQ9E77/note.json). For those who have no access to a zeppelin installation there exsits also a [docker-compose setup](https://github.com/heikowagner/thebigdatablog/tree/master/docker/zeppelin) including the notebook. As an example the code for the logit method is given above, for other linear methods the procedure is comparable.

```
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

def radial_kernel(x,y,sigma):
    return np.exp(-sum((x-y)**2)/(2*sigma**2))


def construct_K(Y,X,X_1,lamb):
    sp_X=sc.parallelize(np.transpose(X)).zipWithIndex()
    sp_X_1=sc.parallelize(np.transpose(X_1)).zipWithIndex()
    sp_Y=sc.parallelize(Y).zipWithIndex().map(lambda(x,y) : (y,x) )
    grid=sp_X.cartesian(sp_X_1)
    K=grid.map(lambda(x,y) : (x[1],radial_kernel(x[0],y[0],lamb)) )
    return [sp_Y, K]
    
def construct_labeled(Y,K):
    def add_element(acc,x):
        if type(acc[1]) == list:
            return (min(acc[0],x[0]), acc[1] + [x[1]]  )
        else:
            return (min(acc[0],x[0]), [acc[1]] + [x[1]]  )
    jnd=Y.join(K).reduceByKey(lambda acc, x : add_element(acc,x) )
    labeled=jnd.map(lambda(y,x) : LabeledPoint(x[0], x[1])  )
    order=jnd.map(lambda (y,x): y)
    return [labeled, order]

##Simualte the training sample
N=500
Y= np.random.randint(0,2,N)
degree=np.random.normal(0,1,N)*2*np.pi
X= [0+ (0.5 + Y*0.5)* np.cos(degree)+ np.random.normal(0,2,N)*0.05, 0 + (0.5 + Y*0.5)*np.sin(degree)+ np.random.normal(0,2,N)*0.05   ]

plt.scatter(X[0], X[1], c=Y)
plt.show()

#Example Logistic Regression

from pyspark.mllib.regression import LabeledPoint

Y_K=construct_K(Y,X,X,0.1)
l_train=construct_labeled(Y_K[0], Y_K[1])[0]


# Evaluating the model on training data
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel

LogitModel = LogisticRegressionWithLBFGS.train(l_train)
labelsAndPreds = l_train.map(lambda p: (p.label, LogitModel.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda lp: lp[0] != lp[1]).count() / float(l_train.count())
print("Training Error = " + str(trainErr))

#Construct Test Sample and apply the model
##Generate data
#Simulation
N=200

Y_test=np.random.randint(0,2,N)
degree=np.random.normal(0,1,N)*2*np.pi
X_test=[0+ (0.5 + Y_test*0.5)* np.cos(degree)+ np.random.normal(0,2,N)*0.05, 0 + (0.5 + Y_test*0.5)*np.sin(degree)+ np.random.normal(0,2,N)*0.05]

#plot data
plt.scatter(X_test[0], X_test[1], c=Y_test)
plt.show()

Y_K_test=construct_K(Y_test,X_test,X,0.1)
l_test=construct_labeled(Y_K_test[0], Y_K_test[1])

##Logit
labelsAndPreds = l_test[0].map(lambda p: (p.label, LogitModel.predict(p.features)))
testErr = labelsAndPreds.filter(lambda lp: lp[0] != lp[1]).count() / float(l_train.count())
print("Prediction Error (Logit)= " + str(testErr))

#plot predictions
preds=labelsAndPreds.map(lambda lp: lp[1]).collect()
sort_order=l_test[1].collect()
pred_sorted = [x for _,x in sorted(zip(sort_order,preds))]

plt.scatter(X_test[0], X_test[1], c=pred_sorted)
plt.show()
```