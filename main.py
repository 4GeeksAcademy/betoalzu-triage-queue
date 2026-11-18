"""Command-line interface for the triage queue."""

from triage_queue import Patient, TriageQueue


def run() -> None:
    queue = TriageQueue()

    while True:
        print(
            "\n=== Cola de triaje ===\n"
            "1. Añadir paciente\n"
            "2. Llamar al siguiente paciente\n"
            "3. Ver cola actual\n"
            "4. Ver estadísticas\n"
            "5. Salir"
        )
        choice = input("Selecciona una opción: ").strip()

        if choice == "1":
            name = input("Nombre del paciente: ").strip()
            level_text = input("Nivel de triaje (1=crítico, 2=urgente, 3=estándar): ").strip()
            try:
                patient = Patient(name=name, triage_level=int(level_text))
            except ValueError as error:
                print(f"Entrada inválida: {error}")
                continue
            queue.enqueue(patient)
            print(f"Paciente añadido: {patient.name} (nivel {patient.triage_level}).")
        elif choice == "2":
            try:
                patient = queue.dequeue()
            except LookupError as error:
                print(error)
            else:
                print(f"Siguiente paciente: {patient.name} (nivel {patient.triage_level}).")
        elif choice == "3":
            patients = queue.list_queue()
            if not patients:
                print("No hay pacientes en espera.")
            else:
                print("Pacientes en orden de atención:")
                for position, patient in enumerate(patients, start=1):
                    print(
                        f"{position}. {patient.name} — nivel {patient.triage_level} "
                        f"(llegada: {patient.arrived_at.isoformat()})"
                    )
        elif choice == "4":
            print("Pacientes en espera por nivel:")
            for level, count in queue.stats().items():
                print(f"  Nivel {level}: {count}")
        elif choice == "5":
            print("Saliendo del gestor de triaje.")
            return
        else:
            print("Opción inválida. Selecciona un número del 1 al 5.")


def main() -> None:
    try:
        run()
    except EOFError:
        print("\nEntrada finalizada. Saliendo del gestor de triaje.")


if __name__ == "__main__":
    main()
