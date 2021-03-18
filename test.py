# Leemos el archivo de texto (input)
import sys
import time


def input():
    try:
        reader = open(sys.argv[1], "r", encoding="utf8")
    except OSError:
        print("El archivo no se ha podido abrir correctamente")
        sys.exit()

    texto = reader.read()
    reader.close()
    return texto


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

if __name__ == '__main__':
    start_time = time.time()
    text = input()
    word_count(text)

    print("--- %s seconds ---" % (time.time() - start_time))


