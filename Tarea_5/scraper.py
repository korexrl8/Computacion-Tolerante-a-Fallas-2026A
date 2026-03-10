from flask import Flask, jsonify
import logging
import requests
from bs4 import BeautifulSoup
import os
import signal

app = Flask(__name__)

# Configuración del registro persistente
logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                    format='%(asctime)s - APP - %(message)s')

# URL del producto que quieres vigilar (Cámbiala por la que quieras)
URL_PRODUCTO = "https://www.amazon.com.mx/AMD-Ryzen-5600GT-Procesador-sobremesa/dp/B0CQ4DTJYX/?_encoding=UTF8&pd_rd_w=2BGo7&content-id=amzn1.sym.1d43a0e5-652d-470f-8bfb-903770744fec%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=1d43a0e5-652d-470f-8bfb-903770744fec&pf_rd_r=GAAYN7CF7RGN52YWSW1B&pd_rd_wg=N7l2Y&pd_rd_r=b4fe5bba-bcdb-48f8-b897-510445568b4a&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d"

def obtener_precio_amazon(url):
    """Hace scraping real a la página de Amazon."""
    # Los headers son obligatorios para que Amazon no nos bloquee inmediatamente
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        logging.info("Consultando Amazon de forma real...")
        respuesta = requests.get(url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.content, "html.parser")
            
            # Buscamos la clase CSS donde Amazon suele guardar el precio
            precio_elem = soup.find("span", {"class": "a-offscreen"})
            
            if precio_elem:
                return precio_elem.text.strip()
            else:
                logging.warning("No se encontró el precio. Amazon podría haber cambiado la estructura o pedido un CAPTCHA.")
                return "Precio oculto"
        else:
            logging.error(f"Amazon respondió con código: {respuesta.status_code}")
            return f"Error HTTP {respuesta.status_code}"
            
    except Exception as e:
        logging.error(f"Falla al conectar con Amazon: {e}")
        return "Error de conexión"

@app.route('/')
def home():
    precio = obtener_precio_amazon(URL_PRODUCTO)
    logging.info(f"Precio consultado y mostrado al usuario: {precio}")
    return f"""
    <h1>Monitor de Precios Amazon</h1>
    <h2>Producto monitoreado: Ryzen 5 5600GT</h2>
    <p><a href='{URL_PRODUCTO}' target='_blank'>Ver producto original</a></p>
    <h3 style='color: green;'>Precio actual detectado: {precio}</h3>
    <p><small>Refresca la página para volver a hacer scraping.</small></p>
    """

@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "mensaje": "Servidor funcionando correctamente"})

@app.route('/matar')
def matar_servidor():
    """Simulador de falla crítica para probar el monitor."""
    logging.error("¡Falla crítica! El proceso principal ha colapsado.")
    os.kill(os.getpid(), signal.SIGINT) # Se cierra a sí mismo violentamente
    return "Servidor destruido."

if __name__ == '__main__':
    logging.info("Iniciando servidor Scraper local en el puerto 5000...")
    # Usamos threaded=True para poder recibir peticiones del usuario y del monitor al mismo tiempo
    app.run(port=5000, threaded=True)