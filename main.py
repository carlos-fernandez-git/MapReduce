#!/usr/bin/env python3

# Autors:
# Carlos Fernández Morillas - 1428230
# Joel Ferrando Ruiz - 1460649

import sys
import re
import concurrent.futures


def read_text_file(index):
    try:
        reader = open(sys.argv[index], "r", encoding="utf8")
    except OSError:
        print("txt file not found")
        sys.exit()

    texto = reader.read()
    reader.close()
    return texto


# Itera sobre els diccionaris mirant sumant els valors de les mateixes claus dels diccionaris

def merge_dictionaries(all_dictionaries):
    dictionary_result = {}
    for d in all_dictionaries:
        for key, value in d.items():
            if key in dictionary_result:
                dictionary_result[key] = dictionary_result[key] + value
            else:
                dictionary_result[key] = value
    return dictionary_result


# Recorre el diccionari obtingut de la funció shuffle()
# Per cada clau (paraula) suma els valors (números 1)
# Guarda aquesta suma com a valor de cada clau
# Retorna el diccionari resultat

def reduce(shuffle_result_dict, id_process):
    dict_final_reduced = {}
    for word in shuffle_result_dict:
        dict_final_reduced[word] = sum(shuffle_result_dict[word])
    return dict_final_reduced


# Recorre la llista amb les paraules i l'1
# Si la clau (nom de la paraula) ja es troba al diccionari, afegeix un 1 al valor de la clau
# Si no, crea la clau amb el valor [1]
# Crida a funció reduce()

def shuffle(word_map_result, id_process):
    result_dict = {}

    for word in word_map_result:
        if word[0] in result_dict:
            result_dict[word[0]].append(1)
        else:
            result_dict[word[0]] = [1]
    return reduce(result_dict, id_process)


# Transforma els caràcters de la String a minúscules
# Elimina els caràcters especials per deixar només lletres
# Divideix la String en paraules i les guarda en una llista
# Crea llista amb [paraula, 1]
# Crida a funció shuffle()

def mapping(part_of_text, id_process):
    part_of_text = part_of_text.lower()
    processed_text = re.sub('[,.;:!¡?¿()]+', '', part_of_text)
    words = processed_text.split()
    word_map_result = []
    for i in range(len(words)):
        word_map_result.append([words[i], 1])

    return shuffle(word_map_result, id_process)


# Crea els diferents processos mitjançant la llibreria concurrent.futures Crida a funció divide_chunks() per dividir
# la string entre els diferents processos Cada procés executa la funció mapping() amb la seva part del text Un cop
# tots els processos tenen el seu diccionari, crida a la funció merge_dictionaries() per ajuntar els diccionaris de
# tots els processos

def splitting(input_text):
    try:
        if not input_text:
            raise ValueError('Empty file!')
    except ValueError as e:
        print(e)

    n_processes = 10
    # Creating processes
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for id_process, part_of_text in enumerate(divide_chunks(input_text,
                                                                int(len(input_text) / n_processes))):
            results.append(executor.submit(mapping, part_of_text, id_process))

        all_dictionaries = []
        for f in concurrent.futures.as_completed(results):
            all_dictionaries.append(f.result())

    return merge_dictionaries(all_dictionaries)


# Guarda els resultats a un .txt

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


def show_dictionary(result_dictionary_words):
    for word in result_dictionary_words:
        print(word + ' : ' + str(result_dictionary_words[word]))


def main():
    try:
        if len(sys.argv) == 1:
            print("Please, specify a text file...")
    except ValueError as e:
        print(e)
        sys.exit()

    # For each .txt
    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = read_text_file(index)
        result_dictionary_words = splitting(text)
        show_dictionary(result_dictionary_words)


if __name__ == '__main__':
    main()
