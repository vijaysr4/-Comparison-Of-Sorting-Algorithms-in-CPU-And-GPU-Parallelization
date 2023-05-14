import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

# Define the kernel function to execute on the GPU
mod = SourceModule("""
    __global__ void square(float *a)
    {
        int idx = threadIdx.x;
        a[idx] = a[idx]*a[idx];
    }
    """)

# Create an array of numbers to square
a = np.array([1, 2, 3, 4, 5]).astype(np.float32)

# Allocate memory on the GPU and copy the data over
a_gpu = drv.mem_alloc(a.nbytes)
drv.memcpy_htod(a_gpu, a)

# Call the kernel function on the GPU
func = mod.get_function("square")
func(a_gpu, block=(5,1,1))

# Copy the result back to the CPU
a_result = np.empty_like(a)
drv.memcpy_dtoh(a_result, a_gpu)

print("Input array:", a)
print("Result array:", a_result)
