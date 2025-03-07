# %%
import numpy as np
import matplotlib.pyplot as plt
import timeit
from scipy.interpolate import interp1d
import spox.opset.ai.onnx.v20 as op
import ndonnx as ndx
from ndonnx._propagation import eager_propagate

# Initializing an array with data
# Simulation
T = 500
X = np.linspace(-5, 5, T) 
Y= (X)**3 + np.random.normal(-0, 10, T)
ndx_X= ndx.asarray(X)
plt.scatter(X, Y, c="blue")
 
plt.xlabel('sample')
plt.ylabel('X')
 
# Presetting
Tout = int( 2 ** np.floor(np.log(T)/np.log(2)) )
print(Tout)
 
# Interpolate Y
f = interp1d(X, Y)
grid = np.linspace(-5, 5, num=Tout)
Ynew=f(grid)

ndx_grid = ndx.asarray(grid)

ndx_Ynew = ndx.asarray(Ynew)

def ndx_elementwise_max_0(y):
    xy = y.__array_namespace__()
    return (y-xy.abs(y))/2

ndx_elementwise_max_0(ndx_X)
# %%
def epan_kernel(u, b):
    u = u / b
    return ndx_elementwise_max_0( 1. / b * 3. / 4 * (1 - u ** 2) )

epan_kernel(X, 0.5)
# %%

@eager_propagate
def fft(x: ndx.Array, inverse: int=0, onesided: int=0) -> ndx.Array:
    var = x.spox_var()
    fft_var = op.dft(var, inverse=inverse, onesided=onesided)
    return ndx.from_spox_var(fft_var)

def ifft(x):
    return fft(x, inverse=1, onesided=0)

onnx_result = fft(ndx.reshape(ndx_Ynew, (-1, 1)))
onnx_result2 = ifft(onnx_result)
#print(onnx_result.to_numpy())
print(onnx_result2.to_numpy()[:,0,0])

# %%
def fftshift(x):
    xy = x.__array_namespace__()
    min_index =  len(x)//2- xy.argmin(xy.abs(x))-1
    return xy.roll(x, min_index)

fftshift(ndx_X)
# %%
epan_kernel(ndx_grid, 3)
# %%

# Estimation using FFT
start = timeit.default_timer()

def kernel_regression(ndx_grid, ndx_Ynew, ndx_X, h):
    xy = ndx_grid.__array_namespace__()
    kernel = epan_kernel(ndx_grid, h)
    print(kernel)
    kernel_ft = fft(xy.reshape(kernel, (-1, 1)))
    print(kernel_ft.to_numpy())
    func_tmp = kernel_ft * fft(xy.reshape(ndx_Ynew, (-1, 1)))
    m_fft = (xy.max(ndx_X)-xy.min(ndx_X))*fftshift(ifft(func_tmp)[:,0,0])/Tout
    return m_fft

kernel_result = kernel_regression(ndx_grid, ndx_Ynew, ndx_X, Tout**(-1/5))
# %%


#np_kernel_result = kernel_regression(grid, Ynew, X, Tout**(-1/5))

plt.plot(ndx_grid, kernel_result)
 
stop = timeit.default_timer()
print('Time: ', stop - start)
 
plt.show()
# %%

import ndonnx as ndx
import numpy as np

def mean_drop_outliers(a, low=-5, high=5):
    xp = a.__array_namespace__()
    return xp.mean(a[(low < a) & (a < high)])

np_result = mean_drop_outliers(np.asarray([-10, 0.5, 1, 4]))
onnx_result = mean_drop_outliers(ndx.asarray([-10, 0.5, 1, 4]))
np.testing.assert_equal(np_result, onnx_result.to_numpy())
print(onnx_result.to_numpy())

# %%