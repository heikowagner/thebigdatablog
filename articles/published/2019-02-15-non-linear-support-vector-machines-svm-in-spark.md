---
categories:
- All Articles
- Coding
- Fundamentals
- Python
- Spark
date: '2019-02-15'
slug: non-linear-support-vector-machines-svm-in-spark
status: publish
tags: []
title: Non-Linear Support Vector Machines (SVM)
wp_id: 1274
wp_modified: '2023-10-01T10:12:11'
---

# 1. Introduction

![](https://www.thebigdatablog.com/wp-content/uploads/2018/04/Rplot01-300x300.png)

**Figure 1:** The figure show three lines separating the black and the green group.

This blog post is about Support Vector Machines (SVM), but not only about SVMs. SVMs belong to the class of classification algorithms and are used to separate one or more groups. In it’s pure form an SVM is a linear separator, meaning that SVMs can only separate groups using a a straight line. However ANY linear classifier can be transformed to a nonlinear classifier and SVMs are excellent to explain how this can be done. For a deeper introduction to the topic I recommend [Tibshirani (2009)](https://www.amazon.com/Elements-Statistical-Learning-Prediction-Statistics/dp/0387848576), one can find a more detailed description including an derivation of the complete lagrangian there.

The general Idea of SVM is to separate two (or more) groups using a straight line (see Figure 1). However, in general there exits infinitely many lines that fulfill the task. So which one is the “correct” one? The SVM answers this question by choosing the line (or hyperplane if we suppose more than two features) which is most far away (the distance is denoted by ![\zeta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-972238cb0edae352c280a54fc315146f_l3.png "Rendered by QuickLaTeX.com")) from the nearest points within each group.

# 2. Mathematical Formulation

## 2.1 Separating Hyperplanes

Suppose multivariate data given by a pair ![(y,x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-57b6e6ee680857c53c52b227b4b67ad1_l3.png "Rendered by QuickLaTeX.com") where the explanatory variable ![x \in \mathbb{R}^p](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6baf5012ca650182746df3586c28b0cc_l3.png "Rendered by QuickLaTeX.com") and the group coding ![y \in \{-1,1\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-58a8e9ed4c534a8de9435be90c24a5b5_l3.png "Rendered by QuickLaTeX.com"). In the following we assume an iid. sample of size ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") given by ![(y_1,x_1),\dots,(y_N,x_N)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c9ab60a9220e8311c70b5c809278931f_l3.png "Rendered by QuickLaTeX.com").\
Any separating hyperplane (which is a line if ![p=2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-36cf66ae876ab93b38b965cbe720697e_l3.png "Rendered by QuickLaTeX.com")) can therefore be described such that there exits some ![\beta\in \mathbb{R}^p](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1ec91cb4cffb894ca8ab0e543cb7bd19_l3.png "Rendered by QuickLaTeX.com") and

(1)    ![\begin{equation*} y_i(x_i^T \beta + \beta_0) \geq \zeta >0, \; \forall i=1,\dots,N. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4a824b54e1e09764301cbd8826c295aa_l3.png "Rendered by QuickLaTeX.com")

Note that with the (non restrictive) condition that ![||\beta||=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d20c36e27f791ec0088291239db3ebd9_l3.png "Rendered by QuickLaTeX.com"). Our task to separate the groups is covered by the minimization problem

(2)    ![\begin{equation*} min_{\beta,\beta_0} ||\beta|| \; s.t. \; y_i(x_i^T \beta + \beta_0) >1, \; i=1,\dots,N. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8b41953da2d831bc112181c9b971167d_l3.png "Rendered by QuickLaTeX.com")

# 2.2 Support Vector Machines

In most cases the assumption that there exits a hyperplane that perfectly parts the data points is unrealistic. Usually some points will lie on the other side of the hyperplane. In that case ([2](#id1616987450)) will not have a solution. The idea of SVM is now to introduce an parameter ![\xi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d3dfe7e11233bac0a8bed6fb221f5460_l3.png "Rendered by QuickLaTeX.com") to fix this issue. In particular we modify ([1](#id2902895661)) such that we require\


(3)    ![\begin{equation*} y_i(x_i^T \beta + \beta_0) \geq \zeta(1 -\xi_i), \; \forall i \, \xi_i >0, \; \sum_{i=1}^N \xi_i < \infty.  \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4ba4585fec2392a2ccf9788dea78b689_l3.png "Rendered by QuickLaTeX.com")

The corresponding minimization problem is then given by

(4)    ![\begin{equation*}  min_{\beta,\beta_0} ||\beta|| \; s.t. \; y_i(x_i^T \beta + \beta_0) > 1 -\xi_i,\xi_i \geq 0 \; \forall i, \; \sum \xi_i \leq C < \infty  \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1807ab03af55ab8a82c8f90c9be5fb63_l3.png "Rendered by QuickLaTeX.com")

Both ([2](#id1616987450)) and ([3](#id3019913911)) are convex optimization problems and can be solved for example using the [Lagrange minimization technique](https://en.wikipedia.org/wiki/Lagrange_multiplier</a). A solution for ([4](#id1533103627)) always has the form

(5)    ![\begin{equation*}  \beta=\sum_{i=1}^N a_i y_i x_i  \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3dd5b1de9ae67fc512b83af9232b37d9_l3.png "Rendered by QuickLaTeX.com")

where ![a_i>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6087cfb220cdc3f06cce6de8e1e5c075_l3.png "Rendered by QuickLaTeX.com") iff ([3](#id3019913911)) is met with “![=](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b8690b7efd237bfe32a6e92e3b699b96_l3.png "Rendered by QuickLaTeX.com")” and ![a_i=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0c8b08d19b7e14b67166632f98ecb05a_l3.png "Rendered by QuickLaTeX.com") else, these ![a_i>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6087cfb220cdc3f06cce6de8e1e5c075_l3.png "Rendered by QuickLaTeX.com") are then called **support vectors**.

## 2.2 Nonlinear SVMs

[![](https://www.thebigdatablog.com/wp-content/uploads/2018/04/Rplot-300x300.png)](https://www.thebigdatablog.com/wp-content/uploads/2018/04/Rplot.png)

**Figure 2:** The figure shows an example of two groups which are not separating using a straight line.

The method we described so far can only handle data where the groups can be separate using some hyperplane (line). However in many cases the data to be considered is not suited to be separated using a linear method. See figure 2 for example, in figure 2 the groups are arranged in two circles with different radius. Any attempt to separate the groups using a line will thus fail. However any linear method can be transformed into a non-linear method by projecting the data ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com") into a higher dimensional space. This new data ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com") may then be separable by some linear method. In case of figure 2 a suitable projection is for example given by ![\phi(x)=(x_1,x_2, x_1^2 + x^2)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3233982a0330e6a69ba984037f9f1f66_l3.png "Rendered by QuickLaTeX.com"), ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com") maps the data onto a cone where the data can be separated using a hyperplane as to be seen in figure 3. However, there are some drawbacks using this method. First of all ![\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b2be26c0c1341f54b29baddda771346_l3.png "Rendered by QuickLaTeX.com") will in general be unknown. In our simple example we where lucky to find a suitable ![\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b2be26c0c1341f54b29baddda771346_l3.png "Rendered by QuickLaTeX.com"), however concerning a more complicated data structure fining a suitable ![\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b2be26c0c1341f54b29baddda771346_l3.png "Rendered by QuickLaTeX.com") turns out to be very hard. Secondly, depending on the dataset, the dimension of ![\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b2be26c0c1341f54b29baddda771346_l3.png "Rendered by QuickLaTeX.com") needed to guarantee the existence of a separating hyperplane can become quite large and even infinite. Before we deal with this issues using kernels we will first have a look at the modified minimization problem ([4](#id1533103627)) using ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com") instead of ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com").

Let the nonlinear solution function given by ![f(x)= \phi(x)^T \beta+\beta_0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f25bdcde9a8aed237de059e8b910840b_l3.png "Rendered by QuickLaTeX.com"). To overcome the need of the constant ![C](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f34f74d98915e33f37a086f8cbfb996a_l3.png "Rendered by QuickLaTeX.com") we introduce some penalty ![\lambda>0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1023239a03b85869a6e282ae89b16641_l3.png "Rendered by QuickLaTeX.com") and rewrite ([4](#id1533103627)) as\


(6)    ![\begin{equation*} min_{\beta_0,\beta} \sum_{i=1}^N [1- y_i f(x_i)]_+ \frac{\lambda}{2} ||\beta||^2. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-99b1993130122dfa07145254e63821dc_l3.png "Rendered by QuickLaTeX.com")

\
The notation ![[]_+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e70617edac1f804d04d89cd3fcb6802f_l3.png "Rendered by QuickLaTeX.com") means that only the positive part of ![[1- y f(x)]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fe55da2b2663a96b010ba3b76b78fb11_l3.png "Rendered by QuickLaTeX.com") is taken into account.
At this point I would like to establish the connection to other linear methods. Since we consider SVMs we set the Loss function to ![L(y,f)=[1- y f(x)]_+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-67043ff3e0e46b3f4d460abddf74480c_l3.png "Rendered by QuickLaTeX.com"). Different loss functions ![L(y,f)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-38074f2133601ddbc173ae61f24ca414_l3.png "Rendered by QuickLaTeX.com") will lead to different methods, for example using ![L(y,f)=log(1+exp(-yf(x)))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-73001928adc3d78c45eb868d13ee6177_l3.png "Rendered by QuickLaTeX.com") will correspond to the logistic regression. Therefore the following strategy can be used to extent linear methods to deliver non-linear solutions.

From ([5](#id2344066037)) we already know, that a nonlinear solution function ![f(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a7ee323bc5a3f73ad5e066b13bed5504_l3.png "Rendered by QuickLaTeX.com") will have the form\

(7)    ![\begin{equation*} f(x)=\sum_{i=1}^N a_i y_i \langle\phi(x),\phi(x_i)\rangle +\beta_0 \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-22767b03efeb818b928ac182a5cfef51_l3.png "Rendered by QuickLaTeX.com")

\
We can verify, that knowledge about ![\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b2be26c0c1341f54b29baddda771346_l3.png "Rendered by QuickLaTeX.com") is in fact not required to formulate the solution. We only need to know something about the inner product ![\langle\phi(x),\phi(x_i)\rangle](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-282d0bc2cae06097338583ea54b537bc_l3.png "Rendered by QuickLaTeX.com"). While ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com") could be a high dimensional complicated function, the inner product is just a number. So if we would have some magical procedure that gives us this number, solving Nonlinear SVM would be straightforward. This leads us to think about kernels.

### 2.2.1 Kernels

[![](https://www.thebigdatablog.com/wp-content/uploads/2018/04/animated.gif)](https://www.thebigdatablog.com/wp-content/uploads/2018/04/animated.gif)

**Figure 3:** The same example as above. Projection to a space using one addition dimension makes the groups again separable using a hyperplane.

We already get in touch with [kernels](/kernel-based-estimators-for-multivariate-densities-and-functions/) when estimating [densities](nonparametric-density-estimation-using-spark/) or a [regression](kernel-regression-using-pyspark/). In this application [Kernels](https://en.wikipedia.org/wiki/Positive-definite_kernel) are a way to reduce the infinite-dimensional problem to a finite dimensional optimization problem because the complexity of the optimization problem remains only dependent on the dimensionality of the input space and not of the feature space. To see this, let ![x,z \in \mathbb{R}^p](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ec8982d3ab8e56ad8c72bb2530204c0f_l3.png "Rendered by QuickLaTeX.com") instead of looking at some particular function ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com"), we consider the whole space of functions generated by the linear span of ![\{K(·,z), z \in \mathbb{R}^p)\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-585e277c07916386fbd47f1db3e8df1e_l3.png "Rendered by QuickLaTeX.com") where ![\phi(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-297ad55564e86009c790a69b7a55cea1_l3.png "Rendered by QuickLaTeX.com") is just one element in this space. To model this space in practice popular kernels are

- linear kernel: ![K(x,z)=\langle x,z\rangle](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ca5451784b61533e7c6fd95f126d368c_l3.png "Rendered by QuickLaTeX.com")
- polynomial kernel: ![K(x,z)=\langle x,z\rangle ^{{d}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f308e9265267906e997a93746b0279d4_l3.png "Rendered by QuickLaTeX.com")
- radial kernel: ![K(x,z)=\exp \left(-{\tfrac {||x-z||^{{2}}}{2\sigma ^{{2}}}}\right)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c506b51a34698be6c1fddf5d0905afba_l3.png "Rendered by QuickLaTeX.com")

used. Choosing a kernel that naturally fits the structure of the date is beneficial. In our example from figure 2, the radial kernel is a good choice.
Suppose that ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") has an eigen-expansion

(8)    ![\begin{equation*} K(x, z)= \sum_{j=1}^\infty \gamma_j \varphi_j(z) \varphi_j(x) \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f3eb57f7fc69cb526fdca161c7c657ef_l3.png "Rendered by QuickLaTeX.com")

where ![\varphi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-275e3ff85c541772575a0f466b91d2c4_l3.png "Rendered by QuickLaTeX.com") are the orthonormal eigenfunctions of ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") and eigenvalues ![\gamma_i\geq 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9c81297e297015954c4829c860c3d8b_l3.png "Rendered by QuickLaTeX.com"), ![\sum \gamma_i^2 < \infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e67a8ed4baf8b416a49a26edd988c784_l3.png "Rendered by QuickLaTeX.com") which ensure that that the generated space is a Hilbert space. Then ![\phi(x)= \sum_{j=1}^\infty \delta_j \varphi_j(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c4c2054eaaa8ffa624bb06fb104c005f_l3.png "Rendered by QuickLaTeX.com") for suitable ![\delta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-02c416d77f6650e9c7849397bf6e11bf_l3.png "Rendered by QuickLaTeX.com") and for some ![c_j=\sum_{i=1}^N \alpha_i \gamma_j \varphi_j(x_i) ,j=1,\dots,\infty](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e8da5c2ea646aed8234a9190ec75651e_l3.png "Rendered by QuickLaTeX.com") we can represent

(9)    ![\begin{equation*} f(x) = \sum_{j=1}^\infty c_j \varphi_j(x) =\sum_{i=1}^N \alpha_i K(x,x_i). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad8612dce46791de61a600da4275d172_l3.png "Rendered by QuickLaTeX.com")

\
Thus we can write ([6](#id3885407981)) in its general form as\


(10)    ![\begin{equation*} min_c_j \sum_{i=1}^N L(y_i, \sum_{j=1}^\infty c_j \varphi_j(x_i)) + \lambda \sum_{j=1}^\infty c_j^2/\gamma_j  \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-523f7afe6529bc957c5d6785572f62d9_l3.png "Rendered by QuickLaTeX.com")

\
According to ([9](#id622323472)) we can write down ([10](#id1770475734)) using matrix notation ![\mathbf{K}_{ij} = K(x_i,x_j),\;i,j=1,\dots,N \; \mathbf{y}=(y_1,\dots,y_N),\; \mathbf{\alpha}=(\alpha_1,\dots,\alpha_N)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0574bc59e02ac3f25704dcd8ccf52ce8_l3.png "Rendered by QuickLaTeX.com") as

(11)    ![\begin{equation*} min_\mathbf{\alpha} L(\mathbf{y}, \mathbf{K} \mathbf{\alpha}) + \lambda \mathbf{\alpha}^T \mathbf{K} \mathbf{\alpha}. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ef089891ed4ff87291abf33f74eabdbb_l3.png "Rendered by QuickLaTeX.com")

This finite dimensional problem can now be solved using standard methods.