"""Priority queue primitives for emergency-department triage."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from heapq import heappop, heappush
from itertools import count
from threading import Lock


@dataclass(frozen=True)
class Patient:
    """A patient waiting for triage."""

    name: str
    triage_level: int
    arrived_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El nombre del paciente no puede estar vacío.")
        if (
            isinstance(self.triage_level, bool)
            or not isinstance(self.triage_level, int)
            or self.triage_level not in (1, 2, 3)
        ):
            raise ValueError("El nivel de triaje debe ser 1, 2 o 3.")


class TriageQueue:
    """Thread-safe triage queue ordered by urgency, then enqueue order."""

    def __init__(self):
        self._patients = []
        self._sequence = count()
        self._lock = Lock()

    def enqueue(self, patient: Patient) -> None:
        """Add a patient while preserving FIFO order within each triage level."""
        if not isinstance(patient, Patient):
            raise TypeError("enqueue espera una instancia de Patient.")
        with self._lock:
            heappush(
                self._patients,
                (patient.triage_level, next(self._sequence), patient),
            )

    def dequeue(self) -> Patient:
        """Remove and return the next patient, or raise LookupError if empty."""
        with self._lock:
            if not self._patients:
                raise LookupError("No hay pacientes en espera.")
            return heappop(self._patients)[2]

    def peek(self) -> Patient:
        """Return the next patient without removing it."""
        with self._lock:
            if not self._patients:
                raise LookupError("No hay pacientes en espera.")
            return self._patients[0][2]

    def list_queue(self) -> list[Patient]:
        """Return a snapshot of patients in service order."""
        with self._lock:
            return [entry[2] for entry in sorted(self._patients)]

    def stats(self) -> dict[int, int]:
        """Return the number of waiting patients for each triage level."""
        with self._lock:
            counts = {1: 0, 2: 0, 3: 0}
            for level, _, _ in self._patients:
                counts[level] += 1
            return counts
