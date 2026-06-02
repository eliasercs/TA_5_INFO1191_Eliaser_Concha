import numpy as np
from markov_base import (
    construir_matriz,
    validar_matriz,
    generar_pedidos,
    siguiente_estado
)

def ejecutar_simulacion(num_pedidos: int = 100, max_pasos: int = 50):
    """
    Ejecuta una simulacion completa para una cantidad de pedidos,
    siguiendo su ciclo de vida paso a paso usando la cadena de Markov.
    """
    print("=" * 60)
    print(" SIMULACION DE DISTRIBUCION DE PEDIDOS (CADENA DE MARKOV) ")
    print("=" * 60)
    
    # 1. Obtener y validar la matriz de transicion
    P = construir_matriz()
    if not validar_matriz(P):
        print("La matriz de transicion no es valida. Abortando simulacion.")
        return
    
    # 2. Generar los pedidos iniciales (todos en "Pedido Recibido")
    pedidos = generar_pedidos(num_pedidos)
    print(f"\nSe han generado {num_pedidos} pedidos inicializados en 'Pedido Recibido'.")
    
    # Agregar el estado inicial al historial de cada pedido
    for p in pedidos:
        p.historial.append(p.estado_actual)
        
    paso = 0
    finalizados = 0
    
    # 3. Ciclo de simulacion paso a paso
    while finalizados < num_pedidos and paso < max_pasos:
        paso += 1
        for p in pedidos:
            if not p.esta_finalizado():
                nuevo_est = siguiente_estado(p.estado_actual, P)
                p.actualizar_estado(nuevo_est)
        
        finalizados = sum(1 for p in pedidos if p.esta_finalizado())
        
    # 4. Procesar y mostrar estadisticas de los resultados
    entregados = sum(1 for p in pedidos if p.estado_actual == "Entregado")
    devueltos = sum(1 for p in pedidos if p.estado_actual == "Devuelto")
    
    pasos_totales_entregados = []
    pasos_totales_devueltos = []
    
    for p in pedidos:
        # El numero de transiciones es la longitud del historial menos 1 (el estado inicial)
        num_pasos_pedido = len(p.historial) - 1
        if p.estado_actual == "Entregado":
            pasos_totales_entregados.append(num_pasos_pedido)
        elif p.estado_actual == "Devuelto":
            pasos_totales_devueltos.append(num_pasos_pedido)

    print("\n" + "=" * 60)
    print(" RESULTADOS Y ESTADISTICAS ")
    print("=" * 60)
    print(f"Total de pedidos simulados: {num_pedidos}")
    print(f"Pasos maximos de simulacion: {paso}")
    print("-" * 60)
    print(f"  [+] Entregados exitosamente: {entregados} ({entregados/num_pedidos*100:.1f}%)")
    print(f"  [-] Devueltos al origen:      {devueltos} ({devueltos/num_pedidos*100:.1f}%)")
    print("-" * 60)
    
    if pasos_totales_entregados:
        avg_entregados = np.mean(pasos_totales_entregados)
        print(f"Promedio de pasos para entrega exitosa: {avg_entregados:.2f} pasos")
    if pasos_totales_devueltos:
        avg_devueltos = np.mean(pasos_totales_devueltos)
        print(f"Promedio de pasos para devolucion:      {avg_devueltos:.2f} pasos")
        
    # Mostrar algunos ejemplos de historiales de pedidos
    print("\nEjemplos de ciclos de vida de pedidos individuales:")
    for p in pedidos[:5]:
        print(f"  * {p.id}: {' -> '.join(p.historial)}")
    print("=" * 60)

if __name__ == "__main__":
    # Ejecutamos la simulacion con 1000 pedidos por defecto
    ejecutar_simulacion(num_pedidos=1000)
