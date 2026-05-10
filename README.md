# Diseño e Implementación de un Mecanismo Manivela Corredera Impreso en 3D con Adquisicion de Datos
Diseño, impresión 3D y análisis cinemático de un mecanismo biela-manivela utilizando Arduino (acelerometría) y software de análisis de video para la validación de curvas de velocidad y aceleración.

# Análisis Dinámico de un Mecanismo Biela-Manivela-Corredera en 3D

Este repositorio contiene el desarrollo, fabricación y validación experimental de un mecanismo biela-manivela-corredera. El proyecto integra diseño mecánico, impresión 3D, electrónica con Arduino y análisis de video por computadora.

## 1. Fundamento Teórico

El mecanismo de **biela-manivela-corredera** es un sistema de eslabonamiento diseñado para transformar el movimiento circular en movimiento lineal alternativo o viceversa.

### Definición Técnica
Es un mecanismo de cuatro barras donde uno de los eslabones (la corredera) tiene una articulación de pasador en un extremo y una articulación de deslizamiento (prismática) respecto al eslabón fijo. En este proyecto, el mecanismo se compone de:

1.  **Manivela:** El eslabón que realiza una rotación completa de 360°.
2.  **Biela:** El eslabón que conecta la manivela con la corredera.
3.  **Corredera:** El eslabón que realiza el movimiento de traslación lineal.

## 2. Modelado y Simulación en SolidWorks

Como etapa previa a la fabricación física, se realizó el modelado tridimensional y la simulación cinemática del mecanismo utilizando **SolidWorks**. Esta fase fue fundamental para asegurar la viabilidad del diseño antes de la impresión 3D.

### Referencias de Diseño y Metodología
Para el desarrollo del modelo, se tomaron como base metodológica dos análisis cinemáticos de referencia. Estos recursos fueron esenciales para el ajuste de medidas y la comprensión de las restricciones de movimiento:

* **Video Guía 1:** [Mecanismo biela - manivela - corredera | Análisis cinemático | SolidWorks](https://youtu.be/6QLbw1xS8sg?si=KsOmOA9TbFXreo4o)
* **Video Guía 2:** [Simulación de movimiento en Solidworks. Mecanismo biela-manivela](https://youtu.be/_ggUQRI91M0?si=5zGyvBaKSrtSLi-u).

### Simulación Cinemática
Se ejecutó un estudio de movimiento (*Motion Study*) en el software para obtener las curvas teóricas de referencia:
1.  **Velocidad Lineal:** Observando el comportamiento del desplazamiento de la corredera.
2.  **Aceleración:** Identificando los puntos de máxima inercia para su posterior contraste experimental.

## 3. Metodología Experimental

Para validar el comportamiento del mecanismo impreso en 3D, se utilizaron dos métodos de adquisición de datos:

* **Acelerometría (Hardware):** Un sensor acelerómetro conectado a un **Arduino Uno** montado sobre la corredera para medir las variaciones de velocidad y aceleración en tiempo real.
* **Análisis de Video (Software):** Procesamiento de imágenes a partir de un video del mecanismo en funcionamiento para extraer las curvas cinemáticas mediante el seguimiento de puntos de referencia.

