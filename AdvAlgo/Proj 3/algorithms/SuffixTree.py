from suffix_trees import STree

def count_pattern_occurrences(text, pattern):
    # Create a suffix tree from the text
    st = STree.STree(text)

    # Search for the pattern in the suffix tree
    occurrences = st.find_all(pattern)

    return len(occurrences)

# # Sample text and pattern
# text = "this is a sample text with multiple sample words and another sample."
# pattern = "sample"

# # Count occurrences of the pattern in the text
# occurrence_count = count_pattern_occurrences(text, pattern)

# print("Count of occurrences of the pattern:", occurrence_count)
