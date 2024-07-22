import unittest
from dml import DML
import pymysql

class TestDML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todos los casos de prueba
        cls.dml = DML(host="localhost", user="root", password="Iiebc04299?", db="medical", port=3305)
        cls.dml.conectar()
        cls.setup_database()

    @classmethod
    def setup_database(cls):
        # Crear tabla de prueba
        cls.dml.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        cls.dml.db.commit()

    def test_insertar(self):
        self.dml.insertar("INSERT INTO test_table (name) VALUES (%s)", ("test_name",))
        result = self.dml.consultar("SELECT name FROM test_table WHERE name = %s", ("test_name",))
        self.assertEqual(result[0], "test_name")

    def test_actualizar(self):
        self.dml.insertar("INSERT INTO test_table (name) VALUES (%s)", ("old_name",))
        self.dml.actualizar("UPDATE test_table SET name = %s WHERE name = %s", ("new_name", "old_name"))
        result = self.dml.consultar("SELECT name FROM test_table WHERE name = %s", ("new_name",))
        self.assertEqual(result[0], "new_name")

    def test_eliminar(self):
        self.dml.insertar("INSERT INTO test_table (name) VALUES (%s)", ("delete_me",))
        self.dml.eliminar("DELETE FROM test_table WHERE name = %s", ("delete_me",))
        result = self.dml.consultar("SELECT name FROM test_table WHERE name = %s", ("delete_me",))
        self.assertIsNone(result)

    def test_consultar(self):
        self.dml.insertar("INSERT INTO test_table (name) VALUES (%s)", ("consult_me",))
        result = self.dml.consultar("SELECT name FROM test_table WHERE name = %s", ("consult_me",))
        self.assertEqual(result[0], "consult_me")

    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todos los casos de prueba
        cls.dml.cursor.execute("DROP TABLE IF EXISTS test_table")
        cls.dml.cerrar_conex()

if __name__ == '__main__':
    unittest.main()
