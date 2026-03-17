import requests
from prefect import flow, task
from prefect import get_run_logger

# Parte 2: Modificar y generar un ejemplo con jsonplaceholder

@task(retries=2, retry_delay_seconds=2)
def obtener_posts(url: str):
    logger = get_run_logger()
    logger.info(f"Solicitando posts: {url}")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Error HTTP {response.status_code} al obtener posts")
    data = response.json()
    logger.info(f"Recibidos {len(data)} posts")
    return data

@task
def filtrar_posts_por_usuario(posts: list[dict], user_id: int):
    logger = get_run_logger()
    filtrados = [p for p in posts if p.get("userId") == user_id]
    logger.info(f"Filtrados {len(filtrados)} posts para userId={user_id}")
    return filtrados

@task
def tarea_fallida_controlada(valor: int):
    logger = get_run_logger()
    logger.info(f"Ejecutando tarea_fallida_controlada con valor={valor}")
    # Ejemplo de Task Failed Successfully: la tarea lanza excepción, pero el flujo captura.
    if valor < 0:
        raise ValueError("Valor negativo detectado - fallo intencional")
    return valor * 2

@task
def procesar_posts(posts: list[dict]):
    logger = get_run_logger()
    logger.info("Procesando posts para mostrar resumen")
    titulos = [p.get("title", "") for p in posts[:5]]
    logger.info("Primeros 5 títulos:")
    for i, t in enumerate(titulos, start=1):
        logger.info(f" {i}. {t}")
    return len(posts)

@flow(name="prefect-jsonplaceholder-ejemplo")
def flujo_jsonplaceholder(user_id: int = 1):
    url = "https://jsonplaceholder.cypress.io/posts"
    posts = obtener_posts(url)

    # Ejemplo de manejo de "Task failed successfully".
    try:
        valor = tarea_fallida_controlada(-5)
        get_run_logger().info(f"Resultado valor: {valor}")
    except Exception as e:
        get_run_logger().warning(f"Tarea controlada falló como se esperaba: {e}")
        # Task failed but flujo continúa: Task Failed Successfully

    posts_usuario = filtrar_posts_por_usuario(posts, user_id)
    cantidad = procesar_posts(posts_usuario)
    get_run_logger().info(f"Cantidad de posts de userId={user_id}: {cantidad}")
    return {
        "total_posts_usuario": cantidad,
        "usuario": user_id,
    }

if __name__ == "__main__":
    flujo_jsonplaceholder(1)
