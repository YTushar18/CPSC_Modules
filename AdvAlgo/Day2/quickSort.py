def quickSort(arr, low, high):
    if low < high:
        # Partition the array into two halves and get the pivot index
        pivotIndex = partition(arr, low, high)

        # Recursively sort the subarrays on both sides of the pivot
        quickSort(arr, low, pivotIndex - 1)
        quickSort(arr, pivotIndex + 1, high)

def partition(arr, low, high):
    # Choose the rightmost element as the pivot
    pivot = arr[high]

    # Initialize the index of the smaller element
    i = low - 1

    # Iterate through the array
    for j in range(low, high):
        # If the current element is smaller than or equal to the pivot
        if arr[j] <= pivot:
            # Swap arr[i] and arr[j]
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    # Swap arr[i + 1] and arr[high] to place the pivot in the correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    # Return the index of the pivot
    return i + 1

# Example usage
arr = [5, 4, 3, 2, 1]
quickSort(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
