import threading
import time
import random
import numpy as np
import psutil
import GPUtil
import warnings
warnings.filterwarnings('ignore')



# Generate an array of 1000 unsorted numbers
data = [random.randint(-100000, 100000000) for _ in range(10000000)]
print("Unsorted array:")


# Function to find the partition position
def partition(array, low, high):

	# choose the rightmost element as pivot
	pivot = array[high]

	# pointer for greater element
	i = low - 1

	# traverse through all elements
	# compare each element with pivot
	for j in range(low, high):
		if array[j] <= pivot:

			# If element smaller than pivot is found
			# swap it with the greater element pointed by i
			i = i + 1

			# Swapping element at i with element at j
			(array[i], array[j]) = (array[j], array[i])

	# Swap the pivot element with the greater element specified by i
	(array[i + 1], array[high]) = (array[high], array[i + 1])

	# Return the position from where partition is done
	return i + 1

# function to perform quicksort


def quickSort(array, low, high):
	if low < high:

		# Find pivot element such that
		# element smaller than pivot are on the left
		# element greater than pivot are on the right
		pi = partition(array, low, high)

		# Recursive call on the left of pivot
		quickSort(array, low, pi - 1)

		# Recursive call on the right of pivot
		quickSort(array, pi + 1, high)




size = len(data)

# get the start time
st_qs = time.time()

#quickSort(data, 0, size - 1)

# get the end time
et_qs = time.time()
elapsed_time_qs = (et_qs - st_qs) * 1000
print('\nExecution time QS:', elapsed_time_qs, 'milliseconds')

print('\nSorted Array QS in Ascending Order:')
#print(data, "\n")


import threading


# Function to find the partition position
def Mpartition(array, low, high):

    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1


# function to perform quicksort
def MquickSort(array, low, high, depth=0):
    if low < high:
        if depth >= 2:  # When depth exceeds the maximum allowed value, run quicksort synchronously
            pi = Mpartition(array, low, high)
            MquickSort(array, low, pi - 1, depth + 1)
            MquickSort(array, pi + 1, high, depth + 1)
        else:  # When depth is still within the maximum allowed value, run quicksort concurrently
            # Find pivot element such that element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = Mpartition(array, low, high)

            # Create two threads for quicksort on the left and right partitions respectively
            left_thread = threading.Thread(target = MquickSort, args=(array, low, pi - 1, depth + 1))
            right_thread = threading.Thread(target = MquickSort, args=(array, pi + 1, high, depth + 1))

            # Start the threads
            left_thread.start()
            right_thread.start()

            # Wait for the threads to complete
            left_thread.join()
            right_thread.join()




size = len(data)

# get the start time
st_mqs = time.time()

MquickSort(data, 0, size - 1)

# get the end time
et_mqs = time.time()
elapsed_time_mqs = (et_mqs - st_mqs) * 1000
print('\nExecution time MQS:', elapsed_time_mqs, 'milliseconds')

print('\nSorted Array MQS in Ascending Order:')
#print(data)




from numba import njit, prange

@njit(parallel=True)
def parallel_quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    left = parallel_quicksort(left)
    right = parallel_quicksort(right)
    
    return left + middle + right

# get the start time
st_qs = time.time()
sorted_arr = parallel_quicksort(data)
#print(sorted_arr[1:10])

# get the end time
et_qs = time.time()
elapsed_time_qs_GPU = (et_qs - st_qs) * 1000
print('\nExecution time QS GPU:', elapsed_time_qs_GPU, 'milliseconds')

'''

import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

def quicksort_parallel_gpu(arr):
    # Convert the input list to a NumPy array
    arr = np.array(arr)

    n = len(arr)

    try:
        # Allocate memory on the GPU
        arr_gpu = cuda.mem_alloc(arr.nbytes)
    except cuda.MemoryError:
        print("Error: Failed to allocate memory on the GPU. Please reduce the input size or use a GPU with more memory.")
        return None
    
    cuda.memcpy_htod(arr_gpu, arr)

    # Define the CUDA kernel function
    mod = SourceModule("""
        __global__ void quicksort(int* arr, int left, int right) {
            if (left >= right) {
                return;
            }
            int i = left, j = right;
            int tmp;
            int pivot = arr[(left + right) / 2];

            while (i <= j) {
                while (arr[i] < pivot) {
                    i++;
                }
                while (arr[j] > pivot) {
                    j--;
                }
                if (i <= j) {
                    tmp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = tmp;
                    i++;
                    j--;
                }
            }

            if (left < j) {
                quicksort(arr, left, j);
            }
            if (i < right) {
                quicksort(arr, i, right);
            }
        }
    """)

    # Get a reference to the kernel function
    quicksort_kernel = mod.get_function("quicksort")

    # Call the kernel function with the appropriate parameters
    quicksort_kernel(arr_gpu, np.int32(0), np.int32(n-1), block=(128,1,1), grid=(n//128+1,1))

    # Copy the sorted array back to the CPU and return it
    sorted_arr = np.empty_like(arr)
    cuda.memcpy_dtoh(sorted_arr, arr_gpu)
    return sorted_arr.tolist()



# get the start time
st_qs = time.time()
sorted_arr = quicksort_parallel_gpu(data)

# get the end time
et_qs = time.time()
elapsed_time_qs_GPU = (et_qs - st_qs) * 1000
print('\nExecution time QS GPU:', elapsed_time_qs_GPU, 'milliseconds')
'''
# Testing the psutil library for both CPU and RAM performance details
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
# Testing the GPUtil library for both GPU performance details
GPUtil.showUtilization()





