import sys
import re
from unicodedata import normalize

def leer_archivos(index):
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

# Convertimos el texto
def extraccion(texto):
    texto = texto.lower()
    palabras = texto.split()

    print(palabras)



if __name__ == '__main__':
    for index in range(1, len(sys.argv)):
        texto = leer_archivos(index)
        extraccion(texto)


