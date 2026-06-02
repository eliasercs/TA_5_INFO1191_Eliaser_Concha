## Caso de estudio: Sistema de distribución de pedidos e-commerce

### Descripción del caso

Se modela el ciclo de vida de un pedido en una tienda online similar a Mercado Libre 
o Falabella. Desde que el cliente realiza la compra hasta que el pedido es entregado, 
devuelto o marcado como fallido. Cada pedido transita por distintos estados operacionales, 
y las probabilidades de transición entre ellos reflejan condiciones reales del proceso 
logístico (disponibilidad de stock, capacidad de despacho, tasa de entregas fallidas, etc.).

---

## Estados del sistema

| ID  | Estado          | Descripción                                                                 |
|-----|-----------------|-----------------------------------------------------------------------------|
| S0  | Pedido Recibido | El cliente realizó la compra exitosamente                                   |
| S1  | En Preparación  | El producto está siendo preparado en bodega                                 |
| S2  | En Bodega       | El pedido está listo, esperando asignación a repartidor                     |
| S3  | En Reparto      | El repartidor está en camino al domicilio del cliente                       |
| S4  | Entregado       | El pedido fue entregado exitosamente (estado absorbente)                    |
| S5  | Entrega Fallida | No se pudo entregar (nadie en casa, dirección incorrecta, etc.)             |
| S6  | Devuelto        | El pedido retornó al origen sin ser entregado (estado absorbente)           |

---

## Matriz de transición de primer orden

La matriz de transición **P** representa las probabilidades de pasar de un estado a otro 
en un solo paso. Cada fila corresponde al estado actual y cada columna al estado siguiente. 
La suma de cada fila es igual a 1, cumpliendo la condición de matriz estocástica.

|     | S0  | S1  | S2  | S3  | S4  | S5  | S6  |
|-----|-----|-----|-----|-----|-----|-----|-----|
| S0  | 0.0 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.1 |
| S1  | 0.0 | 0.1 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| S2  | 0.0 | 0.0 | 0.1 | 0.9 | 0.0 | 0.0 | 0.0 |
| S3  | 0.0 | 0.0 | 0.0 | 0.0 | 0.8 | 0.2 | 0.0 |
| S4  | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| S5  | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 0.5 |
| S6  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |

### Justificación de probabilidades

- **S0 → S1 (0.9):** El 90% de los pedidos recibidos pasan a preparación. El 10% restante 
  se devuelve de inmediato por errores de pago o falta de stock.
- **S1 → S2 (0.9):** El 90% de los pedidos en preparación avanzan a bodega. El 10% permanece 
  en preparación un paso más por demoras operativas.
- **S2 → S3 (0.9):** El 90% de los pedidos en bodega son asignados a reparto. El 10% permanece 
  en bodega por falta de repartidor disponible.
- **S3 → S4 (0.8):** El 80% de los pedidos en reparto se entregan exitosamente.
- **S3 → S5 (0.2):** El 20% de los pedidos en reparto no pueden ser entregados.
- **S5 → S3 (0.5):** La mitad de las entregas fallidas se reintenta al día siguiente.
- **S5 → S6 (0.5):** La otra mitad se devuelve definitivamente al origen.
- **S4 y S6:** Son estados absorbentes; una vez alcanzados, el pedido no cambia de estado.

---

## Explicación del Código

El proyecto está diseñado bajo un enfoque modular y orientado a objetos, simulando un proceso estocástico discreto (Cadena de Markov de primer orden). Consta de tres archivos principales:

1. **[markov_base.py](./markov_base.py)**: Define la estructura y el comportamiento base del modelo de Markov.
   - **Estructura de Estados**: El diccionario `ESTADOS` mapea los nombres a índices numéricos (0 a 6). Los estados terminales se definen en el conjunto `ESTADOS_ABSORBENTES`.
   - **[construir_matriz](./markov_base.py#L18)**: Inicializa y retorna la matriz de transición estocástica $P$ de $7 \times 7$ con NumPy.
   - **[validar_matriz](./markov_base.py#L38)**: Valida la consistencia de la matriz $P$ (dimensiones correctas, todos los elementos no negativos, y suma de cada fila igual a $1.0$ con margen de tolerancia de error flotante).
   - **Clase [Pedido](./markov_base.py#L72)**: Modela a un pedido individual. Posee identificador (`id`), el estado actual (`estado_actual`) y la lista de todos los estados transitados (`historial`).
   - **[siguiente_estado](./markov_base.py#L96)**: Determina de forma probabilística el próximo estado del pedido a partir de su estado actual usando la función `numpy.random.choice` ponderada por las probabilidades de transición asociadas.
   - **[generar_pedidos](./markov_base.py#L116)**: Helper para inicializar una colección de $N$ pedidos en el estado inicial "Pedido Recibido".

2. **[main.py](./main.py)**: Orquestador principal de la simulación.
   - Inicializa una lista de pedidos y la matriz de Markov.
   - Modela la evolución temporal de los pedidos paso a paso en un bucle.
   - Detiene el bucle cuando todos los pedidos finalizan en un estado absorbente ("Entregado" o "Devuelto") o se alcanza el límite de pasos definido.
   - Calcula estadísticos descriptivos finales (proporción de éxitos vs devoluciones, promedio de pasos transcurridos por desenlace, e historiales de ciclo de vida).

3. **[test_markov_base.py](./tests/test_markov_base.py)**: Suite de pruebas unitarias escritas con `unittest`.
   - Contiene 12 pruebas para validar las dimensiones de la matriz, la suma unitaria de filas, no negatividad, consistencia de los estados absorbentes, inicialización y actualización de pedidos, generación exclusiva de IDs, entre otros aspectos clave.

---

## Requisitos del Sistema

Para poder ejecutar el código, debes tener instalado:

- **Python 3.7 o superior** (Desarrollado y probado bajo Python 3.12)
- **NumPy**: Biblioteca esencial para la gestión de matrices numéricas y selección probabilística.

---

## Instrucciones de Instalación y Uso

### 1. Acceder al directorio
Asegúrate de estar ubicado en la carpeta del subproyecto:
```bash
cd proyecto
```

### 2. Instalar dependencias
Instala la biblioteca NumPy desde tu terminal ejecutando:
```bash
pip install numpy
```

### 3. Ejecutar la simulación principal
Para iniciar la simulación por defecto y ver las estadísticas de logística:
```bash
python main.py
```

### 4. Ejecutar las pruebas unitarias
Para validar que todo el código base funciona según los requisitos lógicos y probabilísticos esperados:
```bash
python -m unittest tests/test_markov_base.py
```
