import time

def heavy_task(n):
    """
    Función que simula una tarea pesada sumando números del 0 al n-1.
    """
    total = 0
    for i in range(n):
        total += i
    return total

def print_start_end(name):
    print(f"[{name}]")
    start = time.time()
    result = heavy_task(10_000_000)
    end = time.time()
    print(f"[{name}] - Resultado: {result}")
    print(f"[{name}] - Tiempo: {round(end - start, 3)}s")