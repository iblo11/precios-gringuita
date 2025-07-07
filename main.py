from src.modelos import Ingrediente, Receta, ColeccionRecetas
from src.leer_catalogo import procesar_catalogo, cargar_recetas_desde_json
from src.leer_csv import leer_compras
from src.procesar_compras import unir_catalogo_y_compras, calcular_columnas_adicionales
import datetime

catalogo_path = "precios-gringuita/data/catalogo_insumos.xlsx"
catalogo_df = procesar_catalogo(catalogo_path)

compras_path = "precios-gringuita/data/RESUMEN_COMPRAS_PRODUCTO 03-25.xlsx"
compras_df = leer_compras(compras_path)

compras_procesadas = calcular_columnas_adicionales(unir_catalogo_y_compras(catalogo_df, compras_df))

precios = {
    str(nombre).strip().lower(): precio
    for nombre, precio in zip(
        compras_procesadas["PRODUCTO NOMBRE"],
        compras_procesadas["P. x KG/UNI/LIT ENTERO"]
    )
}

recetas = cargar_recetas_desde_json("precios-gringuita/data/recetas.json")

coleccion = ColeccionRecetas()
recetas_fallidas = []

subrecetas_dict = {}
pendientes = recetas.copy()
calculadas = set()

while pendientes:
    nuevas_calculadas = []

    for receta in pendientes:
        try:
            receta.calcular(precios, subrecetas_dict=subrecetas_dict)
            receta.asignar_precio_actual(precio_actual=7000)
            coleccion.agregar_receta(receta)
            subrecetas_dict[receta.nombre.strip().lower()] = receta
            nuevas_calculadas.append(receta)
            print(f"[OK] {receta.nombre}")
        except ValueError as e:
            print(f"[ERROR] {receta.nombre}: {e}")
            recetas_fallidas.append((receta.nombre, str(e)))

    if not nuevas_calculadas:
        break  # No se pudo calcular nada nuevo en este ciclo

    # Eliminamos las recetas que ya fueron procesadas
    for r in nuevas_calculadas:
        pendientes.remove(r)

# Si quedaron pendientes que no se pudieron calcular
if pendientes:
    print("\n⚠️ Recetas que no pudieron calcularse por falta de precios o subrecetas no resueltas:")
    for receta in pendientes:
        print(f" - {receta.nombre}")

"""for receta in recetas:
    es_subreceta = any(ing.es_subreceta for ing in receta.ingredientes)

    if not es_subreceta:
        try:
            receta.calcular(precios)
            receta.asignar_precio_actual(precio_actual=7000)  # placeholder
            subrecetas_dict[receta.nombre.lower()] = receta
        except ValueError as e:
            print(f"[SUBRECETA ERROR] {receta.nombre}: {e}")


for receta in recetas:
    try:
        receta.calcular(precios, subrecetas_dict=subrecetas_dict)
        receta.asignar_precio_actual(precio_actual=7000)
        coleccion.agregar_receta(receta)
    except ValueError as e:
        print(f"[ERROR] No se pudo calcular la receta '{receta.nombre}': {e}")
        recetas_fallidas.append(receta.nombre)

if recetas_fallidas:
    print("\nRecetas que no pudieron calcularse por falta de precios:")
    for nombre in recetas_fallidas:
        print(f" - {nombre}")

output_path = f"/Users/ivonnelivieres/Desktop/extension/precios-gringuita/data/output_{datetime.date.today()}.xlsx"
coleccion.exportar_excel(output_path)
"""