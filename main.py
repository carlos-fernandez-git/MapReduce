import sys
import re
import threading


# TODO https://stackoverflow.com/questions/21351275/split-a-string-to-even-sized-chunks

# Leemos el archivo de texto (input)
def input(index):
    print("Parametro", index, ":", sys.argv[index])
    try:
        reader = open(sys.argv[index], "r", encoding="utf8")
    except OSError:
        print("El archivo no se ha podido abrir correctamente")
        sys.exit()
    print("Archivo leido con exito")

    texto = reader.read()
    reader.close()
    return texto


# Convertimos el texto a lista de palabras
def splitting(texto):
    texto = texto.lower()
    # sub(caracteres_a_buscar, reemplazo, texto)
    texto = re.sub('[,.;:!¡?¿()]+', '', texto)

    # Dividimos el texto en dos partes
    primera_parte, segunda_parte = texto[:int(len(texto) / 2)], texto[int(len(texto) / 2):]

    list_thread1 = []
    list_thread2 = []
    # Dividimos el texto entre los diferentes threads
    t1 = threading.Thread(name="Thread 1", target=mapping, args=(primera_parte, list_thread1, list_thread2))
    t2 = threading.Thread(name="Thread 2", target=mapping, args=(segunda_parte, list_thread1, list_thread2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    word_result = list_thread1 + list_thread2
    return word_result


def shuffle(word_result):
    shuffle_dict = {}
    for palabra in word_result:
        if palabra[0] in shuffle_dict:
            shuffle_dict[palabra[0]].append(1)
        else:
            shuffle_dict[palabra[0]] = [1]

    return shuffle_dict


def mapping(texto, list_thread1, list_thread2):
    if threading.current_thread().name == "Thread 1":
        palabras = texto.split()
        for palabra in palabras:
            list_thread1.append([palabra, 1])

    if threading.current_thread().name == "Thread 2":
        palabras = texto.split()
        for palabra in palabras:
            list_thread2.append([palabra, 1])


if __name__ == '__main__':
    for index in range(1, len(sys.argv)):
        texto = input(index)
        result_list = splitting(texto)
        shuffle_dict = shuffle(result_list)
        print(shuffle_dict)
