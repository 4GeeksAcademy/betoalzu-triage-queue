import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from main import run
from triage_queue import Patient, TriageQueue


class TriageQueueTests(unittest.TestCase):
    def setUp(self):
        self.queue = TriageQueue()

    def test_priority_level_one_jumps_ahead_of_waiting_patients(self):
        standard = Patient("Estándar", 3)
        urgent = Patient("Urgente", 2)
        critical = Patient("Crítico", 1)
        self.queue.enqueue(standard)
        self.queue.enqueue(urgent)
        self.queue.enqueue(critical)

        self.assertEqual(self.queue.list_queue(), [critical, urgent, standard])

    def test_patients_at_same_level_are_served_in_enqueue_order(self):
        first = Patient("Primero", 2)
        second = Patient("Segundo", 2)
        self.queue.enqueue(first)
        self.queue.enqueue(second)

        self.assertIs(self.queue.dequeue(), first)
        self.assertIs(self.queue.dequeue(), second)

    def test_peek_does_not_remove_patient_and_stats_count_each_level(self):
        critical = Patient("Crítico", 1)
        standard = Patient("Estándar", 3)
        self.queue.enqueue(standard)
        self.queue.enqueue(critical)

        self.assertIs(self.queue.peek(), critical)
        self.assertEqual(self.queue.stats(), {1: 1, 2: 0, 3: 1})
        self.assertEqual(self.queue.list_queue(), [critical, standard])

    def test_empty_queue_operations_raise_descriptive_errors(self):
        for operation in (self.queue.dequeue, self.queue.peek):
            with self.subTest(operation=operation.__name__):
                with self.assertRaisesRegex(LookupError, "No hay pacientes"):
                    operation()

    def test_patient_rejects_invalid_triage_level(self):
        for level in (0, 4, True, 1.0):
            with self.subTest(level=level):
                with self.assertRaises(ValueError):
                    Patient("Paciente", level)

    def test_cli_reports_invalid_triage_input_and_continues(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["1", "Paciente", "inválido", "5"]):
            with redirect_stdout(output):
                run()

        self.assertIn("Entrada inválida", output.getvalue())
        self.assertIn("Saliendo del gestor", output.getvalue())


if __name__ == "__main__":
    unittest.main()
