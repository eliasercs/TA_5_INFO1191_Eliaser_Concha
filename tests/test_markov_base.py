import sys
import os
import unittest
import numpy as np

# Añadir el directorio padre al path para poder importar markov_base
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from markov_base import (
    ESTADOS,
    ESTADOS_ABSORBENTES,
    construir_matriz,
    validar_matriz,
    Pedido,
    siguiente_estado,
    generar_pedidos
)

class TestMarkovBase(unittest.TestCase):
    
    def setUp(self):
        self.P = construir_matriz()

    def test_dimensiones_matriz(self):
        """La matriz retornada es de forma (7, 7)"""
        self.assertEqual(self.P.shape, (7, 7))

    def test_filas_suman_1(self):
        """Cada fila de la matriz suma 1.0 con tolerancia ±1e-6"""
        for i in range(7):
            suma_fila = np.sum(self.P[i])
            self.assertTrue(np.isclose(suma_fila, 1.0, atol=1e-6))

    def test_valores_no_negativos(self):
        """Ningún valor de la matriz es negativo"""
        self.assertTrue(np.all(self.P >= 0.0))

    def test_siguiente_estado_valido(self):
        """El estado retornado por siguiente_estado existe en ESTADOS"""
        for estado in ESTADOS:
            sig = siguiente_estado(estado, self.P)
            self.assertIn(sig, ESTADOS)

    def test_estado_absorbente_entregado(self):
        """Desde 'Entregado', siguiente_estado siempre retorna 'Entregado'"""
        for _ in range(100):
            sig = siguiente_estado("Entregado", self.P)
            self.assertEqual(sig, "Entregado")

    def test_estado_absorbente_devuelto(self):
        """Desde 'Devuelto', siguiente_estado siempre retorna 'Devuelto'"""
        for _ in range(100):
            sig = siguiente_estado("Devuelto", self.P)
            self.assertEqual(sig, "Devuelto")

    def test_pedido_estado_inicial(self):
        """Un Pedido nuevo comienza en 'Pedido Recibido'"""
        pedido = Pedido("PED-999")
        self.assertEqual(pedido.estado_actual, "Pedido Recibido")

    def test_pedido_historial_vacio(self):
        """Un Pedido nuevo tiene historial vacío"""
        pedido = Pedido("PED-999")
        self.assertEqual(pedido.historial, [])

    def test_pedido_actualizar_estado(self):
        """actualizar_estado cambia el estado y lo agrega al historial"""
        pedido = Pedido("PED-999")
        pedido.actualizar_estado("En Preparación")
        self.assertEqual(pedido.estado_actual, "En Preparación")
        self.assertEqual(pedido.historial, ["En Preparación"])
        
        pedido.actualizar_estado("En Bodega")
        self.assertEqual(pedido.estado_actual, "En Bodega")
        self.assertEqual(pedido.historial, ["En Preparación", "En Bodega"])

    def test_pedido_esta_finalizado(self):
        """esta_finalizado() retorna True si estado es absorbente"""
        pedido = Pedido("PED-999")
        self.assertFalse(pedido.esta_finalizado())
        
        pedido.actualizar_estado("En Preparación")
        self.assertFalse(pedido.esta_finalizado())
        
        pedido.actualizar_estado("Entregado")
        self.assertTrue(pedido.esta_finalizado())
        
        pedido2 = Pedido("PED-888")
        pedido2.actualizar_estado("Devuelto")
        self.assertTrue(pedido2.esta_finalizado())

    def test_generacion_n_pedidos(self):
        """generar_pedidos(n) retorna exactamente n objetos"""
        n = 15
        pedidos = generar_pedidos(n)
        self.assertEqual(len(pedidos), n)
        for p in pedidos:
            self.assertTrue(isinstance(p, Pedido))

    def test_ids_unicos(self):
        """Todos los IDs generados son distintos entre sí"""
        n = 50
        pedidos = generar_pedidos(n)
        ids = [p.id for p in pedidos]
        self.assertEqual(len(ids), len(set(ids)))
        # Además validamos el formato de ejemplo
        self.assertEqual(pedidos[0].id, "PED-001")
        self.assertEqual(pedidos[49].id, "PED-050")

if __name__ == '__main__':
    unittest.main()
