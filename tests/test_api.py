import unittest
from unittest.mock import MagicMock
from api import add_appointment_logic, instancia


class TestAddAppointmentLogic(unittest.TestCase):

    def setUp(self):
        self.instancia_mock = MagicMock()
        global instancia
        instancia = self.instancia_mock

    def test_successful_appointment_addition(self):
        self.instancia_mock.consultar.side_effect = lambda query, params: [1] if 'patient' in query else None
        self.instancia_mock.insertar.return_value = None

        msg, _ = add_appointment_logic('Carlos Ramirez', '2024-06-22', '7:00:00', 'Consulta general')
        self.assertEqual(msg, 'Cita agregada con éxito')

    def test_appointment_already_exists(self):
        self.instancia_mock.consultar.side_effect = lambda query, params: [1] if 'patient' in query else (
            [1] if 'appointment' in query else None)

        msg, _ = add_appointment_logic('Carlos Ramirez', '2024-07-22', '9:00:00', 'Consulta general')
        self.assertEqual(msg, 'Ya hay una cita registrada en ese horario')

    def test_patient_not_found(self):
        self.instancia_mock.consultar.return_value = None

        msg, _ = add_appointment_logic('John Doe', '2024-07-22', '10:00', 'Consulta general')
        self.assertEqual(msg, 'Paciente no encontrado')



if __name__ == '__main__':
    unittest.main()
