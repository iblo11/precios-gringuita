import pandas as pd

def unir_catalogo_y_compras(catalogo_df, compras_df):
    """
    Une el catálogo de insumos con el archivo de compras por PRODUCTO ID.
    """
    catalogo_df = catalogo_df.drop(columns=["PRODUCTO NOMBRE"])

    df_unido = compras_df.merge(catalogo_df, on="PRODUCTO ID", how="left")

    return df_unido

def calcular_columnas_adicionales(df_resultado):
    """
    Calcula:
    - Precio unitario
    - Tipo de IVA: 0.10, 0.05 o 0.00
    - Precio sin IVA
    - Precio por unidad/kilo/litro
    """

    df_resultado["Total"] = pd.to_numeric(df_resultado["Total"], errors="coerce")
    df_resultado["CANTIDAD"] = pd.to_numeric(df_resultado["CANTIDAD"], errors="coerce")
    df_resultado["Cant x Compra"] = pd.to_numeric(df_resultado["Cant x Compra"], errors="coerce")
    df_resultado["Total Iva 10%"] = pd.to_numeric(df_resultado.get("Total Iva 10%", 0), errors="coerce")
    df_resultado["Total Iva 5%"] = pd.to_numeric(df_resultado.get("Total Iva 5%", 0), errors="coerce")

    # Precio unitario bruto (con IVA)
    df_resultado["P. UNI."] = df_resultado["Total"] / df_resultado["CANTIDAD"]

    # Determinar tipo de IVA por fila
    def detectar_iva(row):
        if row.get("Total Iva 10%", 0) > 0:
            return 0.10
        elif row.get("Total Iva 5%", 0) > 0:
            return 0.05
        else:
            return 0.00  # Exentas

    df_resultado["TIPO DE IVA"] = df_resultado.apply(detectar_iva, axis=1)

    # Precio unitario sin IVA
    df_resultado["P. UNI S IVA"] = df_resultado["P. UNI."] / (1 + df_resultado["TIPO DE IVA"])

    # Precio por unidad/kilo/litro entero
    df_resultado["P. x KG/UNI/LIT ENTERO"] = df_resultado["P. UNI S IVA"] / df_resultado["Cant x Compra"]

    return df_resultado