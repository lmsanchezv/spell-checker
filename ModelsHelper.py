import math
import re

# used for unseen words in training vocabularies
UNK = None
# sentence start and end
SENTENCE_START = "<s>"
SENTENCE_END = "</s>"

def read_sentences_from_file(file_path):
    with open(file_path, "r") as f:
        return [re.split("\s+", line.rstrip('\n')) for line in f]

# calculate number of unigrams & bigrams
def calculate_number_of_unigrams(sentences):
    unigram_count = 0
    for sentence in sentences:
        # remove two for <s> and </s>
        unigram_count += len(sentence) - 2
    return unigram_count

def calculate_number_of_bigrams(sentences):
        bigram_count = 0
        for sentence in sentences:
            # remove one for number of bigrams in sentence
            bigram_count += len(sentence) - 1
        return bigram_count

# print unigram and bigram probs
def print_unigram_probs(sorted_vocab_keys, model, fileName):
    with open(fileName, 'w') as f:
        for vocab_key in sorted_vocab_keys:
            if vocab_key != SENTENCE_START and vocab_key != SENTENCE_END:
                valueToPrint = "{}: {}".format(vocab_key if vocab_key != UNK else "UNK", model.calculate_unigram_probability(vocab_key))
                f.write(valueToPrint + "\n")
                print valueToPrint,
        print("")

def print_bigram_probs(sorted_vocab_keys, model, fileName):
    print "\t\t",
    with open(fileName, 'w') as f:
        for vocab_key in sorted_vocab_keys:
            if vocab_key != SENTENCE_START:
                print(vocab_key if vocab_key != UNK else "UNK" + "\t\t")
        print("")
        for vocab_key in sorted_vocab_keys:
            if vocab_key != SENTENCE_END:
                print(vocab_key if vocab_key != UNK else "UNK" + "\t\t")
                for vocab_key_second in sorted_vocab_keys:
                    if vocab_key_second != SENTENCE_START:
                        print(vocab_key_second if vocab_key_second != UNK else "UNK" + "\t\t")
                        print("{0:.5f}".format(model.calculate_bigram_probabilty(vocab_key, vocab_key_second)) + "\t\t")
                        valueToPrint = "{} {}: {}".format(vocab_key if vocab_key != UNK else "UNK", vocab_key_second if vocab_key_second != UNK else "UNK", model.calculate_bigram_probabilty(vocab_key, vocab_key_second))
                        f.write(valueToPrint + "\n")
                print("")
        print("")

# calculate perplexty
def calculate_unigram_perplexity(model, sentences):
    unigram_count = calculate_number_of_unigrams(sentences)
    sentence_probability_log_sum = 0
    for sentence in sentences:
        try:
            sentence_probability_log_sum -= math.log(model.calculate_sentence_probability(sentence), 2)
        except:
            sentence_probability_log_sum -= float('-inf')
    return math.pow(2, sentence_probability_log_sum / unigram_count)

def calculate_bigram_perplexity(model, sentences):
    number_of_bigrams = calculate_number_of_bigrams(sentences)
    bigram_sentence_probability_log_sum = 0
    for sentence in sentences:
        try:
            bigram_sentence_probability_log_sum -= math.log(model.calculate_bigram_sentence_probability(sentence), 2)
        except:
            bigram_sentence_probability_log_sum -= float('-inf')
    return math.pow(2, bigram_sentence_probability_log_sum / number_of_bigrams)