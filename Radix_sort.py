# -*- coding: utf-8 -*-
import time
import random
from multiprocessing import Pool


def radix_sort(arr):
    RADIX = 10
    max_length = False
    temp, placement = -1, 1

    while not max_length:
        max_length = True
        buckets = [list() for _ in range(RADIX)]

        for i in arr:
            temp = i / placement
            buckets[int(temp % RADIX)].append(i)
            if max_length and temp > 0:
                max_length = False

        a = 0
        for b in range(RADIX):
            bucket = buckets[b]
            for i in bucket:
                arr[a] = i
                a += 1

        placement *= RADIX

    return arr


def radix_sort_parallel(arr, processes=4):
    RADIX = 10
    max_length = False
    temp, placement = -1, 1

    while not max_length:
        max_length = True
        buckets = [list() for _ in range(RADIX)]

        with Pool(processes) as p:
            results = p.map(get_digit, [(i, RADIX, placement) for i in arr])

        for i, digit in zip(arr, results):
            buckets[digit].append(i)
            if max_length and digit > 0:
                max_length = False

        a = 0
        for b in range(RADIX):
            bucket = buckets[b]
            for i in bucket:
                arr[a] = i
                a += 1

        placement *= RADIX

    return arr


def get_digit(args):
    i, RADIX, placement = args
    return int((i / placement) % RADIX)


if __name__ == '__main__':
    # Generate a list of 1,000,000 random integers
    arr = [random.randint(1, 100000) for _ in range(1000)]

    # Sequential radix sort
    start_time = time.time()
    sorted_arr = radix_sort(arr)
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential radix sort took {sequential_time:.5f} seconds")

    # Parallel radix sort
    start_time = time.time()
    sorted_arr_parallel = radix_sort_parallel(arr)
    print(sorted_arr_parallel)
    end_time = time.time()
    parallel_time = end_time - start_time
    print(f"Parallel radix sort took {parallel_time:.5f} seconds")

    # Check if both sorted arrays are the same
    assert sorted_arr == sorted_arr_parallel

