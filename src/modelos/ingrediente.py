class Ingrediente:
    def __init__(self, nombre, cantidad, unidad, precio_compra=0, es_subreceta=False):
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad = unidad
        self.precio_compra = precio_compra
        self.es_subreceta = es_subreceta

    def calcular_costo(self):
        return round(self.cantidad * self.precio_compra, 2)