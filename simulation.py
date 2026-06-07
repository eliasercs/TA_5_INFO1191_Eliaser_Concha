import pandas as pd
import numpy as np
from markov_base import Pedido, siguiente_estado, construir_matriz, generar_pedidos, ESTADOS

class Simulador:
    def __init__(self, num_pedidos: int = 100):
        """
        Inicializa el simulador con una cantidad de pedidos.
        También se crean estructuras para guardar la visualización de eventos.
        """
        self.num_pedidos = num_pedidos
        self.matriz = construir_matriz()
        self.pedidos = generar_pedidos(num_pedidos)
        self.resultados = None

        # Guarda cada cambio de estado ocurrido durante la simulación.
        # Esto permite demostrar la visualización de eventos paso a paso.
        self.eventos = []

        # Guarda cuántos pedidos hay en cada estado en cada paso de tiempo.
        # Esto se usa para construir la tabla y el gráfico de evolución.
        self.estados_por_paso = []

    def _registrar_conteo_estados(self, paso: int):
        """
        Cuenta cuántos pedidos hay en cada estado en un paso determinado.
        Esta información es la base de la visualización de eventos.
        """
        fila = {"paso": paso}
        for estado in ESTADOS:
            fila[estado] = sum(1 for p in self.pedidos if p.estado_actual == estado)
        self.estados_por_paso.append(fila)

    def ejecutar(self, max_pasos: int = 100):
        """
        Ejecuta la simulación para todos los pedidos hasta que finalicen
        o alcancen max_pasos.
        """
        # Asegurar que el estado inicial esté en el historial
        for p in self.pedidos:
            if not p.historial:
                p.historial.append(p.estado_actual)

        # Paso 0: todos los pedidos están en el estado inicial.
        self._registrar_conteo_estados(paso=0)

        paso = 0
        while any(not p.esta_finalizado() for p in self.pedidos) and paso < max_pasos:
            paso += 1

            for p in self.pedidos:
                if not p.esta_finalizado():
                    estado_anterior = p.estado_actual
                    nuevo = siguiente_estado(p.estado_actual, self.matriz)
                    p.actualizar_estado(nuevo)

                    # Registro del evento individual: pedido X pasó de un estado a otro.
                    self.eventos.append({
                        "paso": paso,
                        "id_pedido": p.id,
                        "estado_anterior": estado_anterior,
                        "estado_nuevo": nuevo,
                        "evento": f"{p.id}: {estado_anterior} -> {nuevo}"
                    })

            # Después de procesar todos los pedidos del paso actual,
            # se registra el conteo global por estado.
            self._registrar_conteo_estados(paso=paso)

        return self.pedidos

    def calcular_metricas(self):
        """
        Calcula métricas clave de la simulación.
        """
        total = len(self.pedidos)
        entregados = sum(1 for p in self.pedidos if p.estado_actual == "Entregado")
        cancelados = sum(1 for p in self.pedidos if p.estado_actual == "Devuelto")

        tiempos_por_estado = {estado: [] for estado in ESTADOS}

        for p in self.pedidos:
            conteo_pedido = {estado: 0 for estado in ESTADOS}
            for estado in p.historial:
                conteo_pedido[estado] += 1

            for estado, count in conteo_pedido.items():
                tiempos_por_estado[estado].append(count)

        promedios_estado = {
            estado: np.mean(tiempos) if tiempos else 0
            for estado, tiempos in tiempos_por_estado.items()
        }

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

    def generar_eventos_dataframe(self):
        """
        Retorna una tabla con todos los eventos individuales de la simulación.
        """
        return pd.DataFrame(self.eventos)

    def generar_estados_por_paso_dataframe(self):
        """
        Retorna una tabla con la cantidad de pedidos por estado en cada paso.
        """
        return pd.DataFrame(self.estados_por_paso)

    def exportar_csv(self, filename: str = "resultados_simulacion.csv"):
        """
        Exporta los resultados finales de cada pedido a un archivo CSV.
        """
        if self.resultados is None:
            self.generar_reporte_dataframe()
        self.resultados.to_csv(filename, index=False)
        print(f"Resultados exportados a {filename}")

    def exportar_eventos_csv(self, filename: str = "eventos_simulacion.csv"):
        """
        Exporta el registro de eventos individuales a CSV.
        """
        df_eventos = self.generar_eventos_dataframe()
        df_eventos.to_csv(filename, index=False)
        print(f"Eventos exportados a {filename}")

    def exportar_estados_por_paso_csv(self, filename: str = "estados_por_paso.csv"):
        """
        Exporta el conteo de pedidos por estado y paso a CSV.
        """
        df_estados = self.generar_estados_por_paso_dataframe()
        df_estados.to_csv(filename, index=False)
        print(f"Estados por paso exportados a {filename}")
