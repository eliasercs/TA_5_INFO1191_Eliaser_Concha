import pandas as pd
import numpy as np
from markov_base import Pedido, siguiente_estado, construir_matriz, generar_pedidos, ESTADOS

class Simulador:
    def __init__(self, num_pedidos: int = 100):
        """
        Inicializa el simulador con una cantidad de pedidos.
        """
        self.num_pedidos = num_pedidos
        self.matriz = construir_matriz()
        self.pedidos = generar_pedidos(num_pedidos)
        self.resultados = None

    def ejecutar(self, max_pasos: int = 100):
        """
        Ejecuta la simulación para todos los pedidos hasta que finalicen o alcancen max_pasos.
        """
        # Asegurar que el estado inicial esté en el historial
        for p in self.pedidos:
            if not p.historial:
                p.historial.append(p.estado_actual)

        paso = 0
        while any(not p.esta_finalizado() for p in self.pedidos) and paso < max_pasos:
            for p in self.pedidos:
                if not p.esta_finalizado():
                    nuevo = siguiente_estado(p.estado_actual, self.matriz)
                    p.actualizar_estado(nuevo)
            paso += 1
        return self.pedidos

    def calcular_metricas(self):
        """
        Calcula métricas clave requeridas por el integrante 2.
        """
        total = len(self.pedidos)
        entregados = sum(1 for p in self.pedidos if p.estado_actual == "Entregado")
        cancelados = sum(1 for p in self.pedidos if p.estado_actual == "Devuelto")
        
        # Registro de tiempos (pasos) por estado
        tiempos_por_estado = {estado: [] for estado in ESTADOS}
        
        for p in self.pedidos:
            conteo_pedido = {estado: 0 for estado in ESTADOS}
            for estado in p.historial:
                conteo_pedido[estado] += 1
            
            for estado, count in conteo_pedido.items():
                tiempos_por_estado[estado].append(count)
        
        promedios_estado = {estado: np.mean(tiempos) if tiempos else 0 for estado, tiempos in tiempos_por_estado.items()}
        
        return {
            "total_pedidos": total,
            "entregas_exitosas": entregados,
            "cancelaciones": cancelados,
            "porcentaje_exito": (entregados / total) * 100 if total > 0 else 0,
            "tiempo_promedio_por_estado": promedios_estado
        }

    def generar_reporte_dataframe(self):
        """
        Genera un DataFrame con los resultados detallados de cada pedido.
        """
        data = []
        for p in self.pedidos:
            data.append({
                "id": p.id,
                "estado_final": p.estado_actual,
                "pasos_totales": len(p.historial) - 1,
                "historial": " -> ".join(p.historial)
            })
        self.resultados = pd.DataFrame(data)
        return self.resultados

    def exportar_csv(self, filename: str = "resultados_simulacion.csv"):
        """
        Exporta los resultados a un archivo CSV.
        """
        if self.resultados is None:
            self.generar_reporte_dataframe()
        self.resultados.to_csv(filename, index=False)
        print(f"Resultados exportados a {filename}")
