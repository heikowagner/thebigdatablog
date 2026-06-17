---
categories:
- All Articles
- Coding
- Introduction
- Python
- Python
date: '2025-03-08'
slug: efficient-kernel-smoother-in-the-onnx-format
status: publish
tags: []
title: Efficient Kernel Smoother in the ONNX Format
wp_id: 4696
wp_modified: '2025-03-16T10:59:33'
---

Efficient data processing lies at the heart of modern machine learning. Kernel smoothing, a versatile non-parametric technique, benefits significantly from performance improvements through optimized algorithms and frameworks. In this post, we’ll explore the process of converting a NumPy-based kernel regression implementation, utilizing the Fast Fourier Transform (FFT), into an ONNX-based format. This approach not only ensures platform independence and interoperability but also harnesses hardware acceleration for enhanced performance.

### Introduction

The original implementation of the kernel regression in Python leverages NumPy and FFT to achieve efficient calculations, reducing computational complexity. However, to deploy such models across multiple platforms with minimal changes, converting the implementation to ONNX proves beneficial. ONNX enables models to be exchanged across frameworks, ensuring seamless integration and a notable boost in performance. Tools like [`ndonnx`](https://github.com/Quantco/ndonnx) and [`spox`](https://github.com/Quantco/spox/) further simplify the transition to ONNX by abstracting complex aspects of the conversion process.

### **1. Core Functionality**

The primary goal of the script is to perform kernel regression using FFT to accelerate computations. By applying the FFT, the script efficiently handles convolution-like operations, which are central to kernel density estimation or regression tasks.

Here’s an excerpt of the [script we already discussed](https://www.thebigdatablog.com/kernel-regression-using-the-fast-fourier-transform/) based on [[1](#paperkey_6)] (simplified for clarity):

```
# %%
import numpy as np
# Simulation
T = 500
X = np.linspace(-5, 5, T) 
Y= (X)**3 + np.random.normal(-0, 10, T)

def epan_kernel(u, b):
    u = u / b
    return max(0, 1. / b * 3. / 4 * (1 - u ** 2))


def kernel_smoothing(X, Y, h):
    kernel = [epan_kernel(x, h) for x in X]
    func_tmp = np.fft.fft(kernel) * np.fft.fft(Y)
    m_fft = (max(X)-min(X))*np.fft.fftshift(np.fft.ifft(func_tmp).real)/len(X)
    return m_fft

kernel_smoothing(X, Y, h=0.5)
```

#### **1.1. Key Components of the Script**

The script begins with input data represented by a NumPy array. This includes ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com"), which is an independent variable comprising evenly spaced points between ![-5](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7b5b9d9f382b11767d19f257afca0019_l3.png "Rendered by QuickLaTeX.com") and ![5](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-8995e2084120c1c1f4b53f490d281bc4_l3.png "Rendered by QuickLaTeX.com"), and ![Y](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-82606c3098bb09002088b0f6f9ffbb2a_l3.png "Rendered by QuickLaTeX.com"), the dependent variable following the function ![Y = X^3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2f631016e91c61e5f5bd581b0fd1592b_l3.png "Rendered by QuickLaTeX.com") plus some added random noise to simulate real-world conditions. The bandwidth, ![h](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-14b463d0ecd5b350ced6cf1d6a12eef3_l3.png "Rendered by QuickLaTeX.com"), is also specified and controls the degree of smoothing, with smaller values leading to less smoothing and larger values providing greater smoothing.

To enhance computational efficiency, the input data undergoes a Fourier Transform using `np.fft.fft()`. This transformation shifts the data from the time or spatial domain into the frequency domain, where convolution operations become significantly faster as they translate into pointwise multiplication.

A kernel function, often Gaussian or Epanechnikov, is also transformed into the frequency domain. Applying the kernel involves performing element-wise multiplication between the Fourier-transformed data and the kernel in this domain.

Finally, the result of this multiplication is transformed back into the time domain through an Inverse Fourier Transform using `np.fft.ifft()`. This step produces the final output, completing the kernel regression process.

#### **1.2. Why FFT Matters Here**

The kernel regression problem requires calculating weighted sums or smooth approximations over a dataset. Without FFT, this involves ![\mathcal{O}(n^2)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cc5ab0467393b6c3ad4309a1b0b75301_l3.png "Rendered by QuickLaTeX.com") computations (pairwise operations between all data points). FFT reduces this complexity to ![\mathcal{O}(n \log n)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e2d1dd597fd00ceb8e3002dcdca43cff_l3.png "Rendered by QuickLaTeX.com"), enabling the script to process large datasets efficiently.

### 2. **Porting the Script to ONNX**

#### **2.1: Understanding the Limitation of ndonnx**

Currently, `ndonnx` does not support FFT-related functionality such as `np.fft.fft` and `np.fft.ifft`. This limitation means that we cannot directly export scripts involving FFT computations using `ndonnx`. However, ONNX itself provides operators for Discrete Fourier Transform (DFT). By combining `ndonnx` with `spox`, we can bypass this limitation.

#### **2.2. Mimicking Functionality within ndonnx**

Some operations, while not natively supported, can be mimicked by creatively using existing `ndonnx` features. One such example is `fftshift`. This operation rearranges the Fourier transform output, moving the zero-frequency component to the center of the spectrum. Using `ndonnx`, we can replicate this behavior with a custom implementation.

Here’s how we might mimic elementwise `np.maximum(0,x)` in `ndonnx`:

```
def ndx_elementwise_max_0(y):
    xy = y.__array_namespace__()
    return ((y+xy.abs(-y)))/2
```

Certain operations, like FFT, require the use of `spox` due to the absence of direct support in `ndonnx`. The `spox` library allows us to construct ONNX computation graphs that include advanced operators such as `DFT`, which are crucial for Fourier transform operations.

Example: Implementing FFT with `spox`:

```
@eager_propagate
def fft(x: ndx.Array, inverse: int=0, onesided: int=0) -> ndx.Array:
    var = x.spox_var()
    fft_var = op.dft(var, inverse=inverse, onesided=onesided)
    return ndx.from_spox_var(fft_var)
```

This method allows direct access to ONNX’s `DFT` operator through `spox`, creating a seamless solution for FFT operations. A full overview of the needed polyfills, for example complex multiplication, can be found in the corresponding [polyfill script](https://github.com/heikowagner/thebigdatablog/blob/master/jupyter_notebooks/fft_kernel/polyfills.py).

#### **2.3 Final Estimator**

With this we can then derive the final estimator.

```
import numpy as np
import ndonnx as ndx
from polyfills import ndx_elementwise_max_0, ndx_elementwise_complex_multiply, fft, ifft, fftshift

np.random.seed(0)

# Initializing an array with data
# Simulation
T = 500
X = np.linspace(-5, 5, T) # Oberservation points
Y= (X)**3 + np.random.normal(-0, 10, T)  # Noisy function to estimate

ndx_X = ndx.asarray(X)
ndx_Y = ndx.asarray(Y)

def epan_kernel(u, b):
    u = u / b
    return ndx_elementwise_max_0( 1. / b * 3. / 4 * (1 - u ** 2) )

def kernel_smoother(X, Y, h):
    xy = X.__array_namespace__()
    kernel = epan_kernel(X, h)
    kernel_ft = fft(xy.reshape(kernel, (1, -1, 1)))
    y_ft = fft(xy.reshape(Y, (1, -1, 1)))
    func_tmp = ndx_elementwise_complex_multiply(kernel_ft, y_ft)
    m_fft = (xy.max(X)-xy.min(X))*ifft(func_tmp)[0,:,0]/X.size   # realteil
    return m_fft
# %%

kernel_result = ndx.roll( kernel_smoother(ndx_X, ndx_Y, T**(-1/5)), T//2)
```

The output represents the smoothed version of the data. The `ifft()` function approximates the DFT in the range from ![0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-a5e437be25f29374d30f66cd46adf81c_l3.png "Rendered by QuickLaTeX.com") to ![\pi](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-26d6788550ffd50fe94542bb3e8ee615_l3.png "Rendered by QuickLaTeX.com"). To correctly reorder the output vector from `ifft()`, a `roll()` operation is required to shift it right down the middle. However, this operation cannot be performed directly with `ndonnx`, as determining the concrete shape of a lazy array (in our case ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com")) may not always be feasible.

#### **2. 4 Exporting Model to ONNX**

To export a model to ONNX, we define placeholder arrays for the inputs and parameters using `ndx.array`, specifying their shapes and data types. For instance, `X` and `Y` might represent input data, while `h` is a parameter for the kernel. The model’s computation is defined through a function like `kernel_smoother` applied to these inputs. Once the relationships between inputs and outputs are established, the model can be built using `ndx.build`, which takes the inputs and the computed output (`y`) as its arguments. Finally, the `onnx.save` function saves the model to disk in ONNX format, allowing for seamless portability and use across different platforms. Let’s have a look at the script:

```
import onnx
...
X = ndx.array(shape=("N",), dtype=ndx.float64)
Y = ndx.array(shape=("N",), dtype=ndx.float64)
h = ndx.array(shape=("1"), dtype=ndx.float64)

y = kernel_smoother(X, Y, h)

model = ndx.build({"X": X, "Y": Y, "h": h}, {"y": y})
onnx.save(model, "./kernel_smoother.onnx")
```

This code captures the workflow, creating a structured yet portable ONNX model ready for deployment. To access the scripts follow this [link](https://github.com/heikowagner/thebigdatablog/tree/master/jupyter_notebooks/fft_kernel). With the [Netron](https://netron.app/) we can create visualisation of the generated ONNX graph:

[![kernel smoother (1).onnx (1)](https://www.thebigdatablog.com/wp-content/uploads/2025/03/kernel_smoother-1.onnx-1-551x1024.png)](https://www.thebigdatablog.com/wp-content/uploads/2025/03/kernel_smoother-1.onnx-1.png)

Graph visualisation of kernel smoother.onnx provided by Netron.

#### **2. 4 Load and execute**

To load and predict we can now use the .onnx output file we generated earlier with

```
import onnxruntime as ort
import numpy as np
T = 500
X = np.linspace(-5, 5, T) # Oberservation points
Y= (X)**3 + np.random.normal(-0, 10, T)  # Noisy function to estimate
h=0.5

session = ort.InferenceSession("./kernel_smoother.onnx")
prediction_onnx, = session.run(input_feed={"X": X.reshape(-1,), "Y": Y.reshape(-1,), "h": [h]}, output_names=["y"])

plt.plot( np.roll(  prediction_onnx, T//2) )
```

### References

[1] {. Fan and {. Gijbels, Local polynomial modelling and its applications, London [u.a.]: Chapman & hall, 1996. \
 [[Bibtex]](javascript:void(0))

```
@book{Fan1996,
added-at = {2009-08-21T10:31:17.000+0200},
address = {London [u.a.]},
author = {Fan, {Jianqing} and Gijbels, {Irène}},
biburl = {http://www.bibsonomy.org/bibtex/23e163e04b09550b54a8067f0cbd97b7e/fbw_hannover},
interhash = {de68bea35adadb13da464f65107efce4},
intrahash = {3e163e04b09550b54a8067f0cbd97b7e},
isbn = {0412983214},
keywords = {Equations Mathematische_Statistik Polynomials Regression_analysis},
number = 66,
pagetotal = {XV, 341},
ppn_gvk = {19282144X},
publisher = {Chapman \& Hall},
series = {Monographs on statistics and applied probability series},
timestamp = {2009-08-21T10:31:17.000+0200},
title = {Local polynomial modelling and its applications},
url = {http://gso.gbv.de/DB=2.1/CMD?ACT=SRCHA&SRT=YOP&IKT=1016&TRM=ppn+19282144X&sourceid=fbw_bibsonomy},
year = 1996
}
```