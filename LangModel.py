import Bigrams
from ModelsHelper import read_sentences_from_file, print_bigram_probs,calculate_unigram_perplexity,calculate_bigram_perplexity


#input file to create the LangModel
INPUT_FILE = "output pequeno.txt"

if __name__ == '__main__':
    toy_dataset = read_sentences_from_file(INPUT_FILE)
    toy_dataset_test = read_sentences_from_file(INPUT_FILE)
    
    toy_dataset_model_unsmoothed = Bigrams.BigramLanguageModel(toy_dataset)
    toy_dataset_model_smoothed = Bigrams.BigramLanguageModel(toy_dataset, smoothing=True)

    sorted_vocab_keys = toy_dataset_model_unsmoothed.sorted_vocabulary()

    # print("---------------- Toy dataset ---------------\n")
    # print("=== UNIGRAM MODEL ===")
    # print("- Unsmoothed  -")
    # print_unigram_probs(sorted_vocab_keys, toy_dataset_model_unsmoothed, 'unigramas.txt')
    # print("\n- Smoothed  -")
    # print_unigram_probs(sorted_vocab_keys, toy_dataset_model_smoothed, 'unigramas smoothed.txt')

    # print("")

    print("=== BIGRAM MODEL ===")
    # print("- Unsmoothed  -")
    # print_bigram_probs(sorted_vocab_keys, toy_dataset_model_unsmoothed, 'bigramas.txt')
    print("- Smoothed  -")
    print_bigram_probs(sorted_vocab_keys, toy_dataset_model_smoothed, 'bigramas smoothed.txt')

    print("")

    print("== SENTENCE PROBABILITIES == ")
    longest_sentence_len = max([len(" ".join(sentence)) for sentence in toy_dataset_test]) + 5
    print("sent", " " * (longest_sentence_len - len("sent") - 2), "uprob\t\tbiprob")
    for sentence in toy_dataset_test:
        sentence_string = " ".join(sentence)
        print(sentence_string + " " * (longest_sentence_len - len(sentence_string)))
        print("{0:.5f}".format(toy_dataset_model_smoothed.calculate_sentence_probability(sentence)) + "\t\t")
        print("{0:.5f}".format(toy_dataset_model_smoothed.calculate_bigram_sentence_probability(sentence)))        
        
    print("")

    print("== TEST PERPLEXITY == ")
    print("unigram: ", calculate_unigram_perplexity(toy_dataset_model_smoothed, toy_dataset_test))
    print("bigram: ", calculate_bigram_perplexity(toy_dataset_model_smoothed, toy_dataset_test))
    
    print("")

    # actual_dataset = read_sentences_from_file("train.txt")
    # actual_dataset_test = read_sentences_from_file("test.txt")
    # actual_dataset_model_smoothed = BigramLanguageModel(actual_dataset, smoothing=True)
    # print("---------------- Actual dataset ----------------\n")
    # print("PERPLEXITY of train.txt")
    # print("unigram: ", calculate_unigram_perplexity(actual_dataset_model_smoothed, actual_dataset))
    # print("bigram: ", calculate_bigram_perplexity(actual_dataset_model_smoothed, actual_dataset))

    # print("")

    # print("PERPLEXITY of test.txt")
    # print("unigram: ", calculate_unigram_perplexity(actual_dataset_model_smoothed, actual_dataset_test))
    # print("bigram: ", calculate_bigram_perplexity(actual_dataset_model_smoothed, actual_dataset_test))
