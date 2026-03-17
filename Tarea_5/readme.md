# Monitor de Tolerancia a Fallas - Scraper de Precios Amazon

## Problema que se resuelve

El objetivo es desarrollar un **sistema de monitoreo de precios en Amazon** que funcione de forma continua y automática. El servidor web local necesita estar siempre disponible para consultar los precios en tiempo real, sin intervención manual del usuario.

## Ejecución en segundo plano

Este sistema **requiere ejecutarse en segundo plano** por las siguientes razones:

- El monitor debe verificar constantemente el estado del servidor web sin bloquear otras tareas del usuario.
- El servicio de Windows (`MonitorScraperAmazon`) permite que la aplicación se inicie automáticamente al encender la PC.
- El servidor Flask debe estar siempre disponible para recibir peticiones HTTP, independientemente de si el usuario está trabajando en otras aplicaciones.

## Tipos de fallas que pueden ocurrir

1. **Caída del proceso de scraping**: El servidor Flask puede cerrarse por error, excepción no controlada o falta de recursos.
2. **Pérdida de conexión HTTP**: El monitor intenta conectarse pero recibe timeout o error de conexión.
3. **Respuesta inusual del servidor**: El servidor responde con códigos de estado diferentes a 200.
4. **Crash del sistema**: Apagado inesperado o reinicio de la PC.
5. **Bloqueo por Amazon**: La página puede devolver CAPTCHA o bloquear la IP temporal o permanentemente.

## Estrategia de Tolerancia a Fallas Aplicada

### **Heartbeat (Latido del Corazón)**
- El monitor realiza peticiones HTTP periódicamente (cada 5 segundos) al endpoint `/health` del servidor.
- Si recibe una respuesta `200 OK`, el sistema está saludable.

### **Detección y Reinicio Automático**
- Si el monitor **no recibe respuesta** o falla la conexión, automáticamente:
  - Termina el proceso anterior (si aún existe).
  - Levanta una nueva instancia del servidor Flask.
  - Espera 3 segundos a que arrange completamente antes de reanudar los chequeos.

### **Servicio de Windows**
- El servicio `MonitorScraperAmazon` garantiza que:
  - El monitor se inicie automáticamente al encender la PC.
  - Si el monitor falla, Windows puede intentar reiniciarlo (dependiendo de la configuración).
  - Los logs se registran persistentemente en `monitor_fallas.log`.

### **Logging persistente**
- Se mantiene un registro detallado de todos los eventos en `monitor_fallas.log` y `scraper.log` para auditoría y debugging.

---

## Servicio de Windows Instalado

![Servicio MonitorScraperAmazon](./monitor_servicio.png)

*El servicio `MonitorScraperAmazon` (PID: 23876) aparece en la lista de servicios de Windows con estado "En ejecución", garantizando que el monitor se inicie automáticamente con el sistema operativo y se reinicie en caso de falla.*

---

## Estructura del proyecto

- **`monitor_servicio.py`**: Servicio de Windows que vigila y reinicia la aplicación.
- **`monitor.py`**: Monitor alternativo de línea de comandos (sin servicio de Windows).
- **`scraper.py`**: Servidor Flask que realiza el scraping y expone los endpoints HTTP.
- **`monitor_fallas.log`**: Registro de eventos del monitor.
- **`scraper.log`**: Registro de eventos de la aplicación.
