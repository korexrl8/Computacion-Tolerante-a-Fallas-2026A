# Tarea 6 - Prefect + JsonPlaceholder

## 📌 Objetivo
Implementar una tarea en Prefect siguiendo el tutorial "Getting Started with Prefect (PyData Denver)", luego modificar el ejemplo para consumir un endpoint de `jsonplaceholder.cypress.io` y mostrar un flujo con manejo de error (Task Failed Successfully).

## 🧠 ¿Qué es Prefect?
Prefect es un orquestador de flujos de trabajo en Python. Define `@task` para unidades de trabajo y `@flow` para pipelines. Prefect permite reintentos, dependencias, registrar resultados y ejecutar flujos localmente o en Prefect Cloud.

## ✅ Estructura del repositorio
- `parte_1.py`: Ejemplo básico de Prefect (tasks `saludame`, `sumar`, `dividir` y flow `flujo_basico`).
- `parte2_2.py`: Ejemplo con `jsonplaceholder.cypress.io/posts`, filtrado por `userId`, y manejo de tarea fallida intencional.
- `README.md`: Documentación de la tarea.

## 🚀 Requisitos
- Python 3.10+
- Dependencias:
  - `prefect`
  - `requests`

Instalar dependencias:

```bash
python -m pip install prefect requests
```

## ▶️ Cómo ejecutar
1. Ejecutar parte 1:

```bash
cd Tarea_6
python parte_1.py
```

2. Ejecutar parte 2:

```bash
cd Tarea_6
python parte2_2.py
```

## 🧪 Comportamiento demostrado
- `parte_1.py`: flujo simple con tareas y logs. Termina en estado `Completed`.
- `parte2_2.py`: consulta posts del endpoint `https://jsonplaceholder.cypress.io/posts`, filtra por `userId`, muestra primeros 5 títulos y demuestra un error intencional capturado (`Task Failed Successfully`).

## 📌 Detalles importantes
- En `parte2_2.py`, se usa un `@task` con exception para simular falla intencional y comprobar que el flujo continúa.
- El enlace usado para datos de ejemplo es:
  - `https://jsonplaceholder.cypress.io/posts`

## 🔗 Referencias
- Video del tutorial: "Getting Started with Prefect (PyData Denver)"
- Documentación Prefect: https://docs.prefect.io/
- Endpoint JSONPlaceholder: https://jsonplaceholder.cypress.io/

## 📝 Resultado de la ejecución
- `parte_1.py`: Flow run `prefect-primera-ejecucion` terminado correctamente.
- `parte2_2.py`: Flow run `prefect-jsonplaceholder-ejemplo` con tarea fallida controlada y flujo completado.
