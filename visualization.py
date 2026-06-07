import matplotlib.pyplot as plt

def graficar_evolucion_estados(df_estados, filename: str = "visualizacion_eventos.png"):
    """
    Genera un gráfico de líneas con la evolución de pedidos por estado.
    Eje X: paso de simulación.
    Eje Y: cantidad de pedidos en cada estado.
    """
    if df_estados.empty:
        raise ValueError("No existen datos para graficar. Ejecuta la simulación primero.")

    plt.figure(figsize=(12, 7))

    for columna in df_estados.columns:
        if columna != "paso":
            plt.plot(df_estados["paso"], df_estados[columna], marker="o", label=columna)

    plt.title("Visualización de eventos: evolución de pedidos por estado")
    plt.xlabel("Paso de simulación")
    plt.ylabel("Cantidad de pedidos")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Gráfico guardado como {filename}")


def graficar_resultado_final(metricas: dict, filename: str = "grafico_resultado_final.png"):
    """
    Grafica la métrica de resultado final:
    pedidos entregados exitosamente vs pedidos devueltos/cancelados.
    """
    etiquetas = ["Entregados", "Devueltos"]
    valores = [metricas["entregas_exitosas"], metricas["cancelaciones"]]

    plt.figure(figsize=(7, 5))
    barras = plt.bar(etiquetas, valores)

    plt.title("Resultado final de la simulación")
    plt.xlabel("Estado final")
    plt.ylabel("Cantidad de pedidos")
    plt.grid(axis="y", alpha=0.3)

    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            str(int(altura)),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Gráfico guardado como {filename}")


def graficar_tiempo_promedio_estado(metricas: dict, filename: str = "grafico_tiempo_promedio_estado.png"):
    """
    Grafica el tiempo promedio que los pedidos permanecen en cada estado.
    Usa la métrica tiempo_promedio_por_estado calculada por el simulador.
    """
    tiempos = metricas["tiempo_promedio_por_estado"]
    estados = list(tiempos.keys())
    valores = list(tiempos.values())

    plt.figure(figsize=(11, 6))
    barras = plt.bar(estados, valores)

    plt.title("Tiempo promedio por estado")
    plt.xlabel("Estado")
    plt.ylabel("Promedio de pasos")
    plt.xticks(rotation=35, ha="right")
    plt.grid(axis="y", alpha=0.3)

    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            f"{altura:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Gráfico guardado como {filename}")


def graficar_distribucion_pasos(df_resultados, filename: str = "grafico_distribucion_pasos.png"):
    """
    Grafica la distribución de pasos totales necesarios para que los pedidos terminen.
    Usa la columna pasos_totales generada en generar_reporte_dataframe().
    """
    if df_resultados.empty or "pasos_totales" not in df_resultados.columns:
        raise ValueError("El DataFrame de resultados no contiene la columna 'pasos_totales'.")

    plt.figure(figsize=(9, 5))
    plt.hist(df_resultados["pasos_totales"], bins=range(0, int(df_resultados["pasos_totales"].max()) + 2), edgecolor="black")

    plt.title("Distribución de pasos totales por pedido")
    plt.xlabel("Pasos totales")
    plt.ylabel("Cantidad de pedidos")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Gráfico guardado como {filename}")
