class ColeccionRecetas:
    def __init__(self):
        self.recetas = []

    def agregar_receta(self, receta):
        self.recetas.append(receta)

    def resetear(self):
        self.recetas = []

    def exportar_excel(self, ruta):
        if not self.recetas:
            raise ValueError("No hay recetas para exportar.")
    
        import pandas as pd
        filas = [receta.to_dict() for receta in self.recetas]
        df = pd.DataFrame(filas)
        df.to_excel(ruta, index=False)