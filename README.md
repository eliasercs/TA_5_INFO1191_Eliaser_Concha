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

1. **[markov_base.py](./markov_base.py)**: Define la estructura y el comportamiento base del modelo de Markov (Trabajo Integrante 1).
   - **Estructura de Estados**: El diccionario `ESTADOS` mapea los nombres a índices numéricos (0 a 6). Los estados terminales se definen en el conjunto `ESTADOS_ABSORBENTES`.
   - **[construir_matriz](./markov_base.py#L22)**: Inicializa y retorna la matriz de transición estocástica $P$ de $7 \times 7$ con NumPy.
   - **[validar_matriz](./markov_base.py#L42)**: Valida la consistencia de la matriz $P$ (dimensiones correctas, todos los elementos no negativos, y suma de cada fila igual a $1.0$).
   - **Clase [Pedido](./markov_base.py#L78)**: Modela un pedido con su ID, estado actual e historial.
   - **[siguiente_estado](./markov_base.py#L102)**: Realiza la transición probabilística de estados.
   - **[generar_pedidos](./markov_base.py#L122)**: Genera la lista inicial de pedidos.

2. **[simulation.py](./simulation.py)**: Engine de simulación y cálculo de métricas (Trabajo Integrante 2).
   - **Clase Simulador**: Gestiona la ejecución de múltiples pedidos simultáneos.
   - **Cálculo de Métricas**: Calcula entregas exitosas, cancelaciones (devueltos) y el tiempo promedio de permanencia en cada estado.
   - **Exportación**: Genera reportes detallados en formato DataFrame y exporta resultados a archivos CSV.

3. **[main.py](./main.py)**: Orquestador principal que integra el trabajo de ambos integrantes para ejecutar la simulación completa y mostrar resultados.

4. **[Pruebas Unitarias](./tests/)**: 
   - **[test_markov_base.py](./tests/test_markov_base.py)**: Valida la lógica base de Markov.
   - **[test_simulation.py](./tests/test_simulation.py)**: Valida el correcto funcionamiento del simulador y el cálculo de métricas.

---

## Requisitos del Sistema

Para poder ejecutar el código, debes tener instalado:

- **Python 3.7 o superior**
- **NumPy**: Para operaciones matriciales.
- **Pandas**: Para la gestión de datos y exportación a CSV.

---

## Instrucciones de Instalación y Uso

### 1. Instalar dependencias
Instala las bibliotecas necesarias:
```bash
pip install numpy pandas
```

### 2. Ejecutar simulación
Para correr la simulación principal:
```bash
python main.py
```

### 3. Ejecutar pruebas
Para validar el sistema:
```bash
python -m unittest discover tests
```

