import string

num_chapter = 2

def normalize(text):
    # Strip spaces, lowercase, and remove punctuation
    text = text.strip().lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def load_words_from_timestamp_file(filepath):
    words = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('_')
            if len(parts) >= 3:
                word = '_'.join(parts[:-2])
                words.append(word)
    return words

def load_words_from_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text.strip().split()

def check_word_by_word(timestamp_words, full_text_words):
    for i, word in enumerate(timestamp_words):
        if i >= len(full_text_words):
            print(f"Transcript ended early. Missing word: '{word}' at position {i}")
            return
        norm1 = normalize(word)
        norm2 = normalize(full_text_words[i])
        if norm1 != norm2:
            print(f"Mismatch at position {i}: expected '{norm1}' but found '{norm2}'")
            return
    print("All words matched successfully.")

def remove_punctuation(word):
    word = word.replace('—', '').replace('»', '').replace('«', '').replace('◦', '').replace('-', '').replace("-", "").replace('(', '').replace(')', '').replace('"', '').replace("!", '').replace("'", '').replace(':', '').replace(",", "").replace(";", "").replace("?", "").replace(".", " ")
    return word

def check_alignment(timestamp_words, full_text_words):
    """
    Compares the two word streams in *both* directions.

    - If one list ends before the other, report where it happens.
    - If any pair of words (after normalization) differ, report the position.
    - Otherwise confirm that the two lists are identical in content and length.
    """
    n1, n2 = len(timestamp_words), len(full_text_words)
    n_cmp   = min(n1, n2)

    # 1) compare word-by-word up to the shorter length
    for i in range(n_cmp):
        w_ts  = normalize(timestamp_words[i])
        w_txt = normalize(full_text_words[i])
        if w_ts != w_txt:
            print(f"Mismatch at position {i}: timestamp='{w_ts}'  text='{w_txt}'")
            return

    # 2) check for length differences
    if n1 > n2:
        print(f"Text ended early. Extra {n1 - n2} words in timestamps starting at position {n2}.")
    elif n2 > n1:
        print(f"Timestamps ended early. Extra {n2 - n1} words in text starting at position {n1}.")
    else:
        print("Perfect match: every word aligns and the lists are the same length.")

# File paths # 782 1882
timestamp_file = f'../../stimuli_transcriptions/black_audio_timestamps.txt'
full_text_file = f'../../stimuli_transcriptions/black_audio.txt'
# original_transcription_file = f'../german_chapters/raw_ground_truth_text/Chapter_{num_chapter}.txt'

# with open(original_transcription_file, 'r') as f:
#     text = f.read()
#     text = remove_punctuation(text)
#     with open('../german_chapters/raw_ground_truth_text/Chapter_2_no_punc.txt', 'w') as fi:
#         fi.write(text)


# Run check
timestamp_words = load_words_from_timestamp_file(timestamp_file)
full_text_words = load_words_from_text_file(full_text_file)
check_word_by_word(timestamp_words, full_text_words)
check_alignment(timestamp_words, full_text_words)
