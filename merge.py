import random
import concurrent.futures
import time

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

def sequential_merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    return merge(left, right)


def parallel_merge_sort(arr, num_processes=None):
    if len(arr) <= 1:
        return arr

    if num_processes is None:
        num_processes = min(32, len(arr))

    if num_processes <= 1:
        return sequential_merge_sort(arr)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        mid = len(arr) // 2
        left = executor.submit(parallel_merge_sort, arr[:mid], num_processes//2)
        right = executor.submit(parallel_merge_sort, arr[mid:], num_processes//2)
        left = left.result()
        right = right.result()

    return merge(left, right)



if __name__ == "__main__":
    # Generate a random list of integers
    arr = [random.randint(0, 10000) for _ in range(10000000)]

    # Sort using sequential merge sort and measure the run time
    start_time = time.time()
    sorted_seq = sequential_merge_sort(arr.copy())
    end_time = time.time()
    seq_run_time = end_time - start_time
    print(f"Sequential merge sort run time: {seq_run_time:.4f} seconds")

    # Sort using parallel merge sort and measure the run time
    start_time = time.time()
    sorted_par = parallel_merge_sort(arr.copy())
    end_time = time.time()
    par_run_time = end_time - start_time
    print(f"Parallel merge sort run time: {par_run_time:.4f} seconds")

    # Validate that both sorted lists are equal
    assert sorted_seq == sorted_par
    print("Sequential and parallel merge sort produce the same result.")
