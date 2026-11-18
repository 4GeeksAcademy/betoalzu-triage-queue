# Notas de diseño

La cola usa un min-heap de `heapq`, con cada entrada ordenada por `(nivel de
triaje, secuencia de llegada)`. El nivel menor tiene mayor prioridad y un
contador monotónico garantiza FIFO dentro del mismo nivel, sin comparar los
objetos `Patient`. Encolar y desencolar cuestan O(log n), consultar el siguiente
O(1), listar O(n log n) y calcular estadísticas O(n).

Una sola `deque` no permite insertar por prioridad; una lista ordenada requiere
desplazar elementos al insertar, mientras que tres colas separadas podrían
resolverlo pero duplican el control de prioridad y el estado. El heap ofrece
una única estructura que mantiene el siguiente paciente disponible de manera
eficiente.

Todos los accesos y mutaciones del heap están protegidos por el mismo `Lock`.
Un worker que desencola adquiere el lock, extrae y elimina el mínimo como una
operación atómica y solo entonces lo libera; así ese paciente no puede ser
entregado dos veces. Una inserción crítica concurrente queda serializada antes
o después de esa extracción. Si sucede después, tendrá prioridad en la siguiente
extracción; no puede reemplazar retroactivamente al paciente ya retirado.
