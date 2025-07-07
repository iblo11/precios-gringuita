from fuzzywuzzy import process

def encontrar_nombre_similar(nombre_busqueda, nombres_disponibles):
    match, score = process.extractOne(nombre_busqueda, nombres_disponibles)
    return match if score >= 85 else None