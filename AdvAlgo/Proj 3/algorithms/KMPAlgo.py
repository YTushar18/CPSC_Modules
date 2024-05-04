def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    pi = compute_prefix_function(pattern)
    j = 0  # Number of characters matched
    occurrences = []

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]  # Fall back in the pattern
        if text[i] == pattern[j]:
            j += 1  # Match next character
        if j == m:  # A match is found
            occurrences.append(i - m + 1)
            j = pi[j - 1]  # Prepare for the next possible match

    return len(occurrences)


# Get user input
# text = input("Enter the text: ")
# pattern = input("Enter the pattern: ")

# # Find and display occurrences
# occurrences = kmp_search(text, pattern)
# if occurrences:
#     print(f"Pattern found at indices: {occurrences}")
# else:
#     print("Pattern not found in the text.")
