import spox.opset.ai.onnx.v20 as op
from ndonnx._propagation import eager_propagate
import ndonnx as ndx
import numpy as np

def ndx_elementwise_max_0(y):
    """
    Compute the element-wise maximum of an array and zero.

    This function takes an input array `y` and returns an array where each element
    is the maximum of the corresponding element in `y` and zero. It uses the array
    namespace's `abs` function to compute the absolute value of `-y` and then 
    averages `y` and the absolute value of `-y` to achieve the desired result.

    Parameters:
    y (array-like): Input array.

    Returns:
    array-like: An array where each element is the maximum of the corresponding 
                element in `y` and zero.
    """
    xy = y.__array_namespace__()
    return ((y+xy.abs(-y)))/2


def ndx_elementwise_complex_multiply(x, y):
    """
    Perform element-wise multiplication of two complex number arrays.

    This function takes two 3-dimensional arrays `x` and `y` representing complex numbers
    and performs element-wise multiplication. The complex numbers are assumed to be stored
    in the last dimension of the arrays, with the real part at index 0 and the imaginary part
    at index 1.

    Parameters:
    x (ndarray): A 3-dimensional array where the first dimension is 1, and the last dimension
                 contains the real and imaginary parts of the complex numbers.
    y (ndarray): A 3-dimensional array where the first dimension is 1, and the last dimension
                 contains the real and imaginary parts of the complex numbers.

    Returns:
    ndarray: A 3-dimensional array containing the result of the element-wise complex multiplication,
             with the same shape as the input arrays.
    """
    xy = x.__array_namespace__()
    x=x[0,:,:]
    y=y[0,:,:]
    real_part = x[:, 0] * y[:, 0] - x[:, 1] * y[:, 1]
    imag_part = x[:, 0] * y[:, 1] + x[:, 1] * y[:, 0]
    return xy.reshape(xy.stack([real_part, imag_part], axis=-1), (1, -1, 2))


@eager_propagate
def fft(x: ndx.Array, inverse: int=0, onesided: int=0) -> ndx.Array:
    """
    Perform a Fast Fourier Transform (FFT) on the input array.

    Parameters:
    x (ndx.Array): Input array on which to perform the FFT.
    inverse (int, optional): If non-zero, perform the inverse FFT. Default is 0.
    onesided (int, optional): If non-zero, return a one-sided FFT. Default is 0.
    axis (int, optional): Axis along which to compute the FFT. If None, the FFT is computed along the last axis. Default is None.

    Returns:
    ndx.Array: The result of the FFT operation as an ndx.Array.
    """
    var = x.spox_var()
    fft_var = op.dft(var, inverse=inverse, onesided=onesided)
    return ndx.from_spox_var(fft_var)

def ifft(x: ndx.Array) -> ndx.Array:
    """
    Compute the inverse Fast Fourier Transform (IFFT) of an array.

    Parameters:
    x (ndx.Array): Input array to transform.
    axis (int, optional): Axis over which to compute the IFFT. If not specified, the IFFT is computed over the last axis.

    Returns:
    ndx.Array: The transformed array after applying the IFFT.
    """
    return fft(x, inverse=1, onesided=0)

def fftshift(x):
    """
    Shift the zero-frequency component to the center of the spectrum.

    Parameters:
    x (ndx.Array): Input array.

    Returns:
    ndx.Array: The shifted array.
    """
    xy = x.__array_namespace__()
    shift_index =xy.floor(x.size / 2)
    return xy.roll(x, shift_index)
