def find_longest_word(sentence):
    words = sentence.split()
    longest_word = ""
    max_length = 0
    for word in words:
        if len(word) > max_length:
            longest_word = word
            max_length = len(word)
    return longest_word

sentence = input()
result = find_longest_word(sentence)
print(result)
