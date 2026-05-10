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

* **Análisis Cinemático - Referencia 1:** [Mecanismo biela - manivela - corredera | Análisis cinemático | SolidWorks](https://youtu.be/6QLbw1xS8sg?si=8fuSzFIXMK4U_QsU)
* **Análisis Cinemático - Referencia 2:** [Simulación de movimiento en Solidworks. Mecanismo biela-manivela](https://youtu.be/_ggUQRI91M0?si=aOPVly7H2sfQ7lVz)

### Simulación en Autodesk Inventor
Se contó con una simulación base configurada a una velocidad angular de **150 RPM (942 deg/s)**, cortesía del **Prof. Efraín Terán**. A partir de este modelo, se obtuvieron las curvas de aceleración características para el punto central de la biela.

<div align="center">
  <img src="./img/grafica_aceleracion_1.png" alt="Gráfica de Aceleracion 1 - Simulación Inventor" width="400">
  <p><i>Figura 1: Curvas de aceleración del punto central de la biela (Referencia: Prof. Efraín Terán).</i></p>
</div>

<div align="center">
  <img src="./img/Grafica_Aceleracion_2.png" alt="Gráfica de Aceleración 2 - Simulación Inventor" width="400">
  <p><i>Figura 2: Curvas de aceleración del punto central de la biela (Referencia: Prof. Efraín Terán).</i></p>
</div>

> **Nota aclaratoria:** La simulación original se desarrolló con dimensiones menores a las del prototipo final impreso en 3D. Sin embargo, se mantiene la orientación y tendencia de las curvas cinemáticas como patrón de comparación para las pruebas experimentales.

### Resultados Esperados
A través de estas simulaciones se definieron los patrones de referencia para:
1.  **Velocidad Angular**
2.  **Aceleración** 

## 3. Fabricación e Impresión 3D

En esta sección se detallan las consideraciones tomadas para la materialización física del mecanismo. El diseño original fue escalado y modificado para asegurar la funcionalidad mecánica y la facilidad de montaje.

### Archivos de Diseño (CAD)
Los archivos necesarios para la fabricación y edición se encuentran en la carpeta `/cad` del repositorio, organizados de la siguiente manera:

* **Formatos Originales:** Archivos de pieza y ensamble en **SolidWorks 2025**.
* **Formatos de Intercambio (.STEP):** Archivos compatibles con otros softwares de CAD como **Autodesk Inventor**, facilitando su uso académico.

<div align="center">
  <img src="./img/ensamblaje_original.png" alt="Ensamblaje Original en SolidWorks" width="600">
  <p><i>Figura 3: Vista del ensamblaje original diseñado en SolidWorks 2025.</i></p>
</div>

* **Archivos Optimizados:** Se incluyen las versiones finales de las piezas donde se aplicaron ajustes de tolerancias para garantizar el acoplamiento real tras la impresión.

<div align="center">
  <img src="./img/Manivela.png" alt="Manivela" width="400">
  <p><i>Figura 4: Manivela optimizada para acople con motor.</i></p>
</div>

<div align="center">
  <img src="./img/Biela.png" alt="Biela" width="400">
  <p><i>Figura 5: Biela con ajuste de tolerancia en los nodos de articulación.</i></p>
</div>

<div align="center">
  <img src="./img/Corredera.png" alt="Corredera" width="400">
  <p><i>Figura 6: Corredera (Pistón) diseñada para deslizamiento de baja fricción.</i></p>
</div>

<div align="center">
  <img src="./img/Base_para_motor.png" alt="Base para motor" width="400">
  <p><i>Figura 7: Soporte estructural para el motorreductor/actuador.</i></p>
</div>

<div align="center">
  <img src="./img/Base_para_corredera.png" alt="Base para corredera" width="400">
  <p><i>Figura 8: Guía lineal para el desplazamiento de la corredera.</i></p>
</div>

### Resultado Final (Prototipo Físico)

Tras el proceso de impresión y ajuste manual, este es el resultado del mecanismo ensamblado y funcional:

<div align="center">
  <img src="./img/resultado_fisico.png" alt="Mecanismo Fisico" width="600">
  <p><i>Figura 9: Prototipo final impreso en 3D con sistema de adquisición de datos integrado.</i></p>
</div>

### Ajuste de Tolerancias y Montaje
Un aspecto crítico del proyecto fue el ajuste de las dimensiones de los agujeros y ejes para permitir una articulación fluida. 

> **Nota técnica sobre impresión 3D:** Debido a las variaciones en la precisión de las impresoras 3D (contracción del material y resolución de ejes), las dimensiones de los acoples fueron optimizadas mediante un proceso de **prueba y error**. 
> 
> * Se realizaron múltiples iteraciones de impresión para ajustar los diámetros internos de los alojamientos de los pasadores.
> * Se recomienda al usuario verificar la calibración de su impresora antes de proceder con la fabricación completa.

## 3. Metodología Experimental

Para validar el comportamiento del mecanismo impreso en 3D, se utilizaron dos métodos de adquisición de datos:

* **Acelerometría (Hardware):** Un sensor acelerómetro conectado a un **Arduino Uno** montado sobre la corredera para medir las variaciones de velocidad y aceleración en tiempo real.
* **Análisis de Video (Software):** Procesamiento de imágenes a partir de un video del mecanismo en funcionamiento para extraer las curvas cinemáticas mediante el seguimiento de puntos de referencia.

