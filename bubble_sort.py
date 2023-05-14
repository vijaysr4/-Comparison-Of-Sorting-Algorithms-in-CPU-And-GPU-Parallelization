import random 
import time
import psutil
import GPUtil

def bubble_sort(arr):
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        
        # Last i elements are already in place
        for j in range(0, n-i-1):
            
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    
    return arr

# Generate an array of 1000 unsorted numbers
data = [random.randint(-10000, 10000) for _ in range(10000)]

# get the start time
st_qs = time.time()

sorted_arr = bubble_sort(data)

# get the end time
et_qs = time.time()

elapsed_time_qs = (et_qs - st_qs) * 1000
print('\nExecution time BS:', elapsed_time_qs, 'milliseconds')

#print(sorted_arr)

# Testing the psutil library for both CPU and RAM performance details
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
# Testing the GPUtil library for both GPU performance details
GPUtil.showUtilization()

