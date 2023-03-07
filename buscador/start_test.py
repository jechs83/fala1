import subprocess
import time
import psutil

## FUNCION PARA EJECUTAR LOS PROCESOS Y REINICIARLOS CUANDO TERMINEN ##
def start():
    print("Ejecutando los procesos...")

    ## BUSCADORES DE BASE DE DATOS - ENVIA A TELGRAM LAS OFERTAS 
    subprocess.Popen(["python", "C:\Git\\fala\\buscador\\excelsior_telegram.py"], shell=True)
    subprocess.Popen(["python", "C:\Git\\fala\\buscador\\discovery_telegram.py"], shell=True)
    subprocess.Popen(["python", "C:\Git\\fala\\buscador\\enterprise_telegram.py"], shell=True)
    subprocess.Popen(["python", "C:\Git\\fala\\buscador\\voyager_telegram.py"], shell=True)

    ## BOTS PARA LOS COMANDOS DE LAS NAVES
  
    # subprocess.Popen(["python", "C:\Git\\fala\\buscador\\voyager.py"], shell=True)
    # subprocess.Popen(["python", "C:\Git\\fala\\buscador\\discovery.py"], shell=True)
    # subprocess.Popen(["python", "C:\Git\\fala\\buscador\\enterprise.py"], shell=True)

    ## ESPERAR HASTA QUE TODOS LOS PROCESOS ANTERIORES HAYAN TERMINADO
    for process in psutil.process_iter():
        if 'python' in process.name():
            process.wait()
    
    ## DETENER TODOS LOS PROCESOS EN EJECUCION ANTES DE REINICIAR
    subprocess.run(["taskkill", "/IM", "python.exe", "/F"])

    ## ESPERAR 20 MINUTOS PARA VOLVER A INICIAR LA FUNCION START
    print("Procesos completados. Reiniciando en 20 minutos...")
    time.sleep(20*60)

    ## LLAMAR LA FUNCION START NUEVAMENTE PARA REINICIAR EL PROCESO
    start()

start()   ## iniciar la función start. 