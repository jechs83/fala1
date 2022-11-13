# from multiprocessing import Process
# import os


# def funcion(numero):
#     print(os.getpid())
#     for n in range (10):
#         valor = n*n+n
#         print(valor, "---->", numero)
  

# if __name__ == "__main__":
#     procesos=[]

#     cores=os.cpu_count()
#     print("Tienes ",cores, " cores")

#     print("--------- Instanciar")


#     for n in range ( cores ):
#         proceso = Process(target = funcion, args=(n,))
#         procesos.append(proceso)
#     print("------- Ejecutar")

#     for proceso in procesos:
#         proceso.start()

#     print("------- Espera")

#     for proceso in procesos:
#         proceso.join()

#     print("------ regreso a la ejecucion")



array = [["hola", "chau", "adios"], ["bya","assas","asad"]]


array = str(array)

print(array.replace("[","{").replace("]","}"))