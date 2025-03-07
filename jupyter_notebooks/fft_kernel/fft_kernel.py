# %%
import numpy as np
import matplotlib.pyplot as plt
import timeit
from scipy.interpolate import interp1d
 
# Simulation
T = 500
X = np.linspace(-5, 5, T) 
Y= (X)**3 + np.random.normal(-0, 10, T)
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
 
def epan_kernel(u, b):
    u = u / b
    return max(0, 1. / b * 3. / 4 * (1 - u ** 2))
 
 
# Estimation using FFT
start = timeit.default_timer()
 
t = grid
h= Tout**(-1/5)
kernel = [epan_kernel(x, h) for x in t]
kernel_ft = np.fft.fft(kernel)
func_tmp = kernel_ft* np.fft.fft(Ynew)
m_fft = (max(X)-min(X))*np.fft.fftshift(np.fft.ifft(func_tmp).real)/Tout
plt.plot(t, m_fft)
 
stop = timeit.default_timer()
print('Time: ', stop - start)
 
plt.show()
# %%
