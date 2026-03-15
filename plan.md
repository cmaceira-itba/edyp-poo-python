# Plan de Revisión: Notebook POO en Python

> **Fecha:** 2026-03-15
> **Archivo objetivo:** `programacion_orientada_a_objetos.ipynb`
> **Estado actual:** 22 celdas (17 markdown, 2 código funcional, 2 código vacío)

---

## Diagnóstico General

### Problemas Identificados

| Categoría | Problema |
|---|---|
| **Estructura** | El orden actual mezcla teoría de paradigmas con prácticas de Python sin una progresión clara |
| **Código** | Solo 2 snippets funcionales en un curso de programación. Falta código para ~80% de los conceptos teóricos |
| **Temas faltantes** | Test de clases, Excepciones, Métodos (clase/instancia/estático/mágicos) carecen de secciones propias |
| **Redacción** | "Guía de Supervivencia" y "Principios y Buenas Prácticas" son redundantes y solapan contenido |
| **Índice** | No existe tabla de contenidos con vínculos internos |
| **SOLID** | Sección completa sin un solo snippet de código ilustrativo |
| **Contraste** | No hay ejemplos de código malo vs. código correcto para reforzar el aprendizaje |

---

## Estructura Propuesta (Orden de Celdas)

La nueva estructura reorganiza el notebook en 7 módulos con progresión pedagógica:
**Contexto → Fundamentos → Pilares → Clases en Python → Métodos → Relaciones → Calidad**

---

### MÓDULO 0 — Portada e Índice

**Celdas a crear:**

#### Celda 0 — Markdown: Título y Badge Colab
- Mantener badge de Colab actual
- Agregar título principal con H1, breve descripción del material y lista de prerequisitos

#### Celda 1 — Markdown: Índice con Vínculos
```markdown
## Índice

1. [¿Qué es un Paradigma de Programación?](#paradigma)
2. [El Paradigma Estructurado](#estructurado)
3. [Problemas del Diseño: Acoplamiento y Cohesión](#acoplamiento-cohesion)
4. [Código Limpio y SOLID](#solid)
5. [El Paradigma Orientado a Objetos](#poo)
6. [Los Cuatro Pilares del Modelo de Objetos](#pilares)
7. [Clases y Objetos en Python](#clases-objetos)
8. [Atributos y Métodos](#atributos-metodos)
9. [Métodos Especiales (Dunder)](#dunder)
10. [Herencia y Composición](#herencia)
11. [Excepciones](#excepciones)
12. [Testing de Clases](#testing)
13. [Fuentes](#fuentes)
```

**Acción:** Crear celda nueva. Los anchors de vínculos se generan automáticamente en Colab a partir de los encabezados H2/H3.

---

### MÓDULO 1 — Paradigmas de Programación

**Objetivo:** Contextualizar por qué existen diferentes paradigmas antes de presentar POO.

#### Celda — Markdown: `¿Qué es un Paradigma de Programación?` <a name="paradigma">
- **Acción:** Refrasear la introducción. Actualmente es correcta pero genérica.
- Agregar un párrafo con perspectiva propia: *"En la práctica, cuando los alumnos llegan a esta materia ya programan de forma estructurada sin saberlo..."*
- Mencionar explícitamente que Python es multiparadigma y que eso es una ventaja.

#### Celda — Markdown: Nota prerequisitos
- **Acción:** Reformular la nota actual. Actualmente dice "no se requieren prerequisitos de paradigmas" pero eso puede confundir. Clarificar que sí se requiere Python básico.

#### Celda — Markdown: `El Paradigma Estructurado` <a name="estructurado">
- **Acción:** Mantener con ajustes menores de redacción. Agregar los 3 ejemplos de estructuras de control como lista con ejemplos `if`, `for`, `def`.

#### Celda — Code: Ejemplo Paradigma Estructurado (REFACTOR)
- **Acción:** El ejemplo del factorial es bueno pero aislado. Agregar un segundo ejemplo que resuelva un problema más complejo (ej: gestión de inventario) de forma puramente estructural/procedural para luego contrastar con la versión OOP en el módulo 5.
```python
# VERSIÓN PROCEDURAL — se usará como contraste más adelante
# Gestión de un inventario simple
inventario = []

def agregar_producto(nombre: str, precio: float, stock: int) -> None:
    inventario.append({"nombre": nombre, "precio": precio, "stock": stock})

def buscar_producto(nombre: str) -> dict | None:
    for producto in inventario:
        if producto["nombre"] == nombre:
            return producto
    return None

def mostrar_inventario() -> None:
    for p in inventario:
        print(f"{p['nombre']}: ${p['precio']} (stock: {p['stock']})")
```

#### Celda — Markdown: `Código Espagueti`
- **Acción:** Agregar un snippet de código espagueti real con goto-like pattern usando flags booleanos y funciones encadenadas sin estructura. Actualmente es solo texto.
```python
# ❌ Ejemplo de código espagueti: validación con flags anidados
def procesar_pedido(usuario, items, descuento):
    ok = False
    total = 0
    if usuario:
        if len(items) > 0:
            for item in items:
                if item['stock'] > 0:
                    total += item['precio']
                    ok = True
                else:
                    ok = False
                    break
            if ok:
                if descuento > 0:
                    total = total - (total * descuento / 100)
    return total if ok else -1
```

---

### MÓDULO 2 — Problemas de Diseño: Acoplamiento y Cohesión <a name="acoplamiento-cohesion">

#### Celda — Markdown: Acoplamiento
- **Acción:** Mantener contenido, mejorar redacción. Agregar párrafo con experiencia práctica sobre por qué el acoplamiento alto es un problema en proyectos reales.

#### Celda — Code: Ejemplo Acoplamiento (REFACTOR)
- **Acción:** El snippet actual (`FileManager` + `OrderProcessor`) es bueno conceptualmente pero le falta:
  - Type hints en todos los métodos
  - Docstrings
  - Versión "corregida" a continuación mostrando bajo acoplamiento (inyección de dependencias)
  - Comentarios explicativos con `# ❌` y `# ✅`

```python
# ❌ ALTO ACOPLAMIENTO: OrderProcessor crea y controla FileManager
class FileManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write(self, data: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(data)

class OrderProcessor:
    def __init__(self) -> None:
        self.file_manager = FileManager("orders.txt")  # ❌ dependencia hardcodeada

    def process(self, order: str) -> None:
        self.file_manager.write(order)

# ✅ BAJO ACOPLAMIENTO: OrderProcessor recibe el FileManager (inyección)
class OrderProcessorV2:
    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager  # ✅ dependencia inyectada

    def process(self, order: str) -> None:
        self.file_manager.write(order)

# Ahora es fácil cambiar el gestor de archivos sin tocar OrderProcessorV2
```

#### Celda — Markdown: Cohesión
- **Acción:** Mantener contenido. Mejorar con ejemplo concreto de clase con baja cohesión (hace demasiado) vs. alta cohesión (hace una sola cosa bien).

#### Celda — Code: Ejemplo Cohesión (NUEVO)
```python
# ❌ BAJA COHESIÓN: UserManager hace demasiado
class UserManager:
    def create_user(self, name: str): ...
    def send_email(self, user, msg: str): ...  # ¿por qué gestión de usuarios envía emails?
    def generate_report(self): ...             # ¿y también genera reportes?
    def connect_to_db(self): ...               # ¿y maneja la conexión a BD?

# ✅ ALTA COHESIÓN: cada clase tiene una responsabilidad clara
class UserRepository:
    def create(self, name: str): ...
    def find_by_id(self, user_id: int): ...

class EmailService:
    def send(self, recipient: str, message: str): ...

class ReportGenerator:
    def generate_user_report(self, users: list): ...
```

#### Celda — Markdown: Lo Ideal (imagen cuadrante)
- **Acción:** Mantener imagen. Refrasear el texto para vincular explícitamente con los principios SOLID que vienen a continuación.

---

### MÓDULO 3 — Código Limpio y Principios SOLID <a name="solid">

#### Celda — Markdown: Código Limpio
- **Acción:** Mantener los 4 principios. Agregar referencia explícita a Robert C. Martin y un ejemplo breve de cada principio en código.

#### Celda — Markdown: Principios SOLID
- **Acción:** El contenido es sólido (pun intended). Dividir en subsecciones H3 por principio.
- Agregar anclaje `<a name="solid">` al H2.

#### Celda — Code: SRP — Single Responsibility (NUEVO)
```python
# ❌ Viola SRP: la clase hace demasiado
class Invoice:
    def calculate_total(self): ...
    def print_invoice(self): ...    # responsabilidad de presentación
    def save_to_db(self): ...       # responsabilidad de persistencia

# ✅ Respeta SRP: cada clase tiene una razón para cambiar
class Invoice:
    def calculate_total(self) -> float: ...

class InvoicePrinter:
    def print(self, invoice: Invoice) -> None: ...

class InvoiceRepository:
    def save(self, invoice: Invoice) -> None: ...
```

#### Celda — Code: OCP y LSP (NUEVO)
```python
# ❌ Viola OCP: hay que modificar la clase para agregar un nuevo formato
class ReportExporter:
    def export(self, report, format: str):
        if format == "pdf":
            ...
        elif format == "csv":
            ...
        # Cada nuevo formato requiere modificar esta clase

# ✅ Respeta OCP: se extiende sin modificar
from abc import ABC, abstractmethod

class ReportExporter(ABC):
    @abstractmethod
    def export(self, report) -> None: ...

class PDFExporter(ReportExporter):
    def export(self, report) -> None: ...

class CSVExporter(ReportExporter):
    def export(self, report) -> None: ...
```

#### Celda — Code: DIP (NUEVO)
```python
# ❌ Viola DIP: depende de implementación concreta
class Notification:
    def __init__(self):
        self.email = EmailSender()  # dependencia de bajo nivel

    def send(self, msg: str):
        self.email.send(msg)

# ✅ Respeta DIP: depende de abstracción
class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class Notification:
    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender  # inyección de dependencia

    def send(self, message: str) -> None:
        self.sender.send(message)
```

---

### MÓDULO 4 — El Paradigma Orientado a Objetos <a name="poo">

#### Celda — Markdown: ¿Qué es POO?
- **Acción:** Refrasear la sección actual. Es densa. Dividirla en:
  - Definición concisa (2-3 oraciones con cita a Booch)
  - Contraste directo con paradigma estructural (tabla comparativa)
  - El "cambio de mentalidad": pensar en sustantivos (objetos) vs. verbos (funciones)

**Tabla propuesta:**

| | Paradigma Estructurado | Paradigma OOP |
|---|---|---|
| Unidad fundamental | Función/Procedimiento | Objeto |
| Dato y comportamiento | Separados | Unidos en la misma entidad |
| Reuso | Copy-paste, funciones genéricas | Herencia, Composición |
| Complejidad | Crece con el tamaño del programa | Se gestiona con encapsulación |

#### Celda — Markdown: AOO y DOO
- **Acción:** Mantener secciones, simplificar. El ejemplo del videojuego es bueno, expandirlo con un diagrama ASCII simple de clases y relaciones.

#### Celda — Code: Ejemplo Contrastante (NUEVO — cierre del módulo anterior de inventario)
```python
# ✅ VERSIÓN OOP del inventario que antes era procedural
class Producto:
    """Representa un producto en el inventario."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    @property
    def nombre(self) -> str:
        return self._nombre

    def __repr__(self) -> str:
        return f"Producto({self._nombre!r}, ${self._precio}, stock={self._stock})"


class Inventario:
    """Gestiona una colección de productos."""

    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def agregar(self, producto: Producto) -> None:
        self._productos.append(producto)

    def buscar(self, nombre: str) -> Producto | None:
        return next((p for p in self._productos if p.nombre == nombre), None)

    def mostrar(self) -> None:
        for producto in self._productos:
            print(producto)
```

---

### MÓDULO 5 — Los Cuatro Pilares del Modelo de Objetos <a name="pilares">

#### Celda — Markdown: Introducción a los Cuatro Pilares
- **Acción:** Crear celda nueva de introducción que liste los 4 elementos con una oración cada uno antes de desarrollarlos.

#### Celda — Markdown + Imagen: Abstracción
- **Acción:** Mantener imagen. Mejorar redacción. Agregar ejemplo cotidiano concreto (no de código): "Un auto es una abstracción: usás el volante sin saber cómo funciona el motor."

#### Celda — Code: Abstracción con ABC (NUEVO)
```python
from abc import ABC, abstractmethod

class Figura(ABC):
    """Abstracción de una figura geométrica."""

    @abstractmethod
    def area(self) -> float:
        """Calcula el área de la figura."""
        ...

    @abstractmethod
    def perimetro(self) -> float:
        """Calcula el perímetro de la figura."""
        ...

    def describir(self) -> str:
        return f"Área: {self.area():.2f}, Perímetro: {self.perimetro():.2f}"


class Circulo(Figura):
    def __init__(self, radio: float) -> None:
        self.radio = radio

    def area(self) -> float:
        import math
        return math.pi * self.radio ** 2

    def perimetro(self) -> float:
        import math
        return 2 * math.pi * self.radio


class Rectangulo(Figura):
    def __init__(self, ancho: float, alto: float) -> None:
        self.ancho = ancho
        self.alto = alto

    def area(self) -> float:
        return self.ancho * self.alto

    def perimetro(self) -> float:
        return 2 * (self.ancho + self.alto)

# Polimorfismo: misma interfaz, distinto comportamiento
figuras: list[Figura] = [Circulo(5), Rectangulo(4, 6)]
for figura in figuras:
    print(figura.describir())
```

#### Celda — Markdown: Encapsulamiento
- **Acción:** Refrasear. Actualmente muy teórico. Agregar párrafo sobre convenciones Python: `_privado` vs `__muy_privado` vs público.

#### Celda — Code: Encapsulamiento con @property (NUEVO)
```python
class CuentaBancaria:
    """Ejemplo de encapsulamiento: el saldo no es accesible directamente."""

    def __init__(self, titular: str, saldo_inicial: float = 0) -> None:
        self._titular = titular
        self.__saldo = saldo_inicial  # __ = name mangling, muy privado

    @property
    def saldo(self) -> float:
        """El saldo es de solo lectura desde afuera."""
        return self.__saldo

    @property
    def titular(self) -> str:
        return self._titular

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.__saldo += monto

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente")
        self.__saldo -= monto

    def __repr__(self) -> str:
        return f"CuentaBancaria({self._titular!r}, saldo=${self.__saldo:.2f})"

cuenta = CuentaBancaria("Ana García", 1000)
cuenta.depositar(500)
print(cuenta.saldo)    # ✅ acceso controlado
# cuenta.__saldo = 999999  # ❌ no funciona (name mangling)
```

#### Celda — Markdown: Modularidad
- **Acción:** Mantener contenido, simplificar. Vincular explícitamente con la idea de "módulos de Python" (archivos `.py`) como forma concreta de modularidad.

#### Celda — Markdown: Jerarquía
- **Acción:** Mantener. Enfatizar la distinción "is-a" (herencia) vs "has-a" (composición) con ejemplos concretos del dominio del curso.

---

### MÓDULO 6 — Clases y Objetos en Python <a name="clases-objetos">

> Este es el módulo más nuevo y más necesario del notebook.

#### Celda — Markdown: ¿Qué es una Clase?
- **Acción:** Crear sección nueva con definición formal + analogía (clase = plano de construcción, objeto = edificio).
- Diagrama ASCII mostrando clase → múltiples instancias.

#### Celda — Code: Anatomía de una Clase (NUEVO)
```python
class Persona:
    """
    Ejemplo canónico de una clase en Python.

    Attributes:
        nombre: Nombre completo de la persona.
        edad: Edad en años.
    """

    # Atributo de clase (compartido por todas las instancias)
    especie: str = "Homo sapiens"

    def __init__(self, nombre: str, edad: int) -> None:
        # Atributos de instancia (únicos por objeto)
        self.nombre = nombre
        self.edad = edad

    def saludar(self) -> str:
        """Método de instancia: opera sobre self."""
        return f"Hola, soy {self.nombre} y tengo {self.edad} años."

    @classmethod
    def desde_dict(cls, datos: dict) -> "Persona":
        """Método de clase: factory method alternativo."""
        return cls(datos["nombre"], datos["edad"])

    @staticmethod
    def es_mayor_de_edad(edad: int) -> bool:
        """Método estático: utilidad sin acceso a self ni cls."""
        return edad >= 18

    def __repr__(self) -> str:
        return f"Persona({self.nombre!r}, {self.edad})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Persona):
            return NotImplemented
        return self.nombre == other.nombre and self.edad == other.edad


# Instanciación
p1 = Persona("Carlos", 30)
p2 = Persona.desde_dict({"nombre": "Ana", "edad": 25})

print(p1.saludar())
print(Persona.es_mayor_de_edad(17))
print(p1.especie)  # atributo de clase
```

#### Celda — Markdown: Diferencia entre Clase y Objeto
- **Acción:** Crear sección nueva dedicada. Usar la analogía de "molde de galletas" (clase) vs. "galleta" (objeto).

---

### MÓDULO 7 — Atributos y Métodos <a name="atributos-metodos">

#### Celda — Markdown: Tipos de Atributos
- **Acción:** Crear sección nueva. Clasificar: atributos de instancia, de clase, y cómo Python los resuelve (MRO simplificado).

#### Celda — Code: Atributos de Clase vs. Instancia (NUEVO)
```python
class Contador:
    """Demuestra la diferencia entre atributos de clase e instancia."""

    total_instancias: int = 0  # atributo de clase

    def __init__(self, nombre: str) -> None:
        Contador.total_instancias += 1
        self.nombre = nombre
        self.id = Contador.total_instancias  # instancia recibe el valor actual

    def __repr__(self) -> str:
        return f"Contador(id={self.id}, nombre={self.nombre!r})"

c1 = Contador("primero")
c2 = Contador("segundo")
c3 = Contador("tercero")

print(Contador.total_instancias)  # 3 — atributo de clase
print(c1.id, c2.id, c3.id)       # 1 2 3 — atributos de instancia únicos
```

#### Celda — Markdown: Tipos de Métodos
- **Acción:** Crear sección nueva. Tabla comparativa clara:

| Tipo | Decorador | Primer parámetro | Accede a |
|---|---|---|---|
| Instancia | (ninguno) | `self` | atributos de instancia y clase |
| Clase | `@classmethod` | `cls` | atributos de clase, puede crear instancias |
| Estático | `@staticmethod` | (ninguno) | nada (utilidad pura) |
| Mágico/Dunder | (ninguno) | `self` | atributos + protocolo Python |

---

### MÓDULO 8 — Métodos Especiales (Dunder) <a name="dunder">

#### Celda — Markdown: Métodos Mágicos
- **Acción:** Crear sección propia. Actualmente están mencionados en la "Guía de Supervivencia" sin profundidad.

#### Celda — Code: Dunder Methods Esenciales (NUEVO)
```python
class Vector:
    """Clase que implementa los principales métodos dunder."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Representación técnica (para desarrolladores)."""
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        """Representación legible (para usuarios)."""
        return f"({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        """Permite usar el operador +."""
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        """Permite usar == entre vectores."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __len__(self) -> int:
        """Permite usar len() sobre el vector (magnitud entera)."""
        return int((self.x**2 + self.y**2) ** 0.5)

    def __bool__(self) -> bool:
        """Un vector es falsy si es el vector cero."""
        return self.x != 0 or self.y != 0

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)         # usa __add__
print(v1 == v2)        # usa __eq__
print(len(v2))         # usa __len__
print(bool(Vector(0, 0)))  # False — usa __bool__
```

---

### MÓDULO 9 — Herencia y Composición <a name="herencia">

#### Celda — Markdown: Herencia
- **Acción:** Expandir la sección actual de "Jerarquía". Incluir:
  - Cuándo usar herencia ("is-a")
  - Uso correcto de `super()`
  - Advertencia sobre abuso de herencia

#### Celda — Code: Herencia con super() (NUEVO)
```python
class Animal:
    """Clase base para animales."""

    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = nombre
        self.edad = edad

    def describir(self) -> str:
        return f"{self.nombre} ({self.edad} años)"

    def hablar(self) -> str:
        raise NotImplementedError("Las subclases deben implementar hablar()")


class Perro(Animal):
    def __init__(self, nombre: str, edad: int, raza: str) -> None:
        super().__init__(nombre, edad)  # ✅ correcto uso de super()
        self.raza = raza

    def hablar(self) -> str:
        return "¡Guau!"

    def describir(self) -> str:
        return f"{super().describir()} — Raza: {self.raza}"


class Gato(Animal):
    def hablar(self) -> str:
        return "¡Miau!"


# Polimorfismo
animales: list[Animal] = [Perro("Rex", 3, "Labrador"), Gato("Luna", 5)]
for animal in animales:
    print(f"{animal.describir()}: {animal.hablar()}")
```

#### Celda — Markdown: Composición sobre Herencia
- **Acción:** Crear sección nueva. Explicar el principio con ejemplo donde herencia es incorrecta y composición es la solución.

#### Celda — Code: Composición (NUEVO)
```python
# ❌ Herencia incorrecta: un Auto no "es un" Motor
class Motor:
    def encender(self) -> str:
        return "Motor encendido"

class AutoMal(Motor):  # ❌ un Auto no "es un" Motor
    def acelerar(self) -> str:
        return "Acelerando"

# ✅ Composición: un Auto "tiene un" Motor
class Auto:
    def __init__(self, marca: str) -> None:
        self.marca = marca
        self._motor = Motor()  # ✅ composición

    def encender(self) -> str:
        return f"{self.marca}: {self._motor.encender()}"

    def acelerar(self) -> str:
        return f"{self.marca}: Acelerando"

mi_auto = Auto("Toyota")
print(mi_auto.encender())
```

---

### MÓDULO 10 — Excepciones <a name="excepciones">

> **Sección completamente nueva — no existe en el notebook actual.**

#### Celda — Markdown: Manejo de Excepciones en OOP
- Qué son las excepciones y por qué son parte del diseño OOP
- Cuándo crear excepciones propias vs. usar las built-in
- Jerarquía de excepciones en Python

#### Celda — Code: Excepciones Built-in (NUEVO)
```python
class Producto:
    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        if precio < 0:
            raise ValueError(f"El precio no puede ser negativo: {precio}")
        if stock < 0:
            raise ValueError(f"El stock no puede ser negativo: {stock}")
        self.nombre = nombre
        self._precio = precio
        self._stock = stock

    def vender(self, cantidad: int) -> float:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self._stock:
            raise ValueError(f"Stock insuficiente: hay {self._stock}, pediste {cantidad}")
        self._stock -= cantidad
        return cantidad * self._precio

# Manejo con try/except
try:
    producto = Producto("Laptop", 1500, 10)
    total = producto.vender(15)
except ValueError as e:
    print(f"Error de negocio: {e}")
```

#### Celda — Code: Excepciones Personalizadas (NUEVO)
```python
# Jerarquía de excepciones propias del dominio
class InventarioError(Exception):
    """Excepción base para errores del módulo de inventario."""
    pass

class StockInsuficienteError(InventarioError):
    """Se lanza cuando no hay suficiente stock para completar una venta."""

    def __init__(self, producto: str, disponible: int, solicitado: int) -> None:
        self.producto = producto
        self.disponible = disponible
        self.solicitado = solicitado
        super().__init__(
            f"Stock insuficiente para '{producto}': "
            f"disponible={disponible}, solicitado={solicitado}"
        )

class ProductoNoEncontradoError(InventarioError):
    """Se lanza cuando se busca un producto que no existe."""
    pass

# Uso
try:
    raise StockInsuficienteError("Laptop", disponible=2, solicitado=5)
except StockInsuficienteError as e:
    print(f"No se pudo completar la venta: {e}")
    print(f"Podemos ofrecerte solo {e.disponible} unidades.")
except InventarioError as e:
    print(f"Error de inventario genérico: {e}")
```

---

### MÓDULO 11 — Testing de Clases <a name="testing">

> **Sección completamente nueva — no existe en el notebook actual.**

#### Celda — Markdown: ¿Por qué testear clases?
- La importancia del testing en OOP: si cambiás la implementación interna, los tests garantizan que el contrato externo no cambió.
- Introducción a `pytest` (instalar en Colab con `!pip install pytest`).
- Qué testear: comportamiento observable, no implementación interna.
- Estilo pytest: funciones sueltas con prefijo `test_`, sin necesidad de clases.

#### Celda — Code: Instalación de pytest en Colab (NUEVO)
```python
!pip install pytest ipytest --quiet
import ipytest
ipytest.autoconfig()
```

#### Celda — Code: pytest básico (NUEVO)
```python
class CuentaBancaria:
    def __init__(self, saldo_inicial: float = 0) -> None:
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto


# ── Tests con pytest ──────────────────────────────────────────────────────────

def test_saldo_inicial() -> None:
    cuenta = CuentaBancaria(1000)
    assert cuenta.saldo == 1000


def test_depositar_incrementa_saldo() -> None:
    cuenta = CuentaBancaria(1000)
    cuenta.depositar(500)
    assert cuenta.saldo == 1500


def test_retirar_reduce_saldo() -> None:
    cuenta = CuentaBancaria(1000)
    cuenta.retirar(300)
    assert cuenta.saldo == 700


def test_depositar_monto_negativo_lanza_error() -> None:
    cuenta = CuentaBancaria(1000)
    with pytest.raises(ValueError):
        cuenta.depositar(-100)


def test_retirar_mas_de_saldo_lanza_error() -> None:
    cuenta = CuentaBancaria(1000)
    with pytest.raises(ValueError):
        cuenta.retirar(2000)


import pytest
ipytest.run()
```

#### Celda — Code: Testing con fixture y casos de borde (NUEVO)
```python
import pytest

# fixture: reemplaza al setUp de unittest
@pytest.fixture
def cuenta_con_saldo() -> CuentaBancaria:
    """Cuenta con saldo inicial de 500 para los tests."""
    return CuentaBancaria(500)


def test_depositar_cero_lanza_error() -> None:
    cuenta = CuentaBancaria()
    with pytest.raises(ValueError):
        cuenta.depositar(0)


def test_retirar_exactamente_el_saldo(cuenta_con_saldo: CuentaBancaria) -> None:
    """Verificar que se puede retirar exactamente lo disponible."""
    cuenta_con_saldo.retirar(500)
    assert cuenta_con_saldo.saldo == 0


def test_multiples_operaciones() -> None:
    """Test de integración: secuencia de operaciones."""
    cuenta = CuentaBancaria(100)
    cuenta.depositar(200)
    cuenta.retirar(50)
    cuenta.depositar(25)
    assert cuenta.saldo == 275


ipytest.run()
```

---

### MÓDULO 12 — Fuentes <a name="fuentes">

#### Celda — Markdown: Fuentes
- **Acción:** Mantener fuentes actuales. Organizar con formato de lista numerada con formato uniforme (Autor, Título, Año).
- Agregar enlaces directos a las URLs referenciadas en el texto.

---

## Consolidación: Eliminar Redundancias

### Celdas a Eliminar o Fusionar

| Celda actual | Problema | Acción |
|---|---|---|
| "Guía de Supervivencia" | Solapan contenido con módulos 7, 8 y 9 | Eliminar — el contenido se distribuye en los módulos correspondientes |
| "Principios y Buenas Prácticas" | Solapan con módulos 2, 3 y 6 | Eliminar — consolidar en conclusión o checklist final |
| Celda de code vacía (cell 1) | Innecesaria | Eliminar |
| Celda de code vacía (cell 12) | Innecesaria | Eliminar |

### Celda Nueva a Agregar: Checklist Final

#### Celda — Markdown: Checklist de Calidad para Entregas
```markdown
## Checklist: Antes de entregar tu código

- [ ] Cada clase tiene un docstring que explica su responsabilidad
- [ ] Cada método público tiene type hints y docstring
- [ ] Los atributos privados usan `_` o `__` según corresponda
- [ ] No hay lógica de negocio repetida en más de un lugar (DRY)
- [ ] Cada clase tiene tests que cubren el comportamiento normal y los casos de error
- [ ] Las excepciones son descriptivas y tienen mensajes claros
- [ ] Se usa composición en lugar de herencia cuando el vínculo no es "es-un"
```

---

## Resumen de Cambios

| Tipo | Cantidad |
|---|---|
| Módulos / secciones nuevas | 5 (Clases y Objetos, Métodos, Dunder, Excepciones, Testing) |
| Snippets de código nuevos | ~18 |
| Snippets a refactorizar | 2 (acoplamiento, factorial) |
| Celdas a eliminar | 4 (2 vacías + 2 secciones redundantes) |
| Secciones a refrasear | 4 (POO, Abstracción, Encapsulamiento, Jerarquía) |
| Índice | 1 (nuevo) |

---

## Orden de Trabajo Sugerido

1. **Primero:** Crear el índice (rápido, alto impacto visual)
2. **Segundo:** Agregar los módulos faltantes (Testing y Excepciones) — son completamente nuevos
3. **Tercero:** Agregar snippets de código a secciones que ya existen (SOLID, Pilares)
4. **Cuarto:** Refactorizar snippets existentes (acoplamiento)
5. **Quinto:** Revisar y mejorar redacción de secciones teóricas
6. **Sexto:** Eliminar celdas redundantes y reorganizar el orden final
