# Diseno-e-Implementacion-de-un-Mecanismo-Manivela-Corredera-Impreso-en-3D-con-Adquisicion-de-Datos
Diseño, impresión 3D y análisis cinemático de un mecanismo biela-manivela utilizando Arduino (acelerometría) y software de análisis de video para la validación de curvas de velocidad y aceleración.

# Análisis Dinámico de un Mecanismo Biela-Manivela-Corredera en 3D

Este repositorio contiene el desarrollo, fabricación y validación experimental de un mecanismo biela-manivela-corredera. El proyecto integra diseño mecánico, impresión 3D, electrónica con Arduino y análisis de video por computadora.

## 1. Fundamento Teórico

Según la bibliografía base de la materia (Norton, Shigley y Mott), el mecanismo de **biela-manivela-corredera** es un sistema de eslabonamiento diseñado para transformar el movimiento circular en movimiento lineal alternativo o viceversa.

### Definición Técnica
Es un mecanismo de cuatro barras donde uno de los eslabones (la corredera) tiene una articulación de pasador en un extremo y una articulación de deslizamiento (prismática) respecto al eslabón fijo. En este proyecto, el mecanismo se compone de:

1.  **Manivela:** El eslabón que realiza una rotación completa de 360°.
2.  **Biela:** El eslabón que conecta la manivela con la corredera.
3.  **Corredera:** El eslabón que realiza el movimiento de traslación lineal.


## 2. Metodología Experimental

Para validar el comportamiento del mecanismo impreso en 3D, se utilizaron dos métodos de adquisición de datos:

* **Acelerometría (Hardware):** Un sensor acelerómetro conectado a un **Arduino Uno** montado sobre la corredera para medir las variaciones de velocidad y aceleración en tiempo real.
* **Análisis de Video (Software):** Procesamiento de imágenes a partir de un video del mecanismo en funcionamiento para extraer las curvas cinemáticas mediante el seguimiento de puntos de referencia.

## 3. Bibliografía

Este proyecto se apoya en los siguientes textos guía:

* **Norton, R. L. (2011).** *Diseño de máquinas: Un enfoque integrado*. 4ta Edición. Pearson Educación.
* **Budynas, R. G., & Nisbett, J. K. (2015).** *Shigley's Mechanical Engineering Design*. 10th Edition. McGraw-Hill Education.
* **Mott, R. L. (2006).** *Diseño de elementos de máquinas*. 4ta Edición. Pearson Educación.
