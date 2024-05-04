'''
    Sorting Algorithms Used :
    1. Bubble Sort -
    2. Counting Sort -
    3. Bucket Sort -
    4. Quick Sort -
    5. Heap Sort -
    6. Radix Sort -
    7. Insertion Sort -
    8. Quick Select -
'''

# Bubbkle Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

#=========================================================================
# Insertion Sort
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

#=========================================================================
# Merge Sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

#=========================================================================
# Quick sort 
# helper function for quick sort
def partition(array, low, high):

    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])

    return i + 1

def quick_sort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quick_sort(array, low, pi - 1)
        quick_sort(array, pi + 1, high)
    return array

#=========================================================================
# Heap Sort

# helper function for heap sort
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    
    return arr

#=========================================================================
# Radix sort

#helper function for radix sort
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    max_num = max(arr)

    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

#=========================================================================
# Quick Select
# helper function for quick selection sort
def partition(arr, l, r): 
	x = arr[r] 
	i = l 
	for j in range(l, r): 
		if arr[j] <= x: 
			arr[i], arr[j] = arr[j], arr[i] 
			i += 1
	arr[i], arr[r] = arr[r], arr[i] 
	return i 

def quick_select(arr, l, r, k): 
 
	if (k > 0 and k <= r - l + 1): 

		index = partition(arr, l, r) 
		if (index - l == k - 1): 
			return arr[index] 

		if (index - l > k - 1): 
			return quick_select(arr, l, index - 1, k) 
 
		return quick_select(arr, index + 1, r, 
							k - index + l - 1) 
	return -1

#=========================================================================
# Counting Sort
 
def countingSort(array):
    size = len(array)
    max_element = max(array)
    min_element = min(array)
    range_of_elements = max_element - min_element + 1

    output = [0] * size
    count = [0] * range_of_elements
    
    
    for i in range(0, size):                     # Store the count of each element in the count array
        count[array[i] - min_element] += 1
   
    for i in range(1, range_of_elements):        # Store the cumulative count
        count[i] += count[i - 1]
                           
    i = size - 1                                 # Find the index of each element of the original array in count array
    while i >= 0:                                # place the elements in the output array
        output[count[array[i] - min_element] - 1] = array[i]
        count[array[i] - min_element] -= 1
        i -= 1
    
    for i in range(0, size):                     # Copy the sorted elements into the original array
        array[i] = output[i]
    return array

#==============================================================================
# Bucket Sort
def bucket_sort(array):
    n = len(array)
    float_bucket = []
    int_bucket = []

    
    for num in array:                           # Separate floating-point numbers and integers into different buckets
        if isinstance(num, float):
            float_bucket.append(num)
        else:
            int_bucket.append(num)

    float_bucket.sort()                         # Sort the floating-point numbers (if any)
    int_bucket.sort()                           # Sort the integers (if any)
    
    sorted_array = float_bucket + int_bucket    # Concatenate the sorted floating-point numbers and integers

    return sorted_array

