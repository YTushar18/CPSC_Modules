def merge_sort(arr):
    if len(arr) > 1:
        mid = len(a)//2
        Left = arr[:mid]
        Right = arr[mid:]

        merge_sort(Left)
        merge_sort(Right)

        i = j = k = 0

        while i<len(Left) and j<len(Right):
            if Left[i] < Right[i]:
                arr[k] = Left[i]
                i += 1
            else:
                arr[k] = Right[j]
                j += 1
            
            k += 1
        
        while i<len(Left):
            arr[k] = Left[i]
            i += 1
            k += 1

        while i<len(Right):
            arr[k] = Right[i]
            i += 1
            k += 1
        
                