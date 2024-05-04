def build_suffix_array(text):
    text += "$"
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    suffixes.sort()
    suffix_array = [suffix[1] for suffix in suffixes]
    return suffix_array

def count_pattern_occurrences(text, pattern):
    suffix_array = build_suffix_array(text)
    pattern_len = len(pattern)
    n = len(text)
    
    def binary_search_first(pattern):
        low, high = 0, n - 1
        first_occurrence = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = text[suffix_array[mid]:]
            compare = suffix[:pattern_len]
            if compare == pattern:
                first_occurrence = mid
                high = mid - 1
            elif compare < pattern:
                low = mid + 1
            else:
                high = mid - 1
        return first_occurrence
    
    def binary_search_last(pattern):
        low, high = 0, n - 1
        last_occurrence = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = text[suffix_array[mid]:]
            compare = suffix[:pattern_len]
            if compare == pattern:
                last_occurrence = mid
                low = mid + 1
            elif compare < pattern:
                low = mid + 1
            else:
                high = mid - 1
        return last_occurrence
    
    first_occurrence = binary_search_first(pattern)
    last_occurrence = binary_search_last(pattern)
    
    if first_occurrence == -1:
        return 0
    else:
        return last_occurrence - first_occurrence + 1

# Sample text and pattern
# text = "this is a sample text with multiple sample words and another sample. sample sample sample sample sample sample sample"
# pattern = "sample"
# occurrence_count = count_pattern_occurrences(text, pattern)
# print("Count of occurrences of the pattern:", occurrence_count)
