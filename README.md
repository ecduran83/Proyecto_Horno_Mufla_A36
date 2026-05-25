# Diseño e Implementación de un Horno Tipo Mufla para Tratamientos Térmicos (Acero A36)

**Autor:** [Tu Nombre Completo]
**Universidad:** [Nombre de tu Universidad]
**Carrera:** Ingeniería [Tu Carrera]

## 📋 Descripción
Este repositorio contiene el código fuente y los recursos de ingeniería para el proyecto de grado titulado *"Diseño e implementación de un horno tipo mufla para tratamientos térmicos, caso templado en acero A36"*.

El proyecto consiste en un horno de resistencia eléctrica controlado por un sistema embebido, capaz de realizar perfiles de temperatura complejos para metalurgia.

## 📂 Estructura del Repositorio

* **/firmware**: Código fuente C++ para el microcontrolador **ESP32** (PlatformIO). Implementa el sistema operativo **FreeRTOS** y el algoritmo de control **PID**.
* **/software_pc**: Interfaz Gráfica de Usuario (GUI) desarrollada en **Python** con **PySide6**. Maneja el monitoreo, datalogging y programación de rampas.
* **/simulacion**: Scripts de **Pyhon** para el "modelado" del horno (Modelo de Diferencias Finitas) y sintonización de ganancias PID.
* **/docs**: Esquemas eléctricos, diagramas de flujo y fotografías del prototipo.

## 🚀 Tecnologías Utilizadas
* **Hardware:** ESP32, MAX31855 (Termopar K), SSR 25DA.
* **Software:** Python 3.10, PySide6 (Qt), PlatformIO, Jupyter Notebook.
* **Control:** PID Discreto en forma de velocidad, Modulación por tiempo (Time-Proportioning).

## ⚙️ Instalación y Uso

### Firmware
1. Abrir la carpeta `/firmware` en VS Code con la extensión PlatformIO instalada.
2. Compilar y subir al ESP32.

### Software PC
1. Instalar dependencias: `pip install -r software_pc/requirements.txt`
2. Ejecutar la interfaz: `python software_pc/main.py`

---
*Este código es parte de la defensa de grado presentada en [11/2025].*
