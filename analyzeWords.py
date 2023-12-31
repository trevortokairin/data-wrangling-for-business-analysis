from collections import Counter


def analyzeWords(words):
    # Ensure words are lower case
    words = words.str.lower()

    # a. letter_counts
    letter_counts = Counter(words.str[0])
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        if letter not in letter_counts:
            letter_counts[letter] = 0

    # b. max_char
    max_char = words.str.len().max()

    # c. size_counts
    size_counts = Counter(words.str.len())

    # d. oo_count and e. oo_words
    oo_words = words[words.str.contains('oo')]
    oo_count = len(oo_words)

    # f. words_6plus and g. words_6plus_count
    words_6plus = words[words.str.len() >= 6]
    words_6plus_count = len(words_6plus)

    return {
        'letter_counts': dict(letter_counts),
        'max_char': max_char,
        'size_counts': dict(size_counts),
        'oo_count': oo_count,
        'oo_words': oo_words,
        'words_6plus': words_6plus,
        'words_6plus_count': words_6plus_count
    }

