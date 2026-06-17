---
categories:
- All Articles
- Coding
- Fundamentals
- Introduction
date: '2021-02-20'
slug: frequency-severity-modeling-in-consideration-of-covid-19-induced-effects
status: publish
tags: []
title: Frequency-Severity Modeling in consideration of COVID-19 induced effects
wp_id: 2470
wp_modified: '2023-10-01T10:11:19'
---

\
This post is supposed to give a brief introduction in Frequency-Severity models. These models are very popular for determine the optimal price for an insurance. We will take a look at the general idea of frequency-severity modeling and for illustration explore a simple example by using rudimentary assumptions. There is a vast amount of literature that deals with how to calculate the model putting different assumptions. For example by assuming that frequency and severity is not independent [[1](#paperkey_18)]. To model covariates this article uses Generalized Linear Models (GLM) [[2](#paperkey_19)] and as an extension Generalized Linear Mixed Models (GLMM), which could be used to model corona effects, solved using Maximum likelihood estimation. Other methods use Bayesian methods [[3](#paperkey_20)], with the advantage that asymptotic results can be derived even if the observed data is sparse, or tree methods that allows a non linear relationship [[4](#paperkey_21), [5](#paperkey_22)].

## 1. Frequency-Severity Modeling

For illustration purposes we lay out a simple univariate model (we are going to model only a single risk), extending the model is straightforward. We want to model the **Loss Cost** of a given entity. Let ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") be the number of claims over the time interval ![[0, 1]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-caffaae885a1287e3dfc31bfb1cd0694_l3.png "Rendered by QuickLaTeX.com"), ![Y_k, \; k=1, ...,N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f27a97bb73f80d50ba6c3d9dea0e2308_l3.png "Rendered by QuickLaTeX.com"), the amount of each claim (loss). Our aim is model the aggregated loss ![S= \sum_{i=1}^N Y_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d38eb9d6ac3286cf9d5f1ec262d86a29_l3.png "Rendered by QuickLaTeX.com"), since ![S](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-520cb534cd5b6bed768a61515b57cb7e_l3.png "Rendered by QuickLaTeX.com") is unbounded, for asymptotics, it is meaningful to consider the average loss per claim ![\bar{S}=\frac{S}{N}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-68b0a53019cf4bb751f899ba73b2a5af_l3.png "Rendered by QuickLaTeX.com"). By construction we are facing two random variables, ![S](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-520cb534cd5b6bed768a61515b57cb7e_l3.png "Rendered by QuickLaTeX.com") is continues while ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") is discrete, the idea of Frequency-Severity Modeling is to model the joined distribution ![f_{N,S}(n,s) :=  \mathbb{P}_{N|S}(n|s)f_S(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bbeae019b11768ecce07f7735a975ec6_l3.png "Rendered by QuickLaTeX.com") as product of frequency and conditional severity distribution

     ![\[f_{N,S}(n,s) =f_{S|N}(s|N=n)\mathbb{P}(N=n).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ba028f54f9d9620227690ea5ed08dbb9_l3.png "Rendered by QuickLaTeX.com")

Instead one can also model ![f_{N,S}(n,s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8f12f57bcb72f46b8bd34ab3cb1a397a_l3.png "Rendered by QuickLaTeX.com") directly, often done using a Tweedie distribution, however by separating frequency and severity additional insights are expected.

### 1.1 Example

A popular approach is to model ![S](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-520cb534cd5b6bed768a61515b57cb7e_l3.png "Rendered by QuickLaTeX.com") as a [compound Poisson process](https://en.wikipedia.org/wiki/Compound_Poisson_process). Assume that ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") is a counting of a Poisson process with intensity ![\lambda >0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-36bfebde7e221181d4d8535ce2311248_l3.png "Rendered by QuickLaTeX.com"), while ![Y_i \sim^{iid} Q](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0063acfd9f02b2cac6aeab46651e0493_l3.png "Rendered by QuickLaTeX.com") where ![Q](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2c758bec4c272382411b95fc0e7ee250_l3.png "Rendered by QuickLaTeX.com") is a probability distribution with density ![f_Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0ad17f2a834e08eaf191b89a8c42d11_l3.png "Rendered by QuickLaTeX.com") independent of ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com"). Then ![\mathbb{P}(N=n)= \frac{\lambda^n}{n!} e^{-\lambda}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c158c1ca6a4c39d4b94890ce82b3a6b8_l3.png "Rendered by QuickLaTeX.com") and ![f_{S|N}(s|N=n) = (\underbrace{f_Y \ast \dots \ast f_Y}_{n-times})(s)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b436b1b6f6c154713d966cd4d9927c9b_l3.png "Rendered by QuickLaTeX.com") a popular choice here is to assume a gamma distribution ![Q= \Gamma(\alpha, \beta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0c6ff17374fb2b0103a6678890fc1ad3_l3.png "Rendered by QuickLaTeX.com") which leads to ![f_{S|N}(s|N=n)= \frac {\displaystyle (n \beta)^{\alpha}}{\displaystyle \Gamma (\alpha)}}s^{\alpha-1}e^{-n \beta s}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a04e298027c00cda2942fb853292a1cb_l3.png "Rendered by QuickLaTeX.com") for ![s >0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7488e186c52a6b8e0f6d9d58ebe38a7a_l3.png "Rendered by QuickLaTeX.com") and ![0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a5e437be25f29374d30f66cd46adf81c_l3.png "Rendered by QuickLaTeX.com") if ![s\leq 0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ebd0c8002dd5064fb4c16aed9aefd9dd_l3.png "Rendered by QuickLaTeX.com"). Statistical measures of interest are for example expected loss and variance given by \

(1)    ![\begin{equation*}E(S) = E(N) E(Y)= \lambda \frac{\alpha}{\beta} $ \text{ and } Var(S)= E(N)Var(Y)+Var(N)E(Y)^2 = \lambda \alpha(\alpha+1) \beta^{-2}.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e11968faffad1ddd51b6a77ab088aafe_l3.png "Rendered by QuickLaTeX.com")

#### 1.1.1 Estimation

Assume we observed claims ![y_1, \dots ,y_n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bb186aaf2b29d7980d3ca5a369104994_l3.png "Rendered by QuickLaTeX.com"), then the maximum likelihood estimators are given by ![\hat{\lambda}_{MLE}=n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-92eec058e1bb8bf4feccb4e3bb3b60b8_l3.png "Rendered by QuickLaTeX.com"), ![\hat{\beta}=  \frac{\hat{\alpha}}{ \bar{y} }](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-25e563fd85831a24e72704ee3467fddc_l3.png "Rendered by QuickLaTeX.com"), while an optimal ![\hat{\alpha}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-89ecd8603670c36cb03393eea395c246_l3.png "Rendered by QuickLaTeX.com") has to fulfill ![n(log(\hat{\alpha})-log(\bar{y}) -\Psi(\hat{\alpha}) + \overline{log(y)} )=0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-203f425768301d1d5043c3ea56cf1dc7_l3.png "Rendered by QuickLaTeX.com") where ![\Psi()](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3a7531b93f851fca495858bbaca80bbe_l3.png "Rendered by QuickLaTeX.com") is [Digamma function](https://en.wikipedia.org/wiki/Digamma_function) . In practice this equation is solved numerically. This leads to estimators for expectation and variance.

## 2. Introducing Covariates

The previous analysis was carried out without covariates ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com"). In the insurance context, there is usually more information available than just the amount and number of claims. Covariates are for example the age of a customer or the car type when looking at motor insurance contracts. An important aspect when modeling insurance data is how long a contract had existed in a certain state of covariates. Thus additionally we introduce an artificial covariates labeled as “**exposure**” used to calibrate the size of a potential outcome variable. Based on these covariates we are interested in the conditional expectation \

     ![\[ E(S|X=x)= E(N|X=x) E(Y|X=x)\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cf08c3be558377af222c6d871db6d7f1_l3.png "Rendered by QuickLaTeX.com")

.

### 2.1 Modeling covariates using GLM

A common way to model covariates is to use a [GLM](https://en.wikipedia.org/wiki/Generalized_linear_model). Let the outcome ![Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82606c3098bb09002088b0f6f9ffbb2a_l3.png "Rendered by QuickLaTeX.com") be a random variable with a particular distribution of the exponential family, e.g. the density can be written as ![f(y|\theta)=exp(\frac{y\theta - b(\theta)}{a(\phi)} + c(y,\phi) )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7810208d2647562b0c485a5e0db28959_l3.png "Rendered by QuickLaTeX.com") where ![\phi \in \mathbb{R}^+](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-56605ac0ff5d1e750e572ec497e04b79_l3.png "Rendered by QuickLaTeX.com") is a scaling parameter also known as dispersion parameter. We assume that there exists some link function ![g](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d208fd391fa57c168dc0f151de829fee_l3.png "Rendered by QuickLaTeX.com") such that for outcome ![Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82606c3098bb09002088b0f6f9ffbb2a_l3.png "Rendered by QuickLaTeX.com") with independent covariates ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com"), ![\mu=E(Y|X)= g^{-1}(X\beta)=g^{-1}(\theta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4730692a2638f0b5e8ff9c473b81d4d3_l3.png "Rendered by QuickLaTeX.com"). Besides, a nice feature is that the variance function has the form \

(2)    ![\begin{equation*}$Var(Y\vert X)=a(\phi)⋅V( E[Y \vert X] ),\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b0b7599c863039795c7d40f8990d2811_l3.png "Rendered by QuickLaTeX.com")

\
meaning that the variance is a function of the mean.

For estimation we rely on Maximum likelihood, in general the log likelihood for the ![j](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43c82d5bb00a7568d935a12e3bd969dd_l3.png "Rendered by QuickLaTeX.com")-th covariate given ![n](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b170995d512c659d8668b4e42e1fef6b_l3.png "Rendered by QuickLaTeX.com") observations given by\

(3)    ![\begin{equation*}l=\sum_{i=1}^n \frac{y_i\theta_i -b(\theta_i)}{a_i(\phi)} + c(y_i, \phi_i) \Rightarrow \frac{l}{\partial \beta_j} = \sum_{i=1}^n \frac{y_i - \mu_i}{a_i(\phi) V(\mu_i)} \times \frac{x_{ij}}{g'(\mu_i)}=0.\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5b0c7bab5cd19660f1b7dfab5d8f40ee_l3.png "Rendered by QuickLaTeX.com")

using the identities ![E(Y)=\mu=b^{'}(\theta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ac20918e5f86121781fe1212cead89c8_l3.png "Rendered by QuickLaTeX.com"), ![Var(Y)= b^{''}(\theta) a(\phi) = V(\mu) a(\phi)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4836f2252931942c16ae7278e9227d12_l3.png "Rendered by QuickLaTeX.com").

#### 1.2.1 Estimate the example using GLM

Recap our previous example, by using a compound Poisson process it was assumed that ![N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5793832f979c2268e3694c246d53b1bb_l3.png "Rendered by QuickLaTeX.com") is a counting of a Poisson process while ![Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82606c3098bb09002088b0f6f9ffbb2a_l3.png "Rendered by QuickLaTeX.com") follows a ![\Gamma(\alpha, \beta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b1bc3469c920fd26d8e25d8963344367_l3.png "Rendered by QuickLaTeX.com") distribution. It is easy to verify, that both distributions are member of the exponential family since the distribution of the Poisson process is given by ![a(\phi)=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3791abc96237c695e08d2303c23cffb3_l3.png "Rendered by QuickLaTeX.com"), ![b(\theta)=exp(\theta)=\lambda](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ac50d6591d4f69cdd1edcca36963bfd9_l3.png "Rendered by QuickLaTeX.com"), ![c(y,\phi)= -log(y!)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-903f109bf27b3614bb196aa1affa0494_l3.png "Rendered by QuickLaTeX.com") while for the Gamma distribution we have to use ![a(\phi)=\phi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8decdeebee8b6ffaf821c119b2e1ae08_l3.png "Rendered by QuickLaTeX.com"), ![b(\theta)=-log(-\theta)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-56271c514b70207fb841c8a874d6741b_l3.png "Rendered by QuickLaTeX.com"), ![c(y,\phi)= \phi^{-2} log(y\phi^{-1}) - log(y) - log(\Gamma(\phi^{-1}))](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bf4e841df0e146ad2f91261ac31e4930_l3.png "Rendered by QuickLaTeX.com") . Finally, based on ([1](#id2552329057)) and ([2](#id2244424231)), \

     ![\[E(S|X)= \lambda \alpha \beta^{-1} \text{ and } Var(S|X)=\lambda V_Y(\alpha \beta^{-1}) + (\alpha \beta^{-1})^2 \phi V_N(\lambda)=\lambda (\alpha \beta^{-1})^2 (\phi +1).\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-17e814797f746bda31585ba4177ef1ea_l3.png "Rendered by QuickLaTeX.com")

\
We assume that we observe ![m](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-6b41df788161942c6f98604d37de8098_l3.png "Rendered by QuickLaTeX.com") types of policyholder. Since in this example, the observed claims ![N=N_1+\dots+ N_m](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c7207a73dc223fb66e5e911912dbb75f_l3.png "Rendered by QuickLaTeX.com") per policyholder is independent from the corresponding claim amount ![Y= \{y_{ij}\}_{i=1,\dots,m, \; j=1,\dots,N_i}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-eedc6c6683d8fb0d46dacfb46746d8bd_l3.png "Rendered by QuickLaTeX.com") the two GLM are estimated separately. Further we assume that there exists ![p](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3bf85f1087e9fbed3a319341134ac1a2_l3.png "Rendered by QuickLaTeX.com") covariates ![X=\{X_i\}_{i=1,\dots,m}=\{x_{ij}\}_{j=1,\dots,m ; j=1,\dots,p}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-94fb2e85beaea50f4aedfc33c7da0d45_l3.png "Rendered by QuickLaTeX.com"). We use a log-link for either GLM, such that with ![\lambda=E(N|X), \; \alpha \beta^{-1}=\mu=E(Y|X)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8e9f4d11428a892776147981876eafc1_l3.png "Rendered by QuickLaTeX.com") the link function is given by ![g=ln](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cd3381dacbe284618b0ea1e2d1f64f8c_l3.png "Rendered by QuickLaTeX.com") and thus ![\lambda_i= exp(\gamma^T X_{i}), \; \mu_i= exp(\zeta^T X_{i})](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-21f617c3ef6387d90d8721d1912964fe_l3.png "Rendered by QuickLaTeX.com") where ![\gamma = (\gamma, \dots, \gamma_p)^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f9a7d7d5618eee84dc844f56c303aacf_l3.png "Rendered by QuickLaTeX.com") and ![\zeta = (\zeta_1, \dots, \zeta_p)^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3ce234f2b04ef382d5d40146a3ecad8b_l3.png "Rendered by QuickLaTeX.com").

In order to find the maximum likelihood estimate for ![\gamma_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-566615c9af5caaf0f8bfe4fe03cf1676_l3.png "Rendered by QuickLaTeX.com"), we use the log likelihood to calculate\

(4)    ![\begin{equation*}l(N|X, \gamma) = \sum_{i=1}^m (N_i \gamma^T X_{i} - exp(\gamma^T X_i) )\; \text{with FOC} \; \sum_{i=1}^m x_{ik} (N_i - exp(\gamma^T X_i)) = 0\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-799f1dc3f82b9ad1d94cd2b154980e59_l3.png "Rendered by QuickLaTeX.com")

\
with a limiting distribution ![\sqrt{m} (\gamma-\hat{\gamma}) \approx N(0, I_\gamma^{-1}) \; \text{ with }  I_\gamma= X diag(\hat{\lambda}_1,\dots,\hat{\lambda}_m) X^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9d4519410acdf7211d4e6a58bfaac1e9_l3.png "Rendered by QuickLaTeX.com").\
Accordingly the maximum likelihood estimate for ![\zeta_k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d0760f00533a46cc026ddd9a6c6e8c4a_l3.png "Rendered by QuickLaTeX.com") using the log likelihood is given by \

     ![\[l(Y|X, \zeta)= \sum_{i=1}^m \sum_{j=1}^{N_i} \frac{- y_{ij}exp(\zeta^T X_i)^{-1} -exp(\zeta^T X_i)}{\phi}\text{ and FOC} \sum_{i=1}^m \sum_{j=1}^{N_i} \frac{x_{ik}(y_{ij}-exp(\zeta^T X_i)) }{\phi exp(\zeta^T X_i)}=0\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-67114c37ee51fe0b891b49dbec8d7c20_l3.png "Rendered by QuickLaTeX.com")

\
with a limiting distribution ![\sqrt{N} (\zeta-\hat{\zeta}) \approx N(0, I_\zeta^{-1}) \; \text{ with } I_\zeta= \frac{1}{\phi}X X^T](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4b9e005a2c28927f26437eb7c2f2b57d_l3.png "Rendered by QuickLaTeX.com").

### 2.2 Incorporate Random Effects

Mixed effect models are used in cases where the response variables arise from different distributions. Therefore they are particularly useful provided that a repeated measurement is made on the same or on clusters of related statistical units. A nice intuition whether to model a random or a fixed effect can be found [here](https://rlbarter.github.io/Practical-Statistics/2017/03/03/fixed-mixed-and-random-effects/). In a nutshell, model a factor as a random effects if:

- If the factor (group) is expected to have expression not yet observed (not entire population of groups is observed)
- If for a particular reason we are not interested in the coefficient of the factor rather than the anticipated structure that may be imposed on our observations.

\
In the insurance context we can use random effects to model a setup where several observations belong to the same few policyholder. In that case the unique identifier for each policyholder is used as covariates for random effects. Another important application where we may use random effect to create better models is due to the corona crisis. Here we observe polices which where issued under corona restrictions installed by the government while others are not. It is very likely that, for example because people do no longer drive to work, this has an effect on the occurred claims. A possible way out is to add the information of government policies as additional covariates to be modeled using random effects. \
Thus, as an extension of the GLM in this section we will now include both fixed and random effects, leading to a *Generalized Mixed Effect Model* (GLMM). Similar to the GLM case we assume that each expression of ![Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82606c3098bb09002088b0f6f9ffbb2a_l3.png "Rendered by QuickLaTeX.com") follows a particular distribution of the exponential family such that conditioned on the random effect ![u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43fe27dc3e528266a619764d90fce60b_l3.png "Rendered by QuickLaTeX.com") \

(5)    ![\begin{equation*}f(y\mathbin{\vert} \theta,u)=exp(\frac{y\theta - b(\theta)}{a(\phi)} + c(y,\phi) )\end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7b68fc43b0413528206a6627e5792df8_l3.png "Rendered by QuickLaTeX.com")

\
where the covariates are separated for fixed effects ![\beta](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b6a7605b1bcca8f1b416eaf733f34e08_l3.png "Rendered by QuickLaTeX.com") and random effects ![u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43fe27dc3e528266a619764d90fce60b_l3.png "Rendered by QuickLaTeX.com"), distributed with ![f_U](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4801e92bd6d8f0bebb97f53b24b2ca59_l3.png "Rendered by QuickLaTeX.com"), such that ![E[Y|u] = \mu](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-5cb611a22b4301236f7297dba18e49e4_l3.png "Rendered by QuickLaTeX.com"), ![g(\mu) = X \beta + Z u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b17106d661fc5d4ea4d94d5cce527bd6_l3.png "Rendered by QuickLaTeX.com"). For random effects we require that ![E(u)=0, Var(u)=G](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9d0237baf595ad1f7b887e79ed06631e_l3.png "Rendered by QuickLaTeX.com"). Similar to ([3](#id2694037013)) the likelihood is given by\

     ![\[L=\prod_{i=1}^n \int exp( \frac{y_i\theta_i -b(\theta_i)}{a_i(\phi)} + c(y_i, \phi_i))  f_U(u)du.\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b1db92ea0918cb2ad4ec463e57e93ba8_l3.png "Rendered by QuickLaTeX.com")

\
Therefore fitting GLMMs via maximum likelihood is very similar to solve the GLM, but involves an additional integration over the random effects. This is usually extremely computationally intensive, especially when more covariates are modeled using random effects.

#### 2.2.1 Extension of the Example

For illustration we will now extend our frequency example using a Poisson process and allow further for a single independent normal distributed random effect. Thus \

(6)    ![\begin{align*}N_i|u_1,\dots, u_m \sim Poi(\lambda_i) \\u_i \sim N(0,\sigma^2)\end{align*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-518f84aeb27bbc94807c91664cdea489_l3.png "Rendered by QuickLaTeX.com")

\
Using the link ![\lambda_i=exp(\gamma^T X_i  + Z_i u_i)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7e1db73d0a65154ea70bf5f403b9a9f2_l3.png "Rendered by QuickLaTeX.com"), the Likelihood is comparable to ([4](#id2144167678)) and is given by\

     ![\[L=\prod_{i=1}^m \int \frac{e^{N_i (\gamma^T X_{i} + Z_i u_i) }e^{-e^{\gamma^T X_{i} + Z_i u_i}}} {N_i!} \times exp(-u_i^2/2\sigma^2)/(2\pi\sigma^2)^{-1/2} d u_i.\]](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b0bb1273ef61262b5112d97e6973a35e_l3.png "Rendered by QuickLaTeX.com")

## 3. Coding example in R

As an illustrative example we will use the well know [Swedish Insurance Dataset](https://www.kaggle.com/floser/swedish-motor-insurance/). These data were compiled by the Swedish Committee on the Analysis of Risk Premium in Motor Insurance, summarized in Hallin and Ingenbleek (1983) and Andrews and Herzberg (1985). The data are cross-sectional, describing third party automobile insurance claims for the year 1977. In this example we will model the number of claims (the frequency) using a GLM as described above based on the covariates Kilometers, Zone, Bonus, Make and with a GLMM using “Zones” as random effects.






















```
library('lme4')
```

```
## Loading required package: Matrix
```

```
library('doParallel')
```

```
## Loading required package: foreach
```

```
## Loading required package: iterators
```

```
## Loading required package: parallel
```

```
library('foreach')

# Load the Dataset
SwedishMotorInsurance <- read.csv("D:/git/car_claims/SwedishMotorInsurance.csv")

# Fit the Model using the entire Dataset to check for significant factors
glm =glm(Claims ~ Kilometres+factor(Zone)+
                     factor(Bonus)+factor(Make), offset=log(Insured),poisson(link=log), data=SwedishMotorInsurance)
summary(glm)
```

```
## 
## Call:
## glm(formula = Claims ~ Kilometres + factor(Zone) + factor(Bonus) + 
##     factor(Make), family = poisson(link = log), data = SwedishMotorInsurance, 
##     offset = log(Insured))
## 
## Deviance Residuals: 
##     Min       1Q   Median       3Q      Max  
## -7.9809  -0.8745  -0.1800   0.5774   6.5738  
## 
## Coefficients:
##                 Estimate Std. Error  z value Pr(>|z|)    
## (Intercept)    -1.915417   0.014012 -136.697  < 2e-16 ***
## Kilometres      0.139678   0.002596   53.805  < 2e-16 ***
## factor(Zone)2  -0.238441   0.009495  -25.111  < 2e-16 ***
## factor(Zone)3  -0.387248   0.009669  -40.049  < 2e-16 ***
## factor(Zone)4  -0.582763   0.008653  -67.345  < 2e-16 ***
## factor(Zone)5  -0.326750   0.014529  -22.489  < 2e-16 ***
## factor(Zone)6  -0.526907   0.011876  -44.366  < 2e-16 ***
## factor(Zone)7  -0.731561   0.040698  -17.976  < 2e-16 ***
## factor(Bonus)2 -0.476283   0.012090  -39.395  < 2e-16 ***
## factor(Bonus)3 -0.689975   0.013502  -51.102  < 2e-16 ***
## factor(Bonus)4 -0.824070   0.014577  -56.534  < 2e-16 ***
## factor(Bonus)5 -0.923048   0.013960  -66.121  < 2e-16 ***
## factor(Bonus)6 -0.992035   0.011622  -85.359  < 2e-16 ***
## factor(Bonus)7 -1.326230   0.008673 -152.910  < 2e-16 ***
## factor(Make)2   0.073345   0.021238    3.454 0.000553 ***
## factor(Make)3  -0.251061   0.025091  -10.006  < 2e-16 ***
## factor(Make)4  -0.671032   0.024120  -27.821  < 2e-16 ***
## factor(Make)5   0.153801   0.020234    7.601 2.94e-14 ***
## factor(Make)6  -0.338687   0.017372  -19.496  < 2e-16 ***
## factor(Make)7  -0.056468   0.023343   -2.419 0.015561 *  
## factor(Make)8  -0.052694   0.031581   -1.669 0.095216 .  
## factor(Make)9  -0.073278   0.009939   -7.373 1.67e-13 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for poisson family taken to be 1)
## 
##     Null deviance: 34070.6  on 2181  degrees of freedom
## Residual deviance:  3087.6  on 2160  degrees of freedom
## AIC: 10769
## 
## Number of Fisher Scoring iterations: 4
```

```
glmm <- glmer(Claims ~ Kilometres+factor(Bonus)
               +factor(Make)+ offset(log(Insured)) + (1|Zone), family=poisson(link=log), data=SwedishMotorInsurance) 
summary(glmm)
```

```
## Generalized linear mixed model fit by maximum likelihood (Laplace
##   Approximation) [glmerMod]
##  Family: poisson  ( log )
## Formula: 
## Claims ~ Kilometres + factor(Bonus) + factor(Make) + offset(log(Insured)) +  
##     (1 | Zone)
##    Data: SwedishMotorInsurance
## 
##      AIC      BIC   logLik deviance df.resid 
##  10810.2  10906.9  -5388.1  10776.2     2165 
## 
## Scaled residuals: 
##     Min      1Q  Median      3Q     Max 
## -7.7295 -0.7598 -0.1686  0.5935  9.9509 
## 
## Random effects:
##  Groups Name        Variance Std.Dev.
##  Zone   (Intercept) 0.04945  0.2224  
## Number of obs: 2182, groups:  Zone, 7
## 
## Fixed effects:
##                 Estimate Std. Error  z value Pr(>|z|)    
## (Intercept)    -2.313183   0.085212  -27.146  < 2e-16 ***
## Kilometres      0.139678   0.002596   53.806  < 2e-16 ***
## factor(Bonus)2 -0.476295   0.012090  -39.397  < 2e-16 ***
## factor(Bonus)3 -0.689984   0.013502  -51.103  < 2e-16 ***
## factor(Bonus)4 -0.824074   0.014576  -56.535  < 2e-16 ***
## factor(Bonus)5 -0.923050   0.013960  -66.122  < 2e-16 ***
## factor(Bonus)6 -0.992032   0.011622  -85.360  < 2e-16 ***
## factor(Bonus)7 -1.326260   0.008673 -152.916  < 2e-16 ***
## factor(Make)2   0.073348   0.021237    3.454 0.000553 ***
## factor(Make)3  -0.251008   0.025090  -10.004  < 2e-16 ***
## factor(Make)4  -0.671048   0.024119  -27.822  < 2e-16 ***
## factor(Make)5   0.153803   0.020234    7.601 2.93e-14 ***
## factor(Make)6  -0.338714   0.017372  -19.498  < 2e-16 ***
## factor(Make)7  -0.056462   0.023342   -2.419 0.015569 *  
## factor(Make)8  -0.052737   0.031581   -1.670 0.094938 .  
## factor(Make)9  -0.073280   0.009939   -7.373 1.67e-13 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

```
## 
## Correlation matrix not shown by default, as p = 16 > 12.
## Use print(x, correlation=TRUE)  or
##     vcov(x)        if you need it
```

```
ranef(glmm)
```

```
## Zone
##   (Intercept)
## 1  0.39743524
## 2  0.15919148
## 3  0.01052576
## 4 -0.18486041
## 5  0.07079332
## 6 -0.12886749
## 7 -0.32328705
## 
## with conditional variances for "Zone"
```

```
# Create a helper function for model evaluation
model_eval = function(train, test) {
  glm =glm(Claims ~ Kilometres+factor(Zone)+
             factor(Bonus)+factor(Make), offset=log(Insured),poisson(link=log), data=train)
  
  glmm <- glmer(Claims ~ Kilometres+factor(Bonus)
                +factor(Make)+ offset(log(Insured)) + (1|Zone), family=poisson(link=log), data=train) 
  
  N=dim(test)[1]
  mse_glm = 1/N*sum( (predict( glm  ,test, type = "response") -test["Claims"] )^2 )
  mse_glmm = 1/N*sum( (predict( glmm ,test, type = "response") -test["Claims"] )^2 )
  return( c(mse_glm, mse_glmm) )
}
# Compare the fit
model_eval(SwedishMotorInsurance,SwedishMotorInsurance)
```

```
## [1] 223.3410 223.3951
```

```
# Eval the model under different conditions

## Resample with test and train
cl <- makeCluster(15) #number of cores
registerDoParallel(cl)

runs <- foreach(1:100, .combine='cbind') %dopar% {
  library('lme4')
  N= dim(SwedishMotorInsurance)[1]
  sample=sample(1:N, floor(0.8*N), replace = FALSE, prob = NULL)
  train=SwedishMotorInsurance[sample,]
  test=SwedishMotorInsurance[-sample,]
  model_eval(train, test)
}
boxplot(t(runs), names= c("glm", "glmm") )
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABUAAAAPACAMAAADDuCPrAAAA0lBMVEUAAAAAADoAAGYAOjoAOmYAOpAAZrY6AAA6OgA6Ojo6OmY6OpA6ZmY6ZpA6ZrY6kJA6kLY6kNtmAABmOgBmOjpmZjpmZmZmZpBmkJBmkLZmkNtmtttmtv+QOgCQOjqQZgCQZjqQZmaQkLaQtraQttuQtv+Q29uQ2/+2ZgC2Zjq2kDq2kGa2kLa2tpC2tra2ttu227a229u22/+2///T09PbkDrbkGbbtmbbtpDbtrbb27bb29vb2//b/9vb////tmb/25D/27b/29v//7b//9v///9Gab7WAAAACXBIWXMAAB2HAAAdhwGP5fFlAAAgAElEQVR4nO3dfXsTV5rgYZkmGDKd7CZk1Msm7DALM5BmIhayNC/OYhzk7/+VtiTZWLKq7VOPj16On/v+owNOXJev81T9WrJKR6NTAEJGu/4BAFoloABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIKECSgAEECChAkoABBAgoQJKAAQQIK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)

In this example the Mixed Model does not improve the prediction quality of the model. This is not surprising since “Zones” is distributed equally and the test dataset resemble the training data very well. The take away message here is that in this example we are not worse off using a glmm instead of a glm.

We will now push the luck a bit in favor n the direction of the GLMM by modifying the sample strategy to evaluate the model. An important application of the GLMM if not the entire population of a factor is observed,

Since we still want to compare both models and a GLM is not able to perform a prediction using an unknown factor not used for training we will give the glm only very few observations for a certain group instead. To evaluate the model, then only observations from that group are used.

```
trails = 500
n_train = c( rep(2,trails), rep(5,trails),  rep(20,trails),  rep(30,trails) ) 

runs_z6 <- foreach(n_train=n_train, .combine='cbind' ) %dopar% {
  library('lme4')
  train_o6=SwedishMotorInsurance[SwedishMotorInsurance["Zone"]!=6,]
  data_m6=SwedishMotorInsurance[SwedishMotorInsurance["Zone"]==6,]
  sample=sample(1:dim(data_m6)[1], n_train, replace = FALSE, prob = NULL)
  train=rbind(train_o6, data_m6[sample,])
  test=data_m6[-sample,]
  c(n_train/dim(data_m6)[1], model_eval(train, test))
}

data=t(runs_z6)
boxplot( c(data[,2],data[,3]) ~ paste( rep(round(data[,1],2) ,2), c( rep("GLM", length(n_train)), rep("GLMM", length(n_train))) ) , outline=FALSE,ylab="MSE", xlab="Model",cex.axis = 0.6)
rect(0.5,-3,2.5,3300,col="grey90",lty=0)
rect(4.5,-3,6.5,3300,col="grey90",lty=0)
boxplot( c(data[,2],data[,3]) ~ paste( rep(round(data[,1],2) ,2), c( rep("GLM", length(n_train)), rep("GLMM", length(n_train))) ) , outline=FALSE,ylab="MSE", xlab="Model",add=TRUE,cex.axis = 0.6)
```

![](data:image/png;base64,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)

The figure shows how the two models perform. For training only a fraction, ranging from 0.01 to 0.1, of observations from one particular group where available. We can conclude, that the GLMM performs better if only a fraction of observation for a certain group are present for training. If more data becomes available the predictive power of GLM and GLMM coincide.







### References

[1] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/https://doi.org/10.1016/j.insmatheco.2016.06.006 "View document in publisher site") J. Garrido, C. Genest, and J. Schulz, “Generalized linear models for dependent frequency and severity of insurance claims,” Insurance: mathematics and economics, vol. 70, pp. 205-215, 2016. \
 [[Bibtex]](javascript:void(0))

```
@article{Garrido2016,
title = {Generalized linear models for dependent frequency and severity of insurance claims},
journal = {Insurance: Mathematics and Economics},
volume = {70},
pages = {205-215},
year = {2016},
issn = {0167-6687},
doi = {https://doi.org/10.1016/j.insmatheco.2016.06.006},
url = {https://www.sciencedirect.com/science/article/pii/S0167668715303358},
author = {J. Garrido and C. Genest and J. Schulz},
keywords = {Aggregate claims model, Claim frequency, Claim severity, Dependence, Exponential dispersion models, Generalized linear model, Loss cost},
abstract = {Traditionally, claim counts and amounts are assumed to be independent in non-life insurance. This paper explores how this often unwarranted assumption can be relaxed in a simple way while incorporating rating factors into the model. The approach consists of fitting generalized linear models to the marginal frequency and the conditional severity components of the total claim cost; dependence between them is induced by treating the number of claims as a covariate in the model for the average claim size. In addition to being easy to implement, this modeling strategy has the advantage that when Poisson counts are assumed together with a log-link for the conditional severity model, the resulting pure premium is the product of a marginal mean frequency, a modified marginal mean severity, and an easily interpreted correction term that reflects the dependence. The approach is illustrated through simulations and applied to a Canadian automobile insurance dataset.}
}
```

[2] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/https://doi.org/10.2307/2988543 "View document in publisher site") S. Haberman and A. E. Renshaw, “Generalized linear models and actuarial science,” Journal of the royal statistical society: series d (the statistician), vol. 45, iss. 4, pp. 407-436, 1996. \
 [[Bibtex]](javascript:void(0))

```
@article{Haberman1996,
author = {Haberman, Steven and Renshaw, Arthur E.},
title = {Generalized Linear Models and Actuarial Science},
journal = {Journal of the Royal Statistical Society: Series D (The Statistician)},
volume = {45},
number = {4},
pages = {407-436},
keywords = {Generalized linear models, Life-insurance, non-life-insurance models},
doi = {https://doi.org/10.2307/2988543},
url = {https://rss.onlinelibrary.wiley.com/doi/abs/10.2307/2988543},
eprint = {https://rss.onlinelibrary.wiley.com/doi/pdf/10.2307/2988543},
abstract = {SUMMARY The authors review the applications of generalized linear models to actuarial problems. This rich class of statistical model has been successfully applied in recent years to a wide range of problems, involving mortality, multiple-state models, lapses, premium rating and reserving. Selective examples of these applications are presented.},
year = {1996}
}
```

[3] C. Gao, Q. Li, and Z. Guo, “Automobile insurance pricing with bayesian general linear model,” in Innovative computing and information, Berlin, Heidelberg, 2011, p. 359–365. \
 [[Bibtex]](javascript:void(0))

```
@InProceedings{Gao2011,
author="Gao, Cheng
and Li, Qi
and Guo, Zirui",
editor="Dai, Minli",
title="Automobile Insurance Pricing with Bayesian General Linear Model",
booktitle="Innovative Computing and Information",
year="2011",
publisher="Springer Berlin Heidelberg",
address="Berlin, Heidelberg",
pages="359--365",
abstract="This paper applies Bayesian Model to the automobile insurance pricing in the purpose of solving the problem that the Generalized Linear Model (GLM) applied in actuarial pricing cannot reveal prior information and has too much confidence in the information from data. Under the assumption of Squared Error Loss, the estimation of the parameter in the model is the mean of the posterior distribution which was calculated by Markov Chain Monte Carlo Methods (MCMC). Finally, take the auto-insurance of WASA Insurance Company in Switzerland as an example. Run MCMC in WINBUGS software to get the estimation of the parameters, and design the comparative auto insurance tariff for this company. The comparison between the pricing utilizing Bayesian Model and that according to GLM reveals that owing to the function of prior information, the two automobile tariffs differ distinctively. Moreover, the prior information has been elegantly reflected in the Bayesian Model.",
isbn="978-3-642-23993-9"
}
```

[4] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/https://doi.org/10.1016/j.eswa.2011.09.058 "View document in publisher site") L. Guelman, “Gradient boosting trees for auto insurance loss cost modeling and prediction,” Expert systems with applications, vol. 39, iss. 3, pp. 3659-3667, 2012. \
 [[Bibtex]](javascript:void(0))

```
@article{Guelman2012,
title = {Gradient boosting trees for auto insurance loss cost modeling and prediction},
journal = {Expert Systems with Applications},
volume = {39},
number = {3},
pages = {3659-3667},
year = {2012},
issn = {0957-4174},
doi = {https://doi.org/10.1016/j.eswa.2011.09.058},
url = {https://www.sciencedirect.com/science/article/pii/S0957417411013674},
author = {Leo Guelman},
keywords = {Statistical learning, Gradient boosting trees, Insurance pricing},
abstract = {Gradient Boosting (GB) is an iterative algorithm that combines simple parameterized functions with “poor” performance (high prediction error) to produce a highly accurate prediction rule. In contrast to other statistical learning methods usually providing comparable accuracy (e.g., neural networks and support vector machines), GB gives interpretable results, while requiring little data preprocessing and tuning of the parameters. The method is highly robust to less than clean data and can be applied to classification or regression problems from a variety of response distributions (Gaussian, Bernoulli, Poisson, and Laplace). Complex interactions are modeled simply, missing values in the predictors are managed almost without loss of information, and feature selection is performed as an integral part of the procedure. These properties make GB a good candidate for insurance loss cost modeling. However, to the best of our knowledge, the application of this method to insurance pricing has not been fully documented to date. This paper presents the theory of GB and its application to the problem of predicting auto “at-fault” accident loss cost using data from a major Canadian insurer. The predictive accuracy of the model is compared against the conventional Generalized Linear Model (GLM) approach.}
}
```

[5] [![[doi]](https://www.thebigdatablog.com/wp-content/plugins/papercite-master/img/external.png)](http://dx.doi.org/10.1080/10920277.2020.1745656 "View document in publisher site") R. Henckaerts, M. Côté, K. Antonio, and R. Verbelen, “Boosting insights in insurance tariff plans with tree-based machine learning methods,” North american actuarial journal, pp. 1-31, 2020. \
 [[Bibtex]](javascript:void(0))

```
@article{Henckaerts2020,
author = { Roel Henckaerts and Marie-Pier Côté and Katrien Antonio and Roel Verbelen },
title = {Boosting Insights in Insurance Tariff Plans with Tree-Based Machine Learning Methods},
journal = {North American Actuarial Journal},
volume = {0},
number = {0},
pages = {1-31},
year = {2020},
publisher = {Routledge},
doi = {10.1080/10920277.2020.1745656},
URL = {
https://doi.org/10.1080/10920277.2020.1745656
},
eprint = {
https://doi.org/10.1080/10920277.2020.1745656
}
}
```