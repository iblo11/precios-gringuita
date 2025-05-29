import pandas as pd
import os

# Ruta al archivo
file_path = "/Users/ivonnelivieres/Desktop/extension/precios-gringuita/data/RESUMEN_COMPRAS_PRODUCTO 03-25.xlsx"
print("Ruta absoluta buscada:", os.path.abspath(file_path))

# Ver las hojas disponibles (por si hay más de una)
excel_file = pd.ExcelFile(file_path)
print("Hojas disponibles:", excel_file.sheet_names)

# Leer la hoja correcta y la fila correcta
df = pd.read_excel(file_path, sheet_name=0, header=11)  

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Ver las primeras filas
print(df.head())