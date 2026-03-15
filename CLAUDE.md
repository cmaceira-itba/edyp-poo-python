# Configuración de Proyecto: Notebook de POO para estudiantes universitarios

## Perfil del Usuario
- Rol: Docente universitario.
- Ubicación/Dialecto: Argentina (usar voseo: "podés", "hacé", "fijate", evitar "vosotros" o terminología de España).
- Enfoque: Técnico, profesional pero con matices de experiencia práctica (experiencial).

## Objetivo
La idea de este documento es servir como una referencia extra a los conocimientos y experiencias que transmitimos verbalmente a los alumnos en clase. Para ello se sustenta en los referentes de la Programacion Orientada a Objetos como:
- Grady Booch
- Bertrand Meyer
- Alan Kay
- Martin Fowler
- Robert C. Martin
Este documento ayudara a los alumnos a entender que es el analisis y diseño orientado a objetos correcto, como se contrasta con el analisis y diseño procedural. Explicara el cambio de mentalidad que supone el analisis y diseño orientado a objetos.

## Público
Esta guia esta orientada servir de material para docentes universitarios que enseñan programacion orientada a objetos en Python a alumnos que no poseen experiencia previa con programacion orientada a objetos y no estudian carreras de informatica. Si deben tener conocimientos previos de python, pero no de POO.

## Guía de Estilo de Redacción (Technical Writing)
- **Tono:** Educativo y preciso. Los conceptos deben ser claros para un nivel de ingeniería.
- **Estructura:** Usar jerarquía de Markdown (H1 para temas macro, H2 para conceptos como Encapsulamiento, H3 para subtemas).
- **Idioma:** Español rioplatense. Evitar palabras como "ordenador", "fichero" o "aparcar". Usar "computadora", "archivo", "notebook".
- **Contenido:** Al mejorar la redacción, integrar las "experiencias propias" del autor de forma que se distingan de la teoría de los libros (ej: "En la práctica, esto suele causar problemas cuando...").

## Guía de Estilo de Código (Refactoring)
- **Estándar:** Python 3.10+ siguiendo PEP 8.
- **POO:** - Preferir Composición sobre Herencia siempre que sea posible.
    - Usar `Type Hinting` explícito en todos los métodos y constructores.
    - Implementar `super()` correctamente en herencia.
    - Los snippets deben ser modulares y listos para ejecutar en celdas de Colab.
- **Documentación:** Cada clase/método refactorizado debe incluir Docstrings en formato Google o NumPy.
- **Estilo**: Preferir codigo limpio y legible, con comentarios explicativos cuando sea necesario.

## Instrucciones para el Agente
- Al editar el archivo `.ipynb`, mantené la separación clara entre celdas de Markdown (teoría) y celdas de Code (snippets).
- Si encontrás un snippet que contradice una buena práctica de arquitectura, proponé la corrección pero explicá el "por qué" basándote en principios de diseño (SOLID, etc.).

## Testing
- **Framework:** Todo el testing unitario debe usar `pytest`. No usar `unittest` bajo ninguna circunstancia.
- Los snippets de testing deben ser ejecutables en Colab (instalar pytest con `!pip install pytest` si es necesario).
- Usar funciones sueltas con prefijo `test_` (estilo pytest), no clases heredando de `unittest.TestCase`.

## Temas puntuales a cubrir
- **Introducción a POO**: ¿Qué es?, ¿Qué cambia?, Características.
- **Clase y Objeto**: ¿En qué se diferencian? Conceptos fundamentales.
- **Conceptos**: Clases, atributos, métodos, relación entre clases.
- **Test de clases** (con pytest).
- **Métodos**: Clase, instancia, estáticos y mágicos.
- **Herencia y Objetos**.
- **Excepciones**.
