# SIPC-P3
# Inteacción con un motor de física 2D a través del reconocimiento de gestos
## Introducción
### Mediapipe
[**MediaPipe Hands**](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=es-419) es una librería para el seguimiento de manos y dedos de alta fidelidad.

Emplea aprendizaje automático para inferir 21 puntos de referencia 3D de una mano a partir de una sola imagen. 

Este método logra un rendimiento en tiempo real y se adapta a varias manos.

### Pymunk
Por su parte, [**Pymunk**](https://www.pymunk.org/en/latest/examples.html) es una librería de física 2D escrita en Python que permite integrar simulaciones físicas realistas en proyectos de programación, como videojuegos o animaciones. 

Utiliza el motor de física Chipmunk para manejar colisiones y efectos de gravedad, permitiendo que los desarrolladores simulen el movimiento de objetos, choques, rebotes, y más, de una forma sencilla y con código intuitivo. 

Es ideal para crear aplicaciones interactivas que requieran comportamientos físicos en dos dimensiones sin necesidad de conocimientos avanzados en física.

## Objetivo
Integrar **MediaPipe** y **Pymunk** para controlar una simulación física 2D con los gestos de la mano.

## Requisitos
- Modificación de la posición de un **elemento dinámico** de la simulación a través de la posición de la mano
- Modificación de la **posición y orientación** de un elemento dinámico de la simulación a través de la posición y orientación de la mano
- Uso de **colisiones**
- **Complejidad** de la funcionalidad desarrollada