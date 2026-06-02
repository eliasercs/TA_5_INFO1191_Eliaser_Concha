import numpy as np
from simulation import Simulador

def ejecutar_simulacion(num_pedidos: int = 100, max_pasos: int = 50):
    """
    Ejecuta una simulacion completa para una cantidad de pedidos
    utilizando la clase Simulador (Integrante 2).
    """
    print("=" * 60)
    print(" SIMULACION DE DISTRIBUCION DE PEDIDOS (CADENA DE MARKOV) ")
    print("=" * 60)
    
    # 1. Inicializar simulador
    sim = Simulador(num_pedidos=num_pedidos)
    
    # 2. Ejecutar simulación
    print(f"\nIniciando simulación de {num_pedidos} pedidos...")
    sim.ejecutar(max_pasos=max_pasos)
    
    # 3. Calcular métricas
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
    for estado, promedio in metricas['tiempo_promedio_por_estado'].items():
        print(f"  - {estado:16}: {promedio:.2f} pasos")
        
    # 4. Exportar resultados
    sim.exportar_csv("resultados_simulacion.csv")
    
    # Mostrar algunos ejemplos de historiales de pedidos
    print("\nEjemplos de ciclos de vida de pedidos individuales:")
    for p in sim.pedidos[:5]:
        print(f"  * {p.id}: {' -> '.join(p.historial)}")
    print("=" * 60)

if __name__ == "__main__":
    # Ejecutamos la simulacion con 1000 pedidos por defecto
    ejecutar_simulacion(num_pedidos=1000)
