import sys
import re
import threading
import time
import logging


# Leemos el archivo de texto (input)
def input(index):
    try:
        reader = open(sys.argv[index], "r", encoding="utf8")
    except OSError:
        print("El archivo no se ha podido abrir correctamente")
        sys.exit()

    texto = reader.read()
    reader.close()
    return texto


# Convertimos el texto a lista de palabras
def splitting(input_text):
    input_text = input_text.lower()
    # sub(caracteres_a_buscar, reemplazo, texto)
    input_text = re.sub('[,.;:!¡?¿()]+', '', input_text)

    list_all_words = input_text.split()
    list_of_ones = []
    n_threads = 6
    threads = list()
    # Creamos los threads y llamamos a mapping
    for i in range(n_threads):
        x = threading.Thread(target=mapping, args=(i, list_all_words, n_threads, list_of_ones))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

    # Creamos los threads y llamamos a Shuffle
    shuffle_dict_result = {}
    for i in range(n_threads):
        x = threading.Thread(target=shuffle, args=(list_of_ones, shuffle_dict_result, n_threads, i, threading.Lock()))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

    # Convertimos el diccionario a lista para poder recorrerlo con indice
    list_key_value = list(shuffle_dict_result.items())
    dict_final_result = {}
    # Parte de reduce:
    for i in range(n_threads):
        x = threading.Thread(target=reduce, args=(list_key_value, n_threads, i, dict_final_result))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()



def mapping(index, list_all_words, n_threads, list_of_ones):
    for i in range(int((index / n_threads) * len(list_all_words)),
                   int(((index + 1) / n_threads) * len(list_all_words))):
        list_of_ones.append([list_all_words[i], 1])


def shuffle(list_of_ones, shuffle_dict_result, n_threads, index, lock):
    for i in range(int((index / n_threads) * len(list_of_ones)),
                   int(((index + 1) / n_threads) * len(list_of_ones))):
        if list_of_ones[i][0] in shuffle_dict_result:
            lock.acquire()
            shuffle_dict_result[list_of_ones[i][0]].append(1)
            lock.release()
        else:
            lock.acquire()
            shuffle_dict_result[list_of_ones[i][0]] = [1]
            lock.release()


def reduce(list_key_value, n_threads, index, dict_final_reduced):
    for i in range(int((index / n_threads) * len(list_key_value)),
                   int(((index + 1) / n_threads) * len(list_key_value))):
        dict_final_reduced[list_key_value[i][0]] = sum(list_key_value[i][1])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("No se ha especificado ningún archivo de texto...")
        sys.exit()
    start_time = time.time()

    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = input(index)
        splitting(text)
        # for word in result_dictionary_words:
        #   print(word, ':', result_dictionary_words[word])

    print("--- %s seconds ---" % (time.time() - start_time))
