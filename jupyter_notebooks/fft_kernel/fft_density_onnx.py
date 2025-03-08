# %%
import numpy as np
import matplotlib.pyplot as plt
import timeit
import ndonnx as ndx
from polyfills import ndx_elementwise_max_0, fft, ifft, fftshift

# Simulation
N = 500
X = np.random.normal(-0, 1.5, N)
ndx_X = ndx.asarray(X)

plt.scatter(np.linspace(0, N, N), X, c="blue")
plt.xlabel('sample')
plt.ylabel('X')
plt.show()

# Presetting
Nout = 2**7

def epan_kernel(u, b):
    u = u / b
    return ndx_elementwise_max_0(1. / b * 3. / 4 * (1 - u ** 2))

# Usual estimation
def dens(s, X, h=0.5):
    return [epan_kernel((s - x) / h, 1) for x in X]
grid = np.linspace(min(X), max(X), num=Nout)
density = [(1. / X.size) * sum(dens(y, X)) for y in grid]
plt.plot(grid, density)


def density_estimation(X, Nout, h=0.5):
    
    t = np.linspace(min(X), max(X), Nout + 1)
    kernel = epan_kernel(t, h)
    kernel_ft = fft(ndx.reshape(ndx.asarray(kernel), (1, -1, 1))) 
    hist, bins = ndx.histogram(X, bins=t)
    ndx_hist = ndx.reshape(ndx.asarray(hist), (1, -1, 1)) 
    density_tmp = ndx_elementwise_complex_multiply(kernel_ft, fft(ndx_hist))
    density_fft = (1. / len(X)) * fftshift(ifft(density_tmp)[0,:,0])
    return (density_fft)

plt.plot(grid, density_estimation(X, Nout, h=0.5))
