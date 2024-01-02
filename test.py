import pymongo
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from decouple import config
import re

# Conectar a la base de datos
client = MongoClient(config("MONGO_DB"))
database = client["saga"]
collection = database["scrap"]

# Filtrar datos para laptops
product_values = re.compile(r'laptop', re.IGNORECASE)
query = {"product": {"$in": [product_values]}}
data = list(collection.find(query))

# Crear un DataFrame con los datos
df = pd.DataFrame(data)



# Utilizar solo los campos list_price, best_price, card_price para simplificar
features = ["list_price", "best_price", "card_price"]


X = df[features].values
y = df["best_price"].values


# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)




# Realizar predicciones en el conjunto de prueba
# predictions = model.predict(X_test)
# print(len(predictions), len(y_test))

# # Analizar posibles errores en los precios
# errores = df.loc[(predictions < y_test), ["product", "precio_actual", "list_price", "best_price", "card_price"]]
predictions = model.predict(X_test)


# Check if lengths match
if len(predictions) == len(y_test):
    # Analizar posibles errores en los precios
    errores = df.loc[:, ["product", "list_price", "best_price", "card_price"]]
    errores = errores[predictions < y_test]
    print(errores)
else:
    print("Error: Lengths of predictions and y_test do not match.")