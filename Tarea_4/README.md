# Tarea 4: Concurrencia en Python (Hilos, Procesos y Asyncio)

## Objetivo

El objetivo de esta tarea es explorar y comparar diferentes formas de concurrencia en Python: hilos (threads), procesos (processes) y programación asíncrona (asyncio). Se implementan ejemplos prácticos para observar diferencias en ejecución y tiempos de respuesta.

Esta tarea se basa en los siguientes recursos:
- [Repositorio de ejemplo de hilos y procesos](https://github.com/michel-lopez-franco/Hilos_Procesos_Python)
- [Scaling in Python](https://www.educative.io/blog/scaling-in-python)
- [Concurrency in Python: Threading, Processes and Asyncio](https://statusneo.com/concurrency-in-python-threading-processes-and-asyncio/)

---

## Estructura de archivos

- `main.py`: Script principal que ejecuta los tres enfoques de concurrencia.
- `threads_example.py`: Ejemplo usando hilos (`threading`).
- `process_example.py`: Ejemplo usando procesos (`multiprocessing`).
- `async_example.py`: Ejemplo usando programación asíncrona (`asyncio`).
- `utils.py`: Funciones auxiliares para simular tareas pesadas.

---

## Descripción de los archivos

### main.py

Este archivo ejecuta secuencialmente los tres enfoques de concurrencia. Llama a las funciones principales de cada ejemplo y muestra los resultados en consola.

### threads_example.py

Implementa la concurrencia usando hilos. Crea 5 hilos que ejecutan una tarea pesada de forma concurrente. Utiliza la librería estándar `threading`.

### process_example.py

Implementa la concurrencia usando procesos. Crea 5 procesos independientes que ejecutan la misma tarea pesada. Utiliza la librería estándar `multiprocessing`.

### async_example.py

Implementa la concurrencia usando programación asíncrona con `asyncio`. Crea 5 tareas asíncronas que simulan una tarea pesada. Utiliza `asyncio` para la gestión cooperativa de tareas.

### utils.py

Contiene funciones auxiliares, como la simulación de una tarea pesada (`heavy_task`) y la impresión de tiempos de inicio y fin de cada tarea.

---

## Requisitos y entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

### Crear entorno virtual

1. Abre una terminal en la carpeta `Tarea_4`.
2. Ejecuta:

   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:

   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En Mac/Linux:
     ```
     source venv/bin/activate
     ```

4. Instala dependencias (en este caso, solo se usan librerías estándar, no es necesario instalar paquetes externos).

---

## Ejecución

Con el entorno virtual activado, ejecuta el archivo principal:

```
python main.py
```

Esto mostrará la ejecución de los tres enfoques de concurrencia y los tiempos de cada uno.

---

## Notas

- Los ejemplos usan tareas pesadas simuladas para observar el comportamiento de cada enfoque.
- Los resultados pueden variar dependiendo del sistema operativo y la carga del sistema.
- La programación asíncrona (`asyncio`) es más eficiente para tareas I/O-bound, mientras que los procesos pueden aprovechar múltiples núcleos para tareas CPU-bound.

---
