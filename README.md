# Diseño e Implementación de un Mecanismo Biela-Manivela-Corredera Impreso en 3D con Adquisicion de Datos
Diseño, impresión 3D y análisis cinemático de un mecanismo biela-manivela utilizando Arduino (acelerometría) y software de análisis de video (tracker) para la validación de curvas de velocidad y aceleración.

# Análisis Dinámico de un Mecanismo Biela-Manivela-Corredera en 3D

Este repositorio contiene el desarrollo, fabricación y validación experimental de un mecanismo biela-manivela-corredera. El proyecto integra diseño mecánico, impresión 3D, electrónica con Arduino y análisis de video por computadora.

## 1. Fundamento Teórico

El mecanismo de **biela-manivela-corredera** es un sistema de eslabonamiento diseñado para transformar el movimiento circular en movimiento lineal alternativo o viceversa.

### Definición Técnica
Es un mecanismo de cuatro barras donde uno de los eslabones (la corredera) tiene una articulación de pasador en un extremo y una articulación de deslizamiento (prismática) respecto al eslabón fijo. En este proyecto, el mecanismo se compone de:

1.  **Manivela:** El eslabón que realiza una rotación completa de 360°.
2.  **Biela:** El eslabón que conecta la manivela con la corredera.
3.  **Corredera:** El eslabón que realiza el movimiento de traslación lineal.

## 2. Modelado y Simulación Cinemática

Se realizó el modelado tridimensional y el análisis de movimiento del mecanismo. Esta fase permitió validar el comportamiento dinámico y ajustar las medidas de los eslabones.

### Referencias de Diseño
Para el desarrollo del modelo en SolidWorks, se tomaron como base metodológica los siguientes recursos:

* **Análisis Cinemático - Referencia 1:** [Nombre del Video 1](URL_VIDEO_1)
* **Análisis Cinemático - Referencia 2:** [Nombre del Video 2](URL_VIDEO_2)

### Simulación en Autodesk Inventor
Se contó con una simulación base configurada a una velocidad angular de **150 RPM (942 deg/s)**, cortesía del **Prof. Efraín Terán**. A partir de este modelo, se obtuvieron las curvas de aceleración características para el punto central de la biela.

> **Nota aclaratoria:** La simulación original se desarrolló con dimensiones menores a las del prototipo final impreso en 3D. Sin embargo, se mantiene la orientación y tendencia de las curvas cinemáticas como patrón de comparación para las pruebas experimentales.

### Resultados Esperados
A través de estas simulaciones se definieron los patrones de referencia para:
1.  **Velocidad Angular**
2.  **Aceleración** 

## 3. Metodología Experimental

Para validar el comportamiento del mecanismo impreso en 3D, se utilizaron dos métodos de adquisición de datos:

* **Acelerometría (Hardware):** Un sensor acelerómetro conectado a un **Arduino Uno** montado sobre la corredera para medir las variaciones de velocidad y aceleración en tiempo real.
* **Análisis de Video (Software):** Procesamiento de imágenes a partir de un video del mecanismo en funcionamiento para extraer las curvas cinemáticas mediante el seguimiento de puntos de referencia.

