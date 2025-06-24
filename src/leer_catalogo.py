import pandas as pd
import os

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

    # Verificamos si hay valores faltantes
    print("\nValores faltantes por columna:")
    print(catalogo.isnull().sum())

    return catalogo
