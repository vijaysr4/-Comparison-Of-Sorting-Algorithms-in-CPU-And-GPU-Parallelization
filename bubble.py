import random
import time
import concurrent.futures

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Parallel Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        left = executor.submit(merge_sort, left).result()
        right = executor.submit(merge_sort, right).result()

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Generate a large dataset
random.seed(42)
large_dataset = [random.randint(0, 100000) for _ in range(100000)]

# Measure runtime for Bubble Sort
start_time = time.time()
bubble_sort(large_dataset.copy())
end_time = time.time()
print("Bubble Sort runtime:", end_time - start_time, "seconds")

# Measure runtime for Parallel Merge Sort
start_time = time.time()
sorted_arr = merge_sort(large_dataset.copy())
end_time = time.time()
print("Parallel Merge Sort runtime:", end_time - start_time, "seconds")
