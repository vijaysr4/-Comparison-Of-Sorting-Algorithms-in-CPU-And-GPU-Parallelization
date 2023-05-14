# -Comparison-Of-Sorting-Algorithms-in-CPU-And-GPU-Parallelization

The primary objective of this project is to investigate the performance and efficiency of 
various sorting algorithms, specifically quicksort, mergesort, and radix sort, when executed in 
different parallel processing environments, including sequential (single-threaded), CPU 
parallel, and GPU parallel implementations. By comparing the execution times of these 
algorithms across different platforms, we aim to understand the potential advantages and 
limitations of each algorithm in terms of scalability, and to offer valuable insights for future 
applications that require efficient sorting techniques.
For this study, we utilized a dataset of 10,000,000 randomly generated numbers and measured 
the elapsed time for each algorithm under different parallelization schemes. The results are as 
follows:
1. Quicksort:
- Sequential implementation: 52.6908 seconds
- CPU parallel implementation: 10.1877 seconds
- GPU parallel implementation: 5.0938 seconds
2. Mergesort:
- Sequential implementation: 88.2696 seconds
- CPU parallel implementation: 30.3716 seconds
- GPU parallel implementation: 8.8916 seconds
3. Radix sort:
- Sequential implementation: 219.59482 seconds
- CPU parallel implementation: 104.57991 seconds
- GPU parallel implementation: 86.27991 seconds

Our findings demonstrate that GPU parallelization offers the most significant performance 
improvements for all three sorting algorithms when compared to sequential and CPU parallel 
implementations. Moreover, radix sort exhibited the greatest speedup in the GPU parallel 
environment, followed by mergesort and quicksort. These results can provide valuable 
guidance for developers seeking to optimize sorting tasks in their applications by leveraging 
the power of parallel processing in CPUs and GPUs
