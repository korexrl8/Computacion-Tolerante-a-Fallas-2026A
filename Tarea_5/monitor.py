import time
import requests
import subprocess
import logging

# Registro persistente del monitor
logging.basicConfig(filename='monitor_fallas.log', level=logging.INFO, 
                    format='%(asctime)s - MONITOR - %(message)s')

URL_HEALTH = "http://127.0.0.1:5000/health"
APP_SCRIPT = "scraper.py"

def iniciar_app():
    """Lanza el servidor local como un proceso independiente."""
    logging.info(f"Iniciando el proceso {APP_SCRIPT}...")
    print(f"[*] Levantando {APP_SCRIPT}...")
    return subprocess.Popen(["python", APP_SCRIPT])

def vigilar():
    proceso = iniciar_app()
    
    # Damos tiempo a que Flask arranque antes de hacer el primer chequeo
    time.sleep(3)
    
    while True:
        try:
            # El "Latido" (Heartbeat): comprobamos si está vivo
            respuesta = requests.get(URL_HEALTH, timeout=3)
            if respuesta.status_code == 200:
                print("[OK] El servidor está corriendo y saludable.")
            else:
                logging.warning(f"Respuesta inesperada del servidor: {respuesta.status_code}")
                
        except requests.exceptions.RequestException:
            # Si hay un error de conexión, el servidor está MUERTO.
            print("[!] ¡ALERTA! El servidor web cayó. Aplicando estrategia de tolerancia a fallas...")
            logging.error("Caída detectada. Reiniciando el proceso de scraping...")
            
            # Limpiamos el proceso anterior por seguridad
            if proceso.poll() is None:
                proceso.terminate()
                proceso.wait()
                
            # Lo revivimos automáticamente
            proceso = iniciar_app()
            
            # Esperamos un poco a que arranque de nuevo
            time.sleep(3)
            
        # Esperamos 5 segundos antes del siguiente chequeo
        time.sleep(5)

if __name__ == '__main__':
    print("=== Iniciando Sistema de Tolerancia a Fallas ===")
    logging.info("Monitor iniciado.")
    vigilar()