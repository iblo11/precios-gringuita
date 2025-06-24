from src.leer_catalogo import procesar_catalogo
from src.leer_csv import leer_compras
from src.procesar_compras import unir_catalogo_y_compras, calcular_columnas_adicionales

catalogo_path = "precios-gringuita/data/catalogo_insumos.xlsx"
catalogo_df = procesar_catalogo(catalogo_path)

compras_path = "precios-gringuita/data/RESUMEN_COMPRAS_PRODUCTO 03-25.xlsx"
compras_df = leer_compras(compras_path)


# Combinar
df_unido = unir_catalogo_y_compras(catalogo_df, compras_df)

# Calcular
df_final = calcular_columnas_adicionales(df_unido)
df_final = df_final[df_final["PRODUCTO ID"] != "PRODUCTO ID"]


# Mostrar resultado final
print(df_final.head())

output_path = "/Users/ivonnelivieres/Desktop/extension/precios-gringuita/data/compras_con_costos.xlsx"


try:
    df_final.to_excel(output_path, index=False)
    print(f"\n✅ Archivo guardado exitosamente en:\n{output_path}")
except Exception as e:
    print(f"\n❌ Error al guardar el archivo: {e}")