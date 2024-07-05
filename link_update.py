from pymongo import MongoClient

# Conectar al cliente de MongoDB
client = MongoClient("mongodb://192.168.8.7:27017/")

# Seleccionar la base de datos y la colección
db = client.saga
collection = db.links

def actualizar_documento(url, lista, page):
    # Crear el documento a actualizar
    documento = {
        "url": url,
        "lista": lista,
        "page": page
    }
    
    # Actualizar el documento si la URL ya existe, de lo contrario, insertarlo
    result = collection.update_one(
        {"url": url},
        {"$set": documento},
        upsert=True
    )
    
    if result.matched_count > 0:
        print(f"Documento con URL '{url}' actualizado.")
    else:
        print(f"Nuevo documento con URL '{url}' insertado.")

def leer_lista_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            # Separar los valores de cada línea
            url, lista_str, page_str = linea.strip().split(',')
            
            # Convertir lista_str y page_str a enteros
            lista = int(lista_str)
            page = int(page_str)
            
            # Llamar a la función para actualizar el documento
            actualizar_documento(url, lista, page)

# Llamar a la función para leer el archivo y actualizar la base de datos
leer_lista_desde_archivo("/Users/javier/GIT/fala/lista.txt")
