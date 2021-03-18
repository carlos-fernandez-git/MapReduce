import sys
import re
import threading
import time


def reduce(shared_dict):
    if threading.current_thread().name == "Thread3":
        for i in sorted(shared_dict)[0: int(len(shared_dict) / 2)]:
            shared_dict[i] = sum(shared_dict[i])

    if threading.current_thread().name == "Thread4":
        for j in sorted(shared_dict)[int(len(shared_dict) / 2):]:
            shared_dict[j] = sum(shared_dict[j])


# Iteramos sobre la lista, si la clave no está, se crea una lista con [1], si la clave existe, se añade 1 a la lista
def shuffle(shared_dict, list_thread1, list_thread2):
    if threading.current_thread().name == "Thread 1":
        for word in list_thread1:
            if word[0] in shared_dict:
                shared_dict[word[0]].append(1)
            else:
                shared_dict[word[0]] = [1]
    if threading.current_thread().name == "Thread 2":
        for word in list_thread2:
            if word[0] in shared_dict:
                shared_dict[word[0]].append(1)
            else:
                shared_dict[word[0]] = [1]


def mapping(texto, list_thread1, list_thread2, shared_dict):
    if threading.current_thread().name == "Thread 1":
        palabras = texto.split()
        for palabra in palabras:
            list_thread1.append([palabra, 1])

    if threading.current_thread().name == "Thread 2":
        palabras = texto.split()
        for palabra in palabras:
            list_thread2.append([palabra, 1])

    shuffle(shared_dict, list_thread1, list_thread2)


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

    # Dividimos el texto en dos partes
    primera_parte, segunda_parte = input_text[:int(len(input_text) / 2)], input_text[int(len(input_text) / 2):]

    list_thread1 = []
    list_thread2 = []
    # Dividimos el texto entre los diferentes threads
    shared_dict = {}
    t1 = threading.Thread(name="Thread 1", target=mapping,
                          args=(primera_parte, list_thread1, list_thread2, shared_dict))
    t2 = threading.Thread(name="Thread 2", target=mapping,
                          args=(segunda_parte, list_thread1, list_thread2, shared_dict))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # Volvemos a crear nuevos threads para la parte de reduce
    t3 = threading.Thread(name="Thread3", target=reduce, args=(shared_dict,))
    t4 = threading.Thread(name="Thread4", target=reduce, args=(shared_dict,))

    t3.start()
    t4.start()

    t3.join()
    t4.join()

    return shared_dict


if __name__ == '__main__':
    start_time = time.time()

    for index in range(1, len(sys.argv)):
        print(sys.argv[index], ":", sep="")
        text = input(index)
        result_dictionary_words = splitting(text)
        #for word in result_dictionary_words:
         #   print(word, ':', result_dictionary_words[word])
    print("--- %s seconds ---" % (time.time() - start_time))
