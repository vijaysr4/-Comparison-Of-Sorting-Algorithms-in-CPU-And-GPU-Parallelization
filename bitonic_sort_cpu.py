import time
import random
import multiprocessing as mp

def bitonic_sort(seq):
    if len(seq) <= 1:
        return seq
    else:
        mid = len(seq) // 2
        left = bitonic_sort(seq[:mid])
        right = bitonic_sort(seq[mid:])
        return bitonic_merge(left + right)

def bitonic_merge(seq):
    if len(seq) <= 1:
        return seq
    else:
        seq = bitonic_compare(seq, True)
        mid = len(seq) // 2
        left = bitonic_merge(seq[:mid])
        right = bitonic_merge(seq[mid:])
        return left + right

def bitonic_compare(seq, step):
    if len(seq) <= 1:
        return seq
    else:
        mid = len(seq) // 2
        for i in range(mid):
            if (seq[i] > seq[i + mid]) == step:
                seq[i], seq[i + mid] = seq[i + mid], seq[i]
        left = bitonic_compare(seq[:mid], step)
        right = bitonic_compare(seq[mid:], step)
        return left + right

def parallel_bitonic_sort(seq):
    if len(seq) <= 1:
        return seq
    
    mid = len(seq) // 2
    with mp.get_context('fork').Pool(2) as p:
        left = p.apply_async(parallel_bitonic_sort, (seq[:mid],))
        right = parallel_bitonic_sort(seq[mid:])
    
    left_seq = left.get()
    right_seq = right
    seq = left_seq + right_seq
    
    return bitonic_merge(seq)

# Sample usage and runtime measurement
if __name__ == '__main__':
    seq = [random.randint(0, 1000000) for _ in range(10000)]
    start_time = time.time()
    sorted_seq = bitonic_sort(seq)
    end_time = time.time()
    print("Sequential bitonic sort")
    print("Execution time: ", end_time - start_time, "seconds")

    start_time = time.time()
    sorted_seq = parallel_bitonic_sort(seq)
    end_time = time.time()
    print("Parallel bitonic sort")
    print("Execution time: ", end_time - start_time, "seconds")
