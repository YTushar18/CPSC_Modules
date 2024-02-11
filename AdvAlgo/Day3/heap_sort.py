def max_heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2 
 
    if left < n and arr[largest] < arr[left]:
        largest = left
 
    if right < n and arr[largest] < arr[right]:
        largest = right
 
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]
        max_heapify(arr, n, largest)
 
def build_max_heap(arr):
    n = len(arr)
 
    for i in range(n, 0, -1): # OR for i in range(n//2,-1,-1)
        max_heapify(arr, n, i)
 
    
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  
        
        max_heapify(arr, i, 0)

arr = [45, 21, 7, 14, 38, 5]
build_max_heap(arr)
n = len(arr)
print ("Sorted array is")
for i in range(n):
    print ("%d" %arr[i])