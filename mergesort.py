import numpy as np
import cupy as cp
import time
from concurrent.futures import ThreadPoolExecutor

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

def parallel_merge_sort(arr, executor=None):
    if len(arr) <= 1:
        return arr
    if not executor:
        with ThreadPoolExecutor() as e:
            return parallel_merge_sort(arr, e)
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left_future = executor.submit(parallel_merge_sort, left, executor)
    right_future = executor.submit(parallel_merge_sort, right, executor)
    left = left_future.result()
    right = right_future.result()
    return merge(left, right)

def gpu_merge_sort(arr_gpu):
    if len(arr_gpu) <= 1:
        return arr_gpu
    mid = len(arr_gpu) // 2
    left = arr_gpu[:mid]
    right = arr_gpu[mid:]
    left = gpu_merge_sort(left)
    right = gpu_merge_sort(right)
    return cp.concatenate((left[left <= right.min()], right[right <= left.min()], left[left > right.min()], right[right > left.min()]))

# Generate random data
data = np.random.randint(0, 100000, 100000)
data_gpu = cp.array(data)

# CPU: Merge Sort
start = time.time()
sorted_data = merge_sort(data)
end = time.time()
print(f"CPU - Merge Sort: {end - start:.6f} seconds")

# CPU: Parallel Merge Sort
start = time.time()
sorted_parallel_data = parallel_merge_sort(data)
end = time.time()
print(f"CPU - Parallel Merge Sort: {end - start:.6f} seconds")

# GPU: Merge Sort
start = time.time()
sorted_data_gpu = gpu_merge_sort(data_gpu)
cp.cuda.Stream.null.synchronize()
end = time.time()
print(f"GPU - Merge Sort: {end - start:.6f} seconds")
