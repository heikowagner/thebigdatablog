---
categories:
- All Articles
- Fundamentals
date: '2017-01-22'
slug: fourier-transform
status: publish
tags: []
title: Fourier Transform
wp_id: 654
wp_modified: '2026-06-11T18:46:29'
---

## 1. The Fourier Transform

The Fourier transform ![\tilde{f}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8fe6551fcad8dbed6517f9c2ae95dde4_l3.png "Rendered by QuickLaTeX.com") of an integrable function ![f: \mathbb{R}^g \rightarrow \mathbb{C}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-50d5d53b521feb85791c160f00e31be3_l3.png "Rendered by QuickLaTeX.com") with ![s \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8c49b4e64f6cbd201d00c010ac0beb1d_l3.png "Rendered by QuickLaTeX.com") is given by\

(1)    ![\begin{equation*} \tilde{f}(s) = \int_{\mathbb{R}^g} f(x) exp(-2\pi i <x,s>) dx. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-696f3474ad63ff11c548c5a3003b2b76_l3.png "Rendered by QuickLaTeX.com")

Under suitable conditions, the inverse transform from ![\tilde{f}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8fe6551fcad8dbed6517f9c2ae95dde4_l3.png "Rendered by QuickLaTeX.com") to ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com") with ![t \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9058333516e99e10fd782d5557b71286_l3.png "Rendered by QuickLaTeX.com") is then given by\

(2)    ![\begin{equation*} f(t) = \int_{\mathbb{R}^g} \tilde{f}(x) exp(-2\pi i <s,x>) ds. \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-864d6e1a6b12017252515f4d9d2a712d_l3.png "Rendered by QuickLaTeX.com")

The Fourier transform has some nice properties. Assume ![f (x), g(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-359b74384467f4f6d8bce6a52ea2efe8_l3.png "Rendered by QuickLaTeX.com") and ![h(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-81577696f96e5719353992c5632a834c_l3.png "Rendered by QuickLaTeX.com") are integrable functions:

1. *Linearity*: For ![a,b \in \mathbb{C}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c6c11fab4dca5a69ad4425b4ae32213e_l3.png "Rendered by QuickLaTeX.com"), if ![f(x)= a h(x) + b g (x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2adabfa10c5c71fbfeeecfa28b2e9d72_l3.png "Rendered by QuickLaTeX.com"), then ![\tilde{f}(s)= a \tilde{h}(s) + b \tilde{g}(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a8f9873d7286d2fcfbcd583beb5fca27_l3.png "Rendered by QuickLaTeX.com").
2. *Translation:* For ![x_0 \in \mathbb{R}^n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-86db4d4455f9a6cfa8b1e438b9fbaf9f_l3.png "Rendered by QuickLaTeX.com"), if ![f(x)=h(x-x_0)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-15f2c5b0ba35ebf9dc71a0103253e6c9_l3.png "Rendered by QuickLaTeX.com"), then ![\tilde{f}(s) = exp(-2\pi i <x_0,s>) \tilde{h}(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e5d38877fe1fcadccc7c13665e04c785_l3.png "Rendered by QuickLaTeX.com").
3. *Modulation:* For ![s_0 \in \mathbb{R}^n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-10e4e2b76aa24b588688e9d6163384f4_l3.png "Rendered by QuickLaTeX.com"), if ![f(x)=exp(-2\pi i <x,s>)  h(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e4d68bb0b53315edceae3967c0cce42b_l3.png "Rendered by QuickLaTeX.com"), then ![\tilde{f}(s) = \tilde{h}(s-s_0)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5a4724f74435bd12eac966042dfbf174_l3.png "Rendered by QuickLaTeX.com").
4. *Scaling:* For ![a\neq 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c71874e5c357b79f6228b364e6bbd57d_l3.png "Rendered by QuickLaTeX.com"), if ![f(x)=h(a x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-76df9b4dcba0570680eff7907f066698_l3.png "Rendered by QuickLaTeX.com"), then ![\tilde{f}(s)=\frac{1}{|\prod_{i=1}^g a_i|} \tilde{h}(a^{-1} s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-42521113733ab7b7cb08c0f2dbedc51f_l3.png "Rendered by QuickLaTeX.com").*\*

Here we use the notation is used ![a \in \mathbb{R}^g, a^{-1} := (a_1^{-1},\dots a_g^{-1})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4db485a3218fd6d1bb70025e44a57b4f_l3.png "Rendered by QuickLaTeX.com").

An important feature of the Fourier Transform is convolution. Suppose two given functions ![f](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9c09a708375fde2676da319bcdfe8b24_l3.png "Rendered by QuickLaTeX.com") and ![g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d208fd391fa57c168dc0f151de829fee_l3.png "Rendered by QuickLaTeX.com") and let the convolution be defined as ![(f *g)(z) = \int_{\mathbb{R}^g} f(x) g(z-x)dx](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-20e0efe9f6e03de56b69ed884d3cadd3_l3.png "Rendered by QuickLaTeX.com"), then ![\widetilde{f*g} = \tilde{f} \cdot \tilde{g}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-91fc0aed2d343a7e32c5f61ea9dea54c_l3.png "Rendered by QuickLaTeX.com") and ![\widetilde{f \cdot g} = \tilde{f} * \tilde{g}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3a90c1baa09faf2397a5cd93617f5811_l3.png "Rendered by QuickLaTeX.com").

## 2. Discrete Fourier Transform

The discrete Fourier Transform (DFT) is based on points ![f_1, \dots, f_n, \; f_i \in \mathbb{C}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9692184035c2ee98e8ae4eb26d33d8f_l3.png "Rendered by QuickLaTeX.com") and given by\

(3)    ![\begin{equation*} \tilde{f}_k = \sum_{l=1}^n f_l exp(-2 \pi i k l) \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4cda615b5c3bae21d76d5211d41a97ee_l3.png "Rendered by QuickLaTeX.com")

and the inverse by\

(4)    ![\begin{equation*} f_i = \sum_{k=1}^n \tilde{f}_k exp(-2 \pi i n k). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9434e539d2b1895fc778a9b2116a9856_l3.png "Rendered by QuickLaTeX.com")

The DFT can be interpet as a discrete version of [1](#id1179122756). To see this, let ![x_1, \dots, x_T, \; x_i \in \mathbb{R}^g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-21c8231282817d72b200024688decd1e_l3.png "Rendered by QuickLaTeX.com") be some grid. Then a discrete, approximate version of ([1](#id1179122756)) is given by\

(5)    ![\begin{equation*} \tilde{f}(x_k) =\frac{1}{T} \sum_{l=1}^T f(x_l) exp(-2 \pi i x_l x_k). \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-63b3b5f452d13fac7b18d4fe3eb9c97d_l3.png "Rendered by QuickLaTeX.com")

If ![x_1, \dots, x_T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d33f57429f699f4c508698795dc23c20_l3.png "Rendered by QuickLaTeX.com") are g-dimensional equidistantly spaced then ([5](#id1663785787)) will be the Riemann sum while for g-dimensional i.i.d. random observations one may interpret ([5](#id1663785787))  as an monte carlo intergral.

Looking at ([1](#id1179122756)) with integration by substitution with ![x=\frac{1}{T} u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7fa07b36988b9a869f30ce77345ee415_l3.png "Rendered by QuickLaTeX.com"). Assume now observations at an equidistant univariate grid on ![[0,1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25b6d943ab489c05a3dbd5ea29087a48_l3.png "Rendered by QuickLaTeX.com"), ![x_i=\frac{i}{T}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ab7db89bd456ef079c41508caf061d25_l3.png "Rendered by QuickLaTeX.com"), and define ![T f_i \equiv T f(i)=T f(u_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f7e112783cc398a6c3af750ec2fc9fe4_l3.png "Rendered by QuickLaTeX.com") and ![i=u_i=T x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fc18b74ecdc56a0aeafe32988e1d25d0_l3.png "Rendered by QuickLaTeX.com"), then ([5](#id1663785787)) corresponds to ([4](#id1721451678)).