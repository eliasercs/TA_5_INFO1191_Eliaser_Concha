import numpy as np

# Sección 1 — Constantes y definición de estados
ESTADOS = {
    "Pedido Recibido": 0,
    "En Preparación":  1,
    "En Bodega":       2,
    "En Reparto":      3,
    "Entregado":       4,
    "Entrega Fallida": 5,
    "Devuelto":        6
}

ESTADOS_ABSORBENTES = {"Entregado", "Devuelto"}

# Invertir el diccionario para buscar nombres de estado por índice
INDICES_A_ESTADOS = {v: k for k, v in ESTADOS.items()}


# Sección 2 — Construcción y validación de la matriz de transición
def construir_matriz() -> np.ndarray:
    """
    Retorna la matriz de transición 7x7 como numpy array con las probabilidades
    definidas en el caso de estudio.
    """
    P = np.array([
        [0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.1],  # S0: Pedido Recibido
        [0.0, 0.1, 0.9, 0.0, 0.0, 0.0, 0.0],  # S1: En Preparación
        [0.0, 0.0, 0.1, 0.9, 0.0, 0.0, 0.0],  # S2: En Bodega
        [0.0, 0.0, 0.0, 0.0, 0.8, 0.2, 0.0],  # S3: En Reparto
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # S4: Entregado (absorbente)
        [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.5],  # S5: Entrega Fallida
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]   # S6: Devuelto (absorbente)
    ])
    return P


def validar_matriz(P: np.ndarray) -> bool:
    """
    Verifica que:
    - La matriz sea de dimensión 7x7
    - Todos los valores sean mayores o iguales a 0
    - Cada fila sume exactamente 1.0 (tolerancia de 1e-6)
    Imprime un mensaje de éxito o de error por cada fila que no cumpla.
    """
    if P.shape != (7, 7):
        print(f"Error: La matriz no es de dimensión 7x7. Dimensión actual: {P.shape}")
        return False

    if np.any(P < 0):
        print("Error: La matriz contiene valores negativos.")
        return False

    valida = True
    for i in range(7):
        suma_fila = np.sum(P[i])
        nombre_estado = INDICES_A_ESTADOS[i]
        if not np.isclose(suma_fila, 1.0, atol=1e-6):
            print(f"Error en fila {i} ({nombre_estado}): La suma es {suma_fila}, se esperaba 1.0")
            valida = False
        else:
            # Aunque sea exitoso, imprimimos información útil para validación si es necesario, 
            # pero la lógica central es reportar errores.
            pass

    if valida:
        print("Matriz de transicion validada correctamente (7x7, valores no negativos, filas suman 1.0).")
    return valida


# Sección 3 — Clase Pedido
class Pedido:
    """
    Representa un pedido individual en el sistema de distribución.
    """
    def __init__(self, id_pedido: str):
        """
        Inicializa un pedido en el estado "Pedido Recibido" y con historial vacío.
        """
        self.id = id_pedido
        self.estado_actual = "Pedido Recibido"
        self.historial = []

    def actualizar_estado(self, nuevo_estado: str):
        """
        Cambia el estado actual del pedido y lo agrega al historial.
        """
        self.estado_actual = nuevo_estado
        self.historial.append(nuevo_estado)

    def esta_finalizado(self) -> bool:
        """
        Retorna True si el estado actual es uno de los estados absorbentes (finales).
        """
        return self.estado_actual in ESTADOS_ABSORBENTES

    def __repr__(self) -> str:
        return f"Pedido(id='{self.id}', estado_actual='{self.estado_actual}', historial={self.historial})"


# Sección 4 — Selección probabilística del siguiente estado
def siguiente_estado(estado_actual: str, P: np.ndarray) -> str:
    """
    Función central de la cadena de Markov. Retorna el nombre del siguiente estado.
    1. Obtiene el índice del estado actual.
    2. Extrae la fila correspondiente de la matriz P.
    3. Usa numpy.random.choice sobre los nombres de estados con esos pesos.
    4. Retorna el nombre del estado siguiente como string.
    """
    if estado_actual not in ESTADOS:
        raise ValueError(f"Estado '{estado_actual}' no es un estado válido.")
    
    idx_actual = ESTADOS[estado_actual]
    probabilidades = P[idx_actual]
    
    nombres_estados = [INDICES_A_ESTADOS[i] for i in range(7)]
    
    estado_sig = np.random.choice(nombres_estados, p=probabilidades)
    return estado_sig


# Sección 5 — Generación de pedidos iniciales
def generar_pedidos(n: int) -> list[Pedido]:
    """
    Crea una lista de n objetos Pedido, todos inicializados en "Pedido Recibido",
    con IDs únicos autogenerados en formato "PED-001", "PED-002", etc.
    """
    pedidos = []
    for i in range(1, n + 1):
        id_str = f"PED-{i:03d}"
        pedidos.append(Pedido(id_str))
    return pedidos
