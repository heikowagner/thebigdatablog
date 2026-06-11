---
categories:
- All Articles
- Passwords
- Projects
date: '2017-02-09'
slug: 1-thougts-about-passwords
status: publish
tags: []
title: 1. Thougts about Passwords
wp_id: 706
wp_modified: '2026-06-11T18:46:33'
---

## 1. Introduction

This Project is about making an educated guess to derive an unknown password based on hacked password lists (Google: “RockYou”). In this section we will introduce the mathematical framework to handle passwords and develop a simple brute force approach based on *very* unrealistic Assumptions. During this Project these Assumptions will then be weaken to  derive in the end a clever method to guess passwords.

### 1.1. Formulation

Let ![X \in \mathbb{X} \, ,X=x_1 x_2 x_3 \dots x_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-91e7a99d4236a049010d0b0734289f36_l3.png "Rendered by QuickLaTeX.com") be a password and the random variables ![x_i \in \mathbb{A}, E \in \mathbb{N}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-81c618a31cc1f5fe91ad7fd66a31224d_l3.png "Rendered by QuickLaTeX.com") the corresponding letters and password length. ![\mathbb{X}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0a912bd9abe1e6796446fdfedc0ca07c_l3.png "Rendered by QuickLaTeX.com") is the space of all passwords and ![\mathbb{A}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fdb36901bfeee1bb4b059305c252e86_l3.png "Rendered by QuickLaTeX.com") corresponds to the used alphabet, for example if we allow only for lower case letters then ![\mathbb{A} =\{a,b,c, \dots, y,z \}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b6ca4ae7b57a6cdb35d8c4d25a91077d_l3.png "Rendered by QuickLaTeX.com"). As usual this forms a discrete probability space given by ![(\mathbb{X}, P)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f7039d9bf15342da0a6a9586280cb3dc_l3.png "Rendered by QuickLaTeX.com").

## 2. First Attempts

### 2.1 A first naive approach

Let ![X^* \in \mathbb{X}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c79857f1b0cb27e67e487c6cc646d936_l3.png "Rendered by QuickLaTeX.com") be the true password. The idea of a brute force search, where every possible password is successive tested, is then to assume that ![\mathbb{P}(X^*=X) = \mathbb{P}(X^*=Y) \;  \forall X^*,X,Y \in \mathbb{X}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-48e9b5b06ffd9c9dbd04d09aa6e6f17b_l3.png "Rendered by QuickLaTeX.com"). This means that every possible password is equipropable and the testing order is thus irrelevant. It is obvious that this Assumption is not true in general.

### 2.2 A very simple Educated Guess Procedure

In the next step we will replace this assumption by some less strong assumptions:

1. E is distributed with distribution ![f_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-211d2e78c7713fd835ad1f3f52658fdc_l3.png "Rendered by QuickLaTeX.com").
2. ![x_i, \, i=1,\dots,E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-652d3c00f2b8026af6943d0bc20f8752_l3.png "Rendered by QuickLaTeX.com") are independent and identically distributed random variables with distribution ![f_x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f110302ab5b58aefbd1e92367872d303_l3.png "Rendered by QuickLaTeX.com").
3. ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") and ![E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-764e1c770271f92700e1a4fbce46c668_l3.png "Rendered by QuickLaTeX.com") are independent.

Under the given Assumptions the best way to “guess” the password is given by the following procedure. Since ![x_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c8700e0258243116de0d4f288e2e3b44_l3.png "Rendered by QuickLaTeX.com") and ![E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-764e1c770271f92700e1a4fbce46c668_l3.png "Rendered by QuickLaTeX.com") are independent we can apply a two step procedure where we first draw some ![\hat{E}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e47baad8533cbecd5784a0b6a9101d3d_l3.png "Rendered by QuickLaTeX.com") using ![f_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-211d2e78c7713fd835ad1f3f52658fdc_l3.png "Rendered by QuickLaTeX.com").Then each ![x_i, \; i=1,\dots,\hat{E}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c5cef6cf15ddb3d461f8580ee75280c7_l3.png "Rendered by QuickLaTeX.com") is independently drawn using ![f_x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f110302ab5b58aefbd1e92367872d303_l3.png "Rendered by QuickLaTeX.com"). Since ![f_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-211d2e78c7713fd835ad1f3f52658fdc_l3.png "Rendered by QuickLaTeX.com") and ![f_x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f110302ab5b58aefbd1e92367872d303_l3.png "Rendered by QuickLaTeX.com") are unknown they have to be estimated from hacked passwords list which we will denote as ![\mathbb{L} \subset \mathbb{X}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-862236a321056f3a8a78d05e4cf0ebde_l3.png "Rendered by QuickLaTeX.com").

#### 2.2.1 Checking the password security

Under the given Assumptions it is also possible to estimate the “safeness” of given password ![X^*](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f750629b9bf95bdbc645f558cce0bb4a_l3.png "Rendered by QuickLaTeX.com"). Mathematically this means 1 minus the probability that a certain password is “guessed” by the procedure. The first part, the probability that the “correct” password length is “guessed” is simply given by ![P(E=E^*)=f_E(E^*)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6b5fa0bef150982a799c8d45fe792461_l3.png "Rendered by QuickLaTeX.com") . The second part can be understood as ![E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-764e1c770271f92700e1a4fbce46c668_l3.png "Rendered by QuickLaTeX.com") [urn draws](https://en.wikipedia.org/wiki/Urn_problem) with replacement of an urn containing the elements of ![\mathbb{A}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4fdb36901bfeee1bb4b059305c252e86_l3.png "Rendered by QuickLaTeX.com") where the probability to draw a certain element ![x](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ede05c264bba0eda080918aaa09c4658_l3.png "Rendered by QuickLaTeX.com") is given by ![f_x(x)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-175b9b91499602828093dcc845018a86_l3.png "Rendered by QuickLaTeX.com"). Thus ![P(x_1= x^*_1, \dots, x_E = x^*_E |E=E^*)= \prod_{i=1}^{E^*} f_x(x_i^*)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-955ecefe179c487627295bd5f3e9f15b_l3.png "Rendered by QuickLaTeX.com"). Accordingly by [Bayes’ theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem "Bayes' theorem"): ![1 -P(x_1 \dots x_E = x^*_1 \dots x^*_E  \cap E=E^* )=1- f_E(E^*) \prod_{i=1}^{E^*} f_x(x_i^*)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ad97ef2ffe48229f7b2e4a8e7c047b92_l3.png "Rendered by QuickLaTeX.com") as security index.

#### 2.2.2 Density Estimators

A very simple estimator ![\hat{f}_E](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-aa853d21b2896978c49b09396af0002f_l3.png "Rendered by QuickLaTeX.com") is based on counting the length of all passwords in ![\mathbb{L}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-152ccfcc269557f18c63529ecf626c48_l3.png "Rendered by QuickLaTeX.com"). The corresponding estimator is then given by ![\hat{f}_E(E^*)= \frac{\# (X \in \mathbb{L} |E=E^*)}{\# \mathbb{L}}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-350afe54fad6baf73244ef4548f2e64e_l3.png "Rendered by QuickLaTeX.com") and accordingly ![\hat{f}_x(x^*)= \frac{ \sum_{k=1}^\infty \# (X \in \mathbb{L} |x_k=x^*)}{ \sum_{k=1}^\infty k \cdot \# (X \in \mathbb{L} |E = k) }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-249ba8d2c0530127bde933847d9827e1_l3.png "Rendered by QuickLaTeX.com").