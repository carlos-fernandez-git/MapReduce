import sys
import re
import concurrent.futures
import time


# Read text file
def input(index):
    try:
        reader = open(sys.argv[index], "r", encoding="utf8")
    except OSError:
        print("Error")
        sys.exit()

    texto = reader.read()
    reader.close()
    return texto


def merge_dictionaries(all_dictionaries):
    dictionary_result = {}
    for d in all_dictionaries:
        for key, value in d.items():
            if key in dictionary_result:
                dictionary_result[key] = dictionary_result[key] + value
            else:
                dictionary_result[key] = value
    return dictionary_result


def reduce(shuffle_result_dict, id_process):
    print(id_process, "Entered reduce function")
    dict_final_reduced = {}
    for word in shuffle_result_dict:
        dict_final_reduced[word] = sum(shuffle_result_dict[word])
    return dict_final_reduced


def shuffle(word_map_result, id_process):
    print(id_process, "Entered shuffle function")
    result_dict = {}

    for word in word_map_result:
        if word[0] in result_dict:
            result_dict[word[0]].append(1)
        else:
            result_dict[word[0]] = [1]
    return reduce(result_dict, id_process)


def mapping(words, id_process):
    print(id_process, "Entered mapping function")
    word_map_result = []
    for i in range(len(words)):
        word_map_result.append([words[i], 1])

    return shuffle(word_map_result, id_process)


# Convert text to list of words
def splitting(input_text):

    input_text = input_text.lower()
    input_text = re.sub('[,.;:!¡?¿()]+', '', input_text)
    print("Splitting text")
    words = input_text.split()
    print("Text splitted")
    n_processes = 10
    # Creating processes

    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("Creating processes...")
        results = []
        for id_process in range(n_processes):
            results.append(executor.submit(mapping,
                                           words[int((id_process / n_processes) * len(words)): int(
                                               ((id_process + 1) / n_processes) * len(words))], id_process))

        all_dictionaries = []
        for f in concurrent.futures.as_completed(results):
            all_dictionaries.append(f.result())

    return merge_dictionaries(all_dictionaries)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please, specify a text file...")
        sys.exit()
    start_time = time.time()

    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = input(index)
        result_dictionary_words = splitting(text)
        for word in result_dictionary_words:
            print(word, ':', result_dictionary_words[word])

    print("--- %s seconds ---" % (time.time() - start_time))
