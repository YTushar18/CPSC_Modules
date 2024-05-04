class RabinKarp:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)
        self.hash_value = 0
        self.pattern_hash_value = 0
        self.window = []
        self.base = 256  
        self.prime = 101  # A prime number for modulo operation

    def calculate_hash_value(self, string, length):
        value = 0
        for i in range(length):
            value = (self.base * value + ord(string[i])) % self.prime
        return value

    def recalculate_hash_value(self, old_hash, old_char, new_char):
        new_hash = (
            self.base
            * (old_hash - ord(old_char) * (self.base ** (self.pattern_length - 1)))
            + ord(new_char)
        ) % self.prime
        return new_hash

    def search_pattern(self):
        count = 0

        self.pattern_hash_value = self.calculate_hash_value(
            self.pattern, self.pattern_length
        )
        self.hash_value = self.calculate_hash_value(self.text, self.pattern_length)
        pattern_found = False  # Flag to check if pattern is found
        for i in range(self.text_length - self.pattern_length + 1):
            if self.pattern_hash_value == self.hash_value:
                for j in range(self.pattern_length):
                    if self.text[i + j] != self.pattern[j]:
                        break
                else:
                    # print(f"Pattern found at index {i}")
                    count += 1
                    pattern_found = True
            if i < self.text_length - self.pattern_length:
                self.hash_value = self.recalculate_hash_value(
                    self.hash_value, self.text[i], self.text[i + self.pattern_length]
                )

        if not pattern_found:
            print("Pattern not found in the text.")

        return count


# if __name__ == "__main__":
#     text = input("Enter the text: ")
#     pattern = input("Enter the pattern: ")
#     rk_search = RabinKarp(text, pattern)

#     print(rk_search.search_pattern())
