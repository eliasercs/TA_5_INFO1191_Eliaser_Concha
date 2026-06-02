import sys
import os
import unittest
import pandas as pd

# Añadir el directorio padre al path para poder importar simulation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation import Simulador

class TestSimulation(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.sim = Simulador(num_pedidos=10)

    def test_inicializacion(self):
        """El simulador se inicializa con la cantidad correcta de pedidos."""
        self.assertEqual(len(self.sim.pedidos), 10)
        self.assertIsNotNone(self.sim.matriz)

    def test_ejecutar_avanza_pedidos(self):
        """La simulación debe registrar estados en el historial de los pedidos."""
        self.sim.ejecutar(max_pasos=5)
        for p in self.sim.pedidos:
            # Todos deben tener al menos el estado inicial
            self.assertGreaterEqual(len(p.historial), 1)

    def test_calcular_metricas(self):
        """Verifica que el cálculo de métricas devuelva los campos requeridos."""
        self.sim.ejecutar(max_pasos=20)
        metricas = self.sim.calcular_metricas()
        
        campos_esperados = [
            "total_pedidos", 
            "entregas_exitosas", 
            "cancelaciones", 
            "porcentaje_exito", 
            "tiempo_promedio_por_estado"
        ]
        for campo in campos_esperados:
            self.assertIn(campo, metricas)
            
        self.assertEqual(metricas["total_pedidos"], 10)
        self.assertEqual(len(metricas["tiempo_promedio_por_estado"]), 7)

    def test_generar_reporte_dataframe(self):
        """Verifica que se genere un DataFrame de pandas con la estructura correcta."""
        self.sim.ejecutar(max_pasos=5)
        df = self.sim.generar_reporte_dataframe()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)
        self.assertIn("id", df.columns)
        self.assertIn("estado_final", df.columns)
        self.assertIn("pasos_totales", df.columns)
        self.assertIn("historial", df.columns)

    def test_exportar_csv(self):
        """Verifica la creación del archivo CSV de resultados."""
        filename = "test_export.csv"
        if os.path.exists(filename):
            os.remove(filename)
            
        self.sim.ejecutar(max_pasos=5)
        self.sim.exportar_csv(filename)
        
        self.assertTrue(os.path.exists(filename))
        
        # Limpieza
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
