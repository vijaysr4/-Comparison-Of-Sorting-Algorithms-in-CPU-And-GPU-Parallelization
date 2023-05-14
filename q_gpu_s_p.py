import numpy as np
import time
from numba import cuda

@cuda.jit(device=True)
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

@cuda.jit
def gpu_quicksort_kernel(arr, low, high):
    idx = cuda.grid(1)
    if idx == 0:
        _quicksort(arr, low, high)

@cuda.jit(device=True)
def _quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        _quicksort(arr, low, pivot_index - 1)
        _quicksort(arr, pivot_index + 1, high)

def gpu_quicksort(arr):
    n = arr.shape[0]
    arr_gpu = cuda.to_device(arr.astype(np.float32))
    gpu_quicksort_kernel[1, 1](arr_gpu, 0, n - 1)
    return arr_gpu.copy_to_host()

def measure_runtime():
    data = np.random.randint(0, 100000, size=10000).astype(np.float32)

    start_time = time.perf_counter()
    sorted_data = gpu_quicksort(data)
    elapsed_time = time.perf_counter() - start_time
    print(f"GPU quicksort elapsed time: {elapsed_time:.4f} seconds")

if __name__ == '__main__':
    measure_runtime()
