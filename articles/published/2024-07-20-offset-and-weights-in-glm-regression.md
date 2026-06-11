---
categories:
- All Articles
- Fundamentals
- Introduction
date: '2024-07-20'
slug: offset-and-weights-in-glm-regression
status: publish
tags: []
title: Offset and Weights in GLM Regression
wp_id: 4648
wp_modified: '2024-07-20T12:37:02'
---

## Introduction

In GLMs, we often encounter scenarios where we need to account for exposure or adjust for certain factors. Both offset and weights play crucial roles in achieving this. Let’s break down their differences and understand when to use each one. Let ![Y= (Y_1, Y_2, \dots, Y_n)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d683622470610275fa287464eb9197e0_l3.png "Rendered by QuickLaTeX.com") represent the response variable, ![X_{j} = (X_{j1}, \dots, X_{jm}),  j=1,\dots,n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-73ed521b263b6f5b38c9370f9e06035c_l3.png "Rendered by QuickLaTeX.com") are predictor variables, and ![s_j= \text{time}_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-fdf154ec249e67f87326217f9fe8dd78_l3.png "Rendered by QuickLaTeX.com") represents the exposure time.

### 1. Offset

An **offset** is a covariate included in a model with a fixed coefficient of ![1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4868771cbc422b5818f85500909ce433_l3.png "Rendered by QuickLaTeX.com") (which is not estimated). It acts as a scaling factor for the response variable. Typically, offsets are used with Poisson models to represent exposure. For instance, if you’re modeling count data (e.g., number of events), an offset can account for varying exposure times. The formula for incorporating an offset in a [Poisson GLM](https://www.thebigdatablog.com/frequency-severity-modeling-in-consideration-of-covid-19-induced-effects/) with ![Y \sim Poi(\lambda)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c39a3272c32b2f2d1cf5c062cb034356_l3.png "Rendered by QuickLaTeX.com") is:

     ![\[\text{{Model: }} Y \sim X_1 + X_2 + \ldots + \text{{offset}}(\log(s}))\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c3aaa880d227c09dc6aa9e165b421376_l3.png "Rendered by QuickLaTeX.com")

This makes totally sense, the exposure just multiplies ![\lambda_j = s_j e^{\theta^T X_j }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-76935dfce2108945bab9dfca23d0ed39_l3.png "Rendered by QuickLaTeX.com") compared to a Poisson regression model without different exposure and is **the correct way to incorporate exposure into a Poisson regression**.

The log likelihood is therefore given by

     ![\[log(L) = \sum_{j=1}^n Y_j \theta^T X_j - s_j e^{\theta^T X_j }\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f3f6a908b23981b14b9ed509d83d6df6_l3.png "Rendered by QuickLaTeX.com")

### 2. Using Y_j/s_j as response variable

We still assume that ![Y \sim Poi(\lambda)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c39a3272c32b2f2d1cf5c062cb034356_l3.png "Rendered by QuickLaTeX.com"). Thus assuming ![Y_j/s_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea6b89f9fd5671a8808528b704b66cc8_l3.png "Rendered by QuickLaTeX.com") to be a Poisson distribution as well is incorrect since we are modelling rates now. To see this we take a look at the log likelihood which differs from the offset approach

     ![\[log(L) = \sum_{j=1}^n \frac{Y_j}{s_j} \theta^T X_j - e^{\theta^T X_j }\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ce8b7f79cd90fd126350e44219c6b32c_l3.png "Rendered by QuickLaTeX.com")

### 3. Weights

**Weights**, on the other hand, are quite different. They adjust the variance of the response variable. When using weights, the scale parameter (related to the variance) is divided by the weight values for each observation. Records with weight values less than or equal to 0 or missing are excluded from the analysis. Weights are commonly employed in GLMs to handle heteroscedasticity or unequal variances. Weight are reflected in the log likelihood by

     ![\[log(L) = \sum_{j=1}^n s_j( Y_j \theta^T X_j - e^{\theta^T X_j })\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f8a87e5c61a5ae9d9592191629b589ab_l3.png "Rendered by QuickLaTeX.com")

### **Conclusion:**

To incorporate exposure in an Poisson GLM Regression using an offset is the method of choice. However, a weighted Poisson regression when modelling ![Y_j/s_j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea6b89f9fd5671a8808528b704b66cc8_l3.png "Rendered by QuickLaTeX.com") will give the same results, since:

     ![\[log(L) = \sum_{j=1}^n s_j( \frac{Y_j}{s_i} \theta^T X_j - e^{\theta^T X_j }) = \sum_{j=1}^n Y_j \theta^T X_j - s_j e^{\theta^T X_j }\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a8e18c7d11b338e13989b8298adcd9e7_l3.png "Rendered by QuickLaTeX.com")