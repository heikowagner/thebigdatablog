# %%
import numpy as np
# Simulation
T = 500
X = np.linspace(-5, 5, T) 
Y= (X)**3 + np.random.normal(-0, 10, T)

def epan_kernel(u, b):
    u = u / b
    return max(0, 1. / b * 3. / 4 * (1 - u ** 2))


def kernel_smoothing(X, Y, h=0.5):
    kernel = [epan_kernel(x, h) for x in X]
    func_tmp = np.fft.fft(kernel) * np.fft.fft(Y)
    m_fft = (max(X)-min(X))*np.fft.fftshift(np.fft.ifft(func_tmp).real)/len(X)
    return m_fft

kernel_smoothing(X, Y, h=0.5)