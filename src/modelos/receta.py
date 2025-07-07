from src.utils import encontrar_nombre_similar

class Receta:
    def __init__(self, nombre, ingredientes=None, codigo=None):
        self.nombre = nombre
        self.codigo = codigo
        self.ingredientes = ingredientes or []

        # Valores calculados
        self.costo_mp = 0
        self.mano_obra = 0
        self.indirectos = 0
        self.total_sin_ganancia = 0
        self.ganancia = 0
        self.total_sin_iva = 0
        self.iva = 0
        self.precio_minimo = 0
        self.precio_actual = 0
        self.margen = 0

    def calcular(self, precios, subrecetas_dict=None, porcentaje_mo=0.58, porcentaje_ci=0.4, ganancia_pct=0.4, iva_pct=0.1):
        subrecetas_dict = subrecetas_dict or {}
        nombres_disponibles = list(precios.keys())
        
        faltantes = []

        for ing in self.ingredientes:
            clave = ing.nombre.strip().lower()

            if getattr(ing, "es_subreceta", False):
                subreceta = subrecetas_dict.get(clave)
                if subreceta:
                    ing.precio_compra = subreceta.precio_minimo
                else:
                    faltantes.append(ing.nombre)
            else:
                match = encontrar_nombre_similar(clave, nombres_disponibles)
                if match:
                    ing.precio_compra = precios[match]
                else:
                    faltantes.append(ing.nombre)

        if faltantes:
            raise ValueError(f"No se encontraron precios para: {', '.join(faltantes)}")

        # Cálculos
        self.costo_mp = sum(ing.calcular_costo() for ing in self.ingredientes)
        self.mano_obra = self.costo_mp * porcentaje_mo
        self.indirectos = self.costo_mp * porcentaje_ci
        self.total_sin_ganancia = self.costo_mp + self.mano_obra + self.indirectos
        self.ganancia = self.total_sin_ganancia * ganancia_pct
        self.total_sin_iva = self.total_sin_ganancia + self.ganancia
        self.iva = self.total_sin_iva * iva_pct
        self.precio_minimo = self.total_sin_iva + self.iva

    def asignar_precio_actual(self, precio_actual):
        self.precio_actual = precio_actual
        if self.precio_minimo:
            self.margen = round(self.precio_actual / self.precio_minimo, 2)

    def to_dict(self):
        return {
            "Receta": self.nombre,
            "Costo MP": round(self.costo_mp, 2),
            "MO": round(self.mano_obra, 2),
            "Indirectos": round(self.indirectos, 2),
            "PV Mínimo": round(self.precio_minimo, 2),
            "Precio actual": round(self.precio_actual, 2),
            "Margen": round(self.margen, 2)
        }