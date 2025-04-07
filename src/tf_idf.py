from collections import Counter
import math
import pandas as pd

def create_vocabulary(data):
    vocabulary = set()

    for key, value in data.items():
        vocabulary.update(value["tokens"])  # All words from tokens are added to the vocabulary set

    return sorted(vocabulary)  # Words in the vocabulary are sorted


def calculate_tf(data, vocabulary):
    tf_values = {}

    for key, value in data.items():
        if 'tokens' in value:
            words = value['tokens']
            word_count = len(words)
            word_freq = Counter(words)

            tf_values[key] = {}             # Calculating TF for each word in the document
            for word in vocabulary:
                if word in word_freq:
                    tf_values[key][word] = word_freq[word] / word_count  # If the word exists, we calculate TF
                else:
                    tf_values[key][word] = 0

    return tf_values


def calculate_idf(data, vocabulary):
    idf_values = {}
    N = len(data)   # Total number of documents

    doc_freq = {word: 0 for word in vocabulary}     # Creating a dictionary to track how many documents each word appears in

    for value in data.values():     # Iterating through all documents and calculating DF for each word
        if 'tokens' in value:
            words_in_doc = set(value['tokens'])  # Only take unique words in the document
            for word in words_in_doc:
                if word in doc_freq:  # If the word is in the vocabulary, increase DF
                    doc_freq[word] += 1

    for word, df in doc_freq.items():       # Calculating IDF
        idf_values[word] = math.log(N / df)  # natural log (e)

    return idf_values


def calculate_tfidf_matrix(processed_data):

    vocabulary = create_vocabulary(processed_data)

    tf_values = calculate_tf(processed_data, vocabulary)

    idf_values = calculate_idf(processed_data, vocabulary)

    tfidf_matrix = []

    for doc_id, tf in tf_values.items():
        tfidf_matrix.append([tf[word] * idf_values[word] for word in vocabulary])

    tfidf_df = pd.DataFrame(tfidf_matrix, columns=vocabulary, index=processed_data.keys())

    return tfidf_df