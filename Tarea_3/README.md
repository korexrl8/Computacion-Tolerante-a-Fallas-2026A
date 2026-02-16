# Checkpointing - Restauración de Estado de Ejecución

## 📋 Descripción del Tema

El **checkpointing** es una técnica fundamental en la **computación tolerante a fallas** que permite guardar el estado de un programa en momentos específicos durante su ejecución. Si ocurre un fallo o la ejecución se interrumpe, el programa puede restaurarse desde el último punto guardado (checkpoint) en lugar de comenzar desde cero.

### ¿Por qué es importante?
- **Recuperación de fallos**: Ante interrupciones, puede continuar desde donde se pausó
- **Ahorro de recursos**: Evita rehacer trabajo ya completado
- **Sistemas confiables**: Esencial para procesos largos y críticos
- **Tolerancia a errores**: Mejora la robustez de aplicaciones

---

## 🎯 Objetivo de la Tarea

Desarrollar un programa que sea capaz de:
1. Guardar el estado de ejecución en puntos estratégicos
2. Recuperar ese estado si el programa falla o se interrumpe
3. Continuar la ejecución desde el punto guardado en lugar de reiniciar

---

## 🔍 Análisis del Código

### **1. Importaciones**
```python
import pickle
import os
import time
```
- **`pickle`**: Módulo para serializar (convertir a bytes) y deserializar objetos Python
- **`os`**: Para operaciones del sistema operativo (verificar existencia de archivos)
- **`time`**: Para simular operaciones que tardan tiempo

### **2. Configuración Global**
```python
CHECKPOINT_FILE = "checkpoint.pkl"
```
- Define el nombre del archivo donde se guardará el estado
- Usa extensión `.pkl` (pickle) para indicar que es un archivo serializado

---

## 🛠️ Funciones Principales

### **`save_checkpoint(state)`**
**¿Qué hace?** Guarda el estado actual en un archivo

```python
def save_checkpoint(state):
    with open(CHECKPOINT_FILE, "wb") as f:
        pickle.dump(state, f)
```

**Detalles:**
- Abre el archivo en modo **"wb"** (escritura binaria)
- `pickle.dump()` convierte el objeto `state` (diccionario) a formato binario
- Escribe los bytes al archivo
- Al salir del bloque `with`, el archivo se cierra automáticamente

**Parámetro:**
- `state`: Diccionario con los datos a guardar (ej: `{"counter": 5}`)

---

### **`load_checkpoint()`**
**¿Qué hace?** Restaura el estado previamente guardado o retorna None

```python
def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "rb") as f:
            return pickle.load(f)
    return None
```

**Detalles:**
- Verifica si el archivo de checkpoint existe
- Si existe:
  - Abre el archivo en modo **"rb"** (lectura binaria)
  - `pickle.load()` convierte los bytes al objeto Python original
  - Retorna el estado restaurado
- Si no existe (primera ejecución): Retorna `None`

---

### **`main()`**
**¿Qué hace?** Orquesta el flujo principal del programa

```python
def main():
    # Intentar restaurar estado
    state = load_checkpoint()
```
**Paso 1: Recuperación del Estado**
- Intenta cargar un checkpoint anterior
- Si existe, obtiene el contador; si no, comienza desde 0

```python
    if state is None:
        print("Iniciando desde cero")
        counter = 0
    else:
        print("Restaurando desde checkpoint")
        counter = state["counter"]
```

**Paso 2: Decisión del Punto de Inicio**
- Si es la primera ejecución: `counter = 0`
- Si se restaura: `counter` toma el valor guardado (continúa desde ahí)

```python
    for i in range(counter, 50):
        print("Procesando:", i)
        time.sleep(0.5)
```

**Paso 3: Bucle Principal**
- Itera desde el contador actual hasta 50
- Simula un proceso con `time.sleep(0.5)` (representa operaciones costosas)
- La función `range()` permite reiniciar desde donde se pausó

```python
        save_checkpoint({
            "counter": i + 1
        })
```

**Paso 4: Guardado Periódico**
- Después de cada iteración, guarda el progreso
- Incrementa el contador en 1 para la próxima sesión

---

## 🚀 Cómo Usar el Programa

### **Primera Ejecución**
```bash
python Checkpointing.py
```
**Resultado:**
- Imprime: "Iniciando desde cero"
- Procesa items 0-49
- Guarda el estado en `checkpoint.pkl`

### **Interrumpir y Reanudar**
1. **Durante la ejecución**, presiona `Ctrl+C` para detenerlo (ej: en el ítem 10)
2. **Vuelve a ejecutar** el programa:
   ```bash
   python Checkpointing.py
   ```
3. **Resultado:**
   - Imprime: "Restaurando desde checkpoint"
   - Continúa desde el ítem 11 (no repite el trabajo anterior)

---

## 📦 Tecnologías Utilizadas

| Tecnología    | Propósito                                     |
|-------------- | --------------------------------------------- |
| **Python 3**  | Lenguaje de programación                      |
| **pickle**    | Serialización de objetos para almacenamiento  |
| **os**        | Manejo del sistema de archivos                |
| **time**      | Simulación de operaciones con latencia        |

---

## 📊 Flujo de Ejecución

```
┌─────────────────────────────────────┐
│   Inicio del Programa               │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   ¿Existe checkpoint.pkl?           │
└─────────────────────────────────────┘
       │                  │
      SÍ                  NO
       │                  │
       ▼                  ▼
  Cargar estado      Iniciar desde 0
  (counter valor    (counter = 0)
   guardado)
       │                  │
       └──────┬───────────┘
              ▼
┌─────────────────────────────────────┐
│   Procesar item i                   │
│   (Operación simulada 0.5s)         │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Guardar Checkpoint                │
│   (state = {"counter": i+1})        │
└─────────────────────────────────────┘
              │
              ▼
       ¿i < 49?
       │      │
      SÍ      NO
       │      │
       ▼      ▼
    Continuar  Fin
```

---

## ✨ Ventajas de Esta Implementación

✅ **Simple y clara**: Código fácil de entender  
✅ **Eficiente**: Solo guarda lo esencial (contador)  
✅ **Modular**: Funciones separadas para cargar y guardar  
✅ **Reutilizable**: Fácil de adaptarla a otros proyectos  
✅ **Segura**: Usa `with` para manejar archivos correctamente  

---

## 📝 Notas Importantes

- El archivo `checkpoint.pkl` se crea en la misma carpeta del script
- Para reiniciar completamente, borra `checkpoint.pkl` manualmente
- `pickle` es seguro para datos internos, pero no uses archivos `.pkl` no confiables
- Para sistemas de producción, considera usar bases de datos o formatos como JSON

---

## Conclución

Desde mi punto de vista, para entender el tema de checkpointing tuve que pensarlo como si fuera un videojuego: guardar la partida antes de apagar la computadora y poder continuar después. El programa mostrado es un ejemplo básico pero eficaz, ya que demuestra cómo el checkpointing permite guardar el estado de ejecución para poder retomar el proceso desde donde se quedó.

---

**Tema:** Checkpointing y Recuperación de Estado  
**Fecha:** 16/02/2026
