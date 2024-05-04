def naive_string_matching(text, pattern):
    n = len(text)
    m = len(pattern)

    occurrences = []  # List to store the starting indices of matches

    for i in range(n - m + 1):
        if text[i : i + m] == pattern:
            occurrences.append(i)

    return len(occurrences)


# Get user input
# text = input("Enter the text: ")
# pattern = input("Enter the pattern: ")

# # Find and display occurrences
# occurrences = naive_string_matching(text, pattern)
# if occurrences:
#     print(f"Pattern found at indices: {occurrences}")
# else:
#     print("Pattern not found in the text.")
