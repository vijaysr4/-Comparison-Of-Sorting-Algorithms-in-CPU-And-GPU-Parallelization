import random
import timeit
import multiprocessing

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quicksort(less) + equal + quicksort(greater)

def parallel_quicksort(arr, num_parts):
    chunk_size = len(arr) // num_parts

    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_parts - 1)]
    chunks.append(arr[(num_parts - 1) * chunk_size:])

    with multiprocessing.Pool() as pool:
        sorted_chunks = pool.map(quicksort, chunks)

    sorted_data = []
    for chunk in sorted_chunks:
        sorted_data.extend(chunk)

    return sorted_data

def measure_runtime():
    data = [random.randint(0, 100000) for _ in range(10000000)]

    start_time = timeit.default_timer()
    quicksort(data)
    elapsed_time = timeit.default_timer() - start_time
    print(f"Sequential quicksort elapsed time: {elapsed_time:.4f} seconds")

    num_parts = multiprocessing.cpu_count()
    start_time = timeit.default_timer()
    parallel_quicksort(data, num_parts)
    elapsed_time = timeit.default_timer() - start_time
    print(f"Parallel quicksort elapsed time: {elapsed_time:.4f} seconds")

if __name__ == '__main__':
    measure_runtime()
