import sys
import re
import concurrent.futures
import time


# Read text file
def input(index):
    try:
        reader = open(sys.argv[index], "r", encoding="utf8")
    except OSError:
        print("txt file not found")
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


# Cada proceso recibe la cadena y la procesa
def mapping(part_of_text, id_process):
    print(id_process, "Entered mapping function")
    part_of_text = part_of_text.lower()
    processed_text = re.sub('[,.;:!¡?¿()]+', '', part_of_text)
    print("Splitting text")
    words = processed_text.split()
    print("Text splitted")
    word_map_result = []
    for i in range(len(words)):
        word_map_result.append([words[i], 1])

    return shuffle(word_map_result, id_process)


# Convert text to list of words
def splitting(input_text):
    n_processes = 10

    # Creating processes
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("Creating processes...")
        results = []
        for id_process, part_of_text in enumerate(divide_chunks(input_text, int(len(input_text) / n_processes))):
            results.append(executor.submit(mapping, part_of_text, id_process))

        all_dictionaries = []
        for f in concurrent.futures.as_completed(results):
            all_dictionaries.append(f.result())

    return merge_dictionaries(all_dictionaries)


def save_result_file(result_dictionary_words, index):
    try:
        f = open("file1_result%d.txt" % index, 'w', encoding="utf-8")
    except OSError:
        print("Error in write result file")
        sys.exit()

    for word in result_dictionary_words:
        line = word + ' : ' + str(result_dictionary_words[word]) + "\n"
        f.write(line)


# Recibe el texto y el tamaño a procesar por cada proceso
# Busca donde hay un espacio en blanco para no cortar el texto y lo devuelve
def divide_chunks(text, chunk):
    start = 0
    while True:
        i = chunk
        if start + i >= len(text):
            return text[start:]
        while text[start + i] != ' ':
            i -= 1
        yield text[start:start + i]
        start += i + 1


def main():
    if len(sys.argv) == 1:
        print("Please, specify a text file...")
        sys.exit()

    # Start count time
    start_time = time.time()

    # For each .txt
    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = input(index)
        result_dictionary_words = splitting(text)
        save_result_file(result_dictionary_words, index)

        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
