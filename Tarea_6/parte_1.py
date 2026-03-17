from prefect import flow, task
from prefect import get_run_logger

# Parte 1: Ejemplo básico de Prefect (similar al tutorial de Getting Started)

@task
def saludame(nombre: str) -> str:
    logger = get_run_logger()
    mensaje = f"Hola, {nombre}! Bienvenido a Prefect."
    logger.info(mensaje)
    return mensaje

@task
def sumar(a: int, b: int) -> int:
    logger = get_run_logger()
    resultado = a + b
    logger.info(f"Sumando {a} + {b} = {resultado}")
    return resultado

@task
def dividir(a: int, b: int) -> float:
    logger = get_run_logger()
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    resultado = a / b
    logger.info(f"Dividiendo {a} / {b} = {resultado}")
    return resultado

@flow(name="prefect-primera-ejecucion")
def flujo_basico(nombre: str = "estudiante"):
    saludo = saludame(nombre)
    suma = sumar(10, 5)
    cociente = dividir(suma, 2)
    logger = get_run_logger()
    logger.info(f"El flujo terminó. Saludo: {saludo}, suma: {suma}, cociente: {cociente}")
    return {
        "saludo": saludo,
        "suma": suma,
        "cociente": cociente,
    }

if __name__ == "__main__":
    flujo_basico("Clase de Prefect")
