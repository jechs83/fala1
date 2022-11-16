from casa import *
import time
def casa_sola():
    print()
    print("Quienes son mas casa solas?")
    print("escribe hombre o mujer")
    print()
    x = input()

    print()
    if x ==  "mujer":
        print()
        print(casa_sola_1,"tremenda casa sola")
        print()

    if x ==  "hombre":
        print()
        print(casa_sola_2,"tremendo casa sola")
        print()
    
    if x != "hombre" or "mujer":
        pass
i=1
while i == 1:
     casa_sola()
     time.sleep(2)
