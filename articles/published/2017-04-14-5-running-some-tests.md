---
categories:
- All Articles
- Coding
- Install Spark on a OrangePi PC
- Projects
- Python
date: '2017-04-14'
slug: 5-running-some-tests
status: publish
tags: []
title: 5. Running some tests
wp_id: 944
wp_modified: '2026-06-11T18:46:50'
---

## 1. Test the Enviroment

### 1.1 Simulation of a Brownian Motion

The purpose of the first notebook entry is to check if matplotlib is correctly installed. We simulate 20 Brownian Motions at [0,1] evaluated at 500 points

```

import numpy

random_color = lambda: '#%02x%02x%02x' % tuple(np.random.randint(0,256,3))
fig = plt.figure()
ax = fig.add_subplot(111)

T=500
N=20
times=np.true_divide( numpy.arange(0, T) ,T)
for i in range(0, N):
    t = ax.plot(times , cumsum(random.normal(0,sqrt(true_divide(1,T)),T)), lw=1, c=random_color())
```

The result should somewhat look like this

[![](https://www.thebigdatablog.com/wp-content/uploads/2017/04/2017-04-11-300x169.png)](https://www.thebigdatablog.com/wp-content/uploads/2017/04/2017-04-11.png)

### 1.2 Validation of the Erdős–Kac theorem

I have a lifelong passion for prime numbers, therefore in this simple Spark Program we will try to validate the [Erdős–Kac theorem](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Kac_theorem) in a finite sample setting. The theorem states that if ![\omega(n)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3f5e47a2af401f7b0f7e43c3d8e0e39d_l3.png "Rendered by QuickLaTeX.com") is the is the number of distinct prime factors, then for any fixed ![a<b](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9b57677a3c7d31d00aea3cdd09443b09_l3.png "Rendered by QuickLaTeX.com"),

(1)    ![\begin{equation*} \lim _{N\rightarrow \infty }\left({\frac {1}{N}}\cdot \#\left\{n\leq N:a\leq {\frac {\omega (n)-\log (\log (n))}{\sqrt {\log (\log (n))}}}\leq b\right\}\right)=\Phi (a,b) \end{equation*}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-96dd4a7106d4a7816595c8693d77ae96_l3.png "Rendered by QuickLaTeX.com")

where ![\Phi (a,b)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7509b8b294827abab3b61a2b7a5c6293_l3.png "Rendered by QuickLaTeX.com") is the standard normal distribution.

```

def prime_factors(n):
    i = 2
    p=n
    factors = []
    while i * i <= n: if n % i: i += 1 else: n //= i factors.append(i) if n > 1:
        factors.append(n)
    dist= ( len( unique(factors) ) -log(log(p)))/sqrt(log(log(p)))
    return dist

N=500000
bins=6
nums = sc.parallelize(xrange(3,N))
result=nums.map(prime_factors).histogram(bins)

binsize=mean( diff( result[0] ) )

axis2=np.linspace(-3, 3, num=128)
mu, sigma = 0, 1 # mean and standard deviation

plt.plot(axis2, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (axis2 - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
plt.bar(result[0][0:bins],true_divide(result[1],N),binsize)
plt.show()
```

This should then look like[![](https://www.thebigdatablog.com/wp-content/uploads/2017/04/2017-04-12-1-300x169.png)](https://www.thebigdatablog.com/wp-content/uploads/2017/04/2017-04-12-1.png)