import pandas as pd
import os
import json
from src.modelos import Receta, Ingrediente

# Ruta al archivo
#file_path = "/Users/ivonnelivieres/Desktop/extension/precios-gringuita/data/catalogo_insumos.xlsx"

def procesar_catalogo(file_path):
    """
    Lee y procesa el archivo de catálogo de insumos.
    
    - Llena valores faltantes en 'Cant x Compra' con 1.0.
    - Extrae insumos sin 'PRODUCTO ID' a otro archivo.
    - Elimina filas sin 'PRODUCTO ID' del catálogo.
    - Devuelve el DataFrame limpio.
    """

    # Verificamos la ruta
    print("Ruta absoluta buscada:", os.path.abspath(file_path))

    # Leemos el catálogo
    catalogo = pd.read_excel(file_path)

    # Mostramos los primeros datos
    print("\nPrimeras filas del catálogo:")
    print(catalogo.head())

    catalogo["Cant x Compra"] = catalogo["Cant x Compra"].fillna(1.0)

    insumos_fuera_norma = catalogo[catalogo["PRODUCTO ID"].isnull()]
    insumos_fuera_norma.to_excel("/Users/ivonnelivieres/Desktop/extension/precios-gringuita/data/insumos_fuera_de_norma.xlsx", index=False)
    catalogo.dropna(subset=["PRODUCTO ID"], inplace=True)

    catalogo = catalogo[catalogo["PRODUCTO ID"] != "PRODUCTO ID"]

    # Verificamos si hay valores faltantes
    print("\nValores faltantes por columna:")
    print(catalogo.isnull().sum())

    return catalogo

def cargar_recetas_desde_json(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    recetas = []
    for item in data:
        ingredientes = [
            Ingrediente(i["nombre"], i["cantidad"], i["unidad"], 0)
            for i in item["ingredientes"]
        ]
        receta = Receta(nombre=item["nombre"], codigo=item.get("codigo"), ingredientes=ingredientes)
        recetas.append(receta)
    return recetas