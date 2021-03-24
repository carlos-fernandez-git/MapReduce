import sys
import re
import concurrent.futures
from multiprocessing import Manager
import multiprocessing
import time
import tempfile
import os


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


# Convert text to list of words
def splitting(input_text):
    input_text = input_text.lower()
    input_text = re.sub('[,.;:!¡?¿()]+', '', input_text)
    words = input_text.split()
    n_processes = 4
    # Creating processes
    word_map_result = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for id_process in range(n_processes):
            results.append(executor.submit(mapping, words, n_processes, id_process, word_map_result))

        for f in concurrent.futures.as_completed(results):
            print(f.result())


def mapping(words, n_processes, id_process, word_map_result):
    for i in range(int((id_process / n_processes) * len(words)),
                   int(((id_process + 1) / n_processes) * len(words))):
        word_map_result.append([words[i], 1])

    return shuffle(word_map_result)


def shuffle(word_map_result):
    result_dict = {}
    for word in word_map_result:
        if word[0] in result_dict:
            result_dict[word[0]].append(1)
        else:
            result_dict[word[0]] = [1]
    return result_dict


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please, specify a text file...")
        sys.exit()
    start_time = time.time()

    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = input(index)
        splitting(text)
        # for word in result_dictionary_words:
        #   print(word, ':', result_dictionary_words[word])

    print("--- %s seconds ---" % (time.time() - start_time))
