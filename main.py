from pathlib import Path
from simulation import Simulador
from visualization import (
    graficar_evolucion_estados,
    graficar_resultado_final,
    graficar_tiempo_promedio_estado,
    graficar_distribucion_pasos,
)


def ejecutar_simulacion(num_pedidos: int = 100, max_pasos: int = 50):
    """
    Ejecuta una simulación completa para una cantidad de pedidos.
    Incluye resultados, métricas, eventos y gráficos automáticos.
    """
    print("=" * 60)
    print(" SIMULACION DE DISTRIBUCION DE PEDIDOS (CADENA DE MARKOV) ")
    print("=" * 60)

    # 1. Inicializar simulador
    sim = Simulador(num_pedidos=num_pedidos)

    # 2. Ejecutar simulación
    print(f"\nIniciando simulación de {num_pedidos} pedidos...")
    sim.ejecutar(max_pasos=max_pasos)

    # 3. Calcular métricas originales
    metricas = sim.calcular_metricas()

    print("\n" + "=" * 60)
    print(" RESULTADOS Y ESTADISTICAS ")
    print("=" * 60)
    print(f"Total de pedidos simulados: {metricas['total_pedidos']}")
    print("-" * 60)
    print(f"  [+] Entregados exitosamente: {metricas['entregas_exitosas']} ({metricas['porcentaje_exito']:.1f}%)")
    print(f"  [-] Cancelaciones/Devueltos: {metricas['cancelaciones']}")
    print("-" * 60)

    print("Promedio de tiempo (pasos) por estado:")
    for estado, promedio in metricas["tiempo_promedio_por_estado"].items():
        print(f"  - {estado:16}: {promedio:.2f} pasos")

    # Carpeta donde se guardarán los CSV y gráficos.
    # Se usa la carpeta del archivo main.py para evitar que los archivos
    # se guarden en otra ubicación si el programa se ejecuta desde otro directorio.
    output_dir = Path(__file__).resolve().parent

    # 4. Exportar resultados generales
    sim.exportar_csv(str(output_dir / "resultados_simulacion.csv"))

    # 5. Exportar evidencia de eventos
    sim.exportar_eventos_csv(str(output_dir / "eventos_simulacion.csv"))

    # 6. Exportar tabla para visualización por paso
    sim.exportar_estados_por_paso_csv(str(output_dir / "estados_por_paso.csv"))

    # 7. Preparar dataframes para gráficos
    df_resultados = sim.generar_reporte_dataframe()
    df_estados = sim.generar_estados_por_paso_dataframe()

    # 8. Mostrar ejemplos de ciclos de vida de pedidos individuales
    print("\nEjemplos de ciclos de vida de pedidos individuales:")
    for p in sim.pedidos[:5]:
        print(f"  * {p.id}: {' -> '.join(p.historial)}")

    # 9. Mostrar una tabla resumida de la evolución de eventos
    print("\nConteo de pedidos por estado en los primeros pasos:")
    print(df_estados.head(10).to_string(index=False))

    # 10. Generar gráficos automáticamente
    graficar_evolucion_estados(df_estados, str(output_dir / "visualizacion_eventos.png"))
    graficar_resultado_final(metricas, str(output_dir / "grafico_resultado_final.png"))
    graficar_tiempo_promedio_estado(metricas, str(output_dir / "grafico_tiempo_promedio_estado.png"))
    graficar_distribucion_pasos(df_resultados, str(output_dir / "grafico_distribucion_pasos.png"))

    print("=" * 60)


if __name__ == "__main__":
    ejecutar_simulacion(num_pedidos=1000, max_pasos=50)
