# %%
import numpy as np
import matplotlib.pyplot as plt
import timeit
from scipy.interpolate import interp1d
import ndonnx as ndx
from polyfills import ndx_elementwise_max_0, ndx_elementwise_complex_multiply, fft, ifft  # Hinzugefügte Importe

np.random.seed(0)

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

ndx_elementwise_max_0(ndx_X)

# %%
# Elementwise multiplication
# Entferne die Definition von ndx_elementwise_complex_multiply

# %%
# Entferne die Definition von epan_kernel
def epan_kernel(u, b):
    u = u / b
    return ndx_elementwise_max_0( 1. / b * 3. / 4 * (1 - u ** 2) )

kernel = epan_kernel(ndx_grid, 0.32)

plt.plot(ndx_grid, kernel)

# %%

# Entferne die Definition von fft und ifft

onnx_result = fft(ndx.reshape(kernel, (1, -1, 1)))

onnx_result2 = ifft(onnx_result)
#print(onnx_result.to_numpy()[:,0,:])
print(onnx_result2.to_numpy()[0,:,:])

# %%
onnx_result = fft(ndx.reshape(kernel, (1, -1, 1)))
onnx_result_y = fft(ndx.reshape(ndx_Ynew, (1, -1, 1)))

mult_res = ndx_elementwise_complex_multiply(onnx_result, onnx_result_y)

to_test = mult_res.to_numpy()  #Bis hier hin ziemlich identisch
# %%

as_complex = to_test[:,0]+ to_test[:,1]*1j
# %%
plt.plot(np.fft.ifft(as_complex).real)
# %%
inv = ifft(mult_res)[0,:,0]  # realteil

plt.plot(inv)

# %%
ifft(ndx.asarray([[0. ,1.], [0., 1.], [4., 3.], [0.,1. ]]))[:,:1,0]
# %%
arr = np.array([[2, 4, 6, 8],[7, 3, 5, 9]])
arr1 = np.array([[3, 7, 5, 4],[8, 6, 9, 2]])
arr2 = arr * arr1
# %%
# Entferne die Definition von fftshift
def fftshift(x):
    xy = x.__array_namespace__()
    shift_index =  len(x)//2#- xy.argmin(xy.abs(x))-1
    return xy.roll(x, shift_index)

fftshift(ndx_X)

# %%
plt.plot(fftshift(inv))
# %%
epan_kernel(ndx_grid, 3)
# %%

# Estimation using FFT
start = timeit.default_timer()

def kernel_regression(ndx_grid, ndx_Ynew, ndx_X, h):
    xy = ndx_grid.__array_namespace__()
    kernel = epan_kernel(ndx_grid, h)
    kernel_ft = fft(ndx.reshape(kernel, (1, -1, 1)))
    y_ft = fft(ndx.reshape(ndx_Ynew, (1, -1, 1)))
    func_tmp = ndx_elementwise_complex_multiply(kernel_ft, y_ft)
    m_fft = (xy.max(ndx_X)-xy.min(ndx_X))*fftshift(ifft(func_tmp)[0,:,0])/Tout   # realteil
    return m_fft

kernel_result = kernel_regression(ndx_grid, ndx_Ynew, ndx_X, Tout**(-1/5))
# %%


#np_kernel_result = kernel_regression(grid, Ynew, X, Tout**(-1/5))

plt.plot(ndx_grid, kernel_result)

stop = timeit.default_timer()
print('Time: ', stop - start)
 
plt.show()
# %%


# Instantiate placeholder ndonnx array
x = ndx.array(shape=("N",), dtype=ndx.int64)
y = mean_drop_outliers(x)

# Build and save my ONNX model to disk
model = ndx.build({"x": x}, {"y": y})
onnx.save(model, "mean_drop_outliers.onnx")