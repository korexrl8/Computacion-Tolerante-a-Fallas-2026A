import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import requests
import logging
import os
import sys

# --- RUTAS ABSOLUTAS AUTOMÁTICAS (Crítico para Servicios de Windows) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'monitor_fallas.log')
APP_SCRIPT = os.path.join(BASE_DIR, 'scraper.py')
# Detectamos qué Python estás usando para usar el mismo en el subproceso
PYTHON_EXE = r"C:\Users\Kore\AppData\Local\Programs\Python\Python313\python.exe"

# Configuración del log
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - SERVICIO - %(message)s')

class MonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MonitorScraperAmazon" # Nombre interno en Windows
    _svc_display_name_ = "Monitor Tolerancia a Fallas (Scraper)" # Nombre que verás
    _svc_description_ = "Vigila y mantiene vivo el servidor web local."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Evento para escuchar cuando Windows nos pida detener el servicio
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.proceso = None

    def SvcStop(self):
        """Se ejecuta cuando detienes el servicio o apagas la PC."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        
        # Si apagamos el servicio, también matamos la app de Flask por limpieza
        if self.proceso and self.proceso.poll() is None:
            logging.info("Apagando la app web...")
            self.proceso.terminate()
            self.proceso.wait()
        logging.info("Servicio detenido por Windows.")

    def SvcDoRun(self):
        """Se ejecuta al iniciar el servicio."""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def iniciar_app(self):
        logging.info(f"Levantando {APP_SCRIPT}...")
        # cwd=BASE_DIR asegura que Flask sepa dónde está parado
        return subprocess.Popen([PYTHON_EXE, APP_SCRIPT], cwd=BASE_DIR)

    def main(self):
        logging.info("=== Servicio Monitor de Windows INICIADO ===")
        self.proceso = self.iniciar_app()
        
        # Esperamos 3 segundos a que Flask arranque
        win32event.WaitForSingleObject(self.hWaitStop, 3000)
        url_health = "http://127.0.0.1:5000/health"

        while self.is_running:
            try:
                # El Latido (Heartbeat)
                respuesta = requests.get(url_health, timeout=3)
                if respuesta.status_code != 200:
                    logging.warning(f"Estado inusual: {respuesta.status_code}")
                    
            except requests.exceptions.RequestException:
                # Falla detectada (Tolerancia a Fallas en acción)
                logging.error("Caída detectada. Reiniciando el proceso de scraping...")
                if self.proceso and self.proceso.poll() is None:
                    self.proceso.terminate()
                    self.proceso.wait()
                
                self.proceso = self.iniciar_app()
                win32event.WaitForSingleObject(self.hWaitStop, 3000)
            
            # En lugar de time.sleep(), usamos el evento de Windows. 
            # Así, si apagas la PC, no se queda congelado esperando 5 segundos.
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonitorService)