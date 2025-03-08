# %%
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


import matplotlib.pyplot as plt
plt.scatter(X, Y, c="blue")
plt.xlabel('sample')
plt.ylabel('X')
plt.plot(X, kernel_result)
plt.show()
# %%

# Export model to ONNX

# Instantiate placeholder ndonnx array
import onnx
X = ndx.array(shape=("N",), dtype=ndx.float64)
Y = ndx.array(shape=("N",), dtype=ndx.float64)
h = ndx.array(shape=("1"), dtype=ndx.float64)
# %%
y = kernel_smoother(X, Y, h)

# Build and save my ONNX model to disk
model = ndx.build({"X": X, "Y": Y, "h": h}, {"y": y})
onnx.save(model, "./kernel_smoother.onnx")
# %%

import onnxruntime as ort
import numpy as np
T = 500
X = np.linspace(-5, 5, T) # Oberservation points
Y= (X)**3 + np.random.normal(-0, 10, T)  # Noisy function to estimate
h=0.5

session = ort.InferenceSession("./kernel_smoother.onnx")
prediction_onnx, = session.run(input_feed={"X": X.reshape(-1,), "Y": Y.reshape(-1,), "h": [h]}, output_names=["y"])

plt.plot( prediction_onnx )

# %%