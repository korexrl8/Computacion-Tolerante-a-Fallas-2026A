import asyncio
import time

async def async_heavy_task(name):
    print(f"[{name}] - Iniciando async")
    await asyncio.sleep(0)  # Cooperativo
    start = time.time()
    total = sum(range(10_000_000))
    end = time.time()
    print(f"[{name}] -  Resultado: {total}")
    print(f"[{name}] - Tiempo async: {round(end - start,3)}s")

async def run_async():
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(async_heavy_task(f"Async-{i+1}")))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("=== Ejecutando con Asyncio ===")
    asyncio.run(run_async())