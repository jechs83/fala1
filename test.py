from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://192.168.8.66:27017/")
db = client['saga']
collection = db['scrap']

# Cargar los datos
productos = list(collection.find())
precios = [producto['best_price'] for producto in productos]
precios2 = [producto['list_price'] for producto in productos]
descuentos = [producto['web_dsct'] for producto in productos]

# Preprocesar los datos
scaler = StandardScaler()
data = scaler.fit_transform(list(zip(precios, precios2, descuentos)))

# Entrenar el modelo
model = IsolationForest(contamination=0.01)
model.fit(data)

# Función para predecir si un producto tiene un precio o descuento bug
def es_bug(producto):
    precio = producto['best_price']
    descuento = producto['web_dsct']
    precio2 = producto['list_price']

    data = scaler.transform([[precio, precio2, descuento]])  # Cambio aquí
    pred = model.predict(data)
    return pred[0] == -1

for producto in productos:
    # Verificar si el producto es un "bug"
    if es_bug(producto):
        # Imprimir el producto, el precio y el descuento
        print(f"Producto: {producto['product']}, Precio: {producto['best_price']},Precio2: {producto['list_price']}, Descuento: {producto['web_dsct']}")