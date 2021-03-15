import logging
import threading
import datetime
import time

def consultar(texto):
    time.sleep(3)
    return


tiempo_ini = datetime.datetime.now()

t1 = threading.Thread(name="thread 1", target=consultar, args=("hola", ))



t1.start()

t1.join()

tiempo_fin = datetime.datetime.now()


print("tiempo transcurrido " + str(tiempo_fin.second - tiempo_ini.second))