# Los Cuatro Elementos del Modelo

Grady Booch identificó cuatro elementos que todo modelo orientado a objetos bien formado debe contemplar. No son características opcionales ni capas que se agregan al final: son los pilares sobre los que se construye el diseño. Entender qué es cada uno —y en qué se diferencia de los demás— es el primer paso para tomar decisiones de diseño fundamentadas.

Los cuatro elementos son:

1. **Abstracción** — qué características esenciales expone un objeto
2. **Encapsulamiento** — cómo se protege y controla el estado interno
3. **Modularidad** — cómo se organiza el sistema en unidades cohesivas e independientes
4. **Jerarquía** — cómo se relacionan y ordenan las abstracciones entre sí

## Abstracción

La abstracción consiste en identificar las características esenciales de un objeto e ignorar los detalles irrelevantes para el contexto. Un objeto expone una **interfaz** — lo que puede hacer — y oculta su **implementación** — cómo lo hace. Quien usa el objeto no necesita saber nada de sus entrañas.

En Python, la abstracción formal se implementa con el módulo `abc`. Una clase abstracta define el *contrato* que todas sus subclases deben cumplir, sin especificar cómo lo cumplen.

> Ver en detalle: [Abstracción](../conceptos/abstraccion.md)

## Encapsulamiento

El encapsulamiento protege el estado interno de un objeto y controla cómo se accede o modifica desde afuera. La idea central es que cada objeto es el único responsable de mantener su propia consistencia: nadie externo debería poder poner un objeto en un estado inválido.

Abstracción y encapsulamiento son complementarios pero distintos: la abstracción define *qué* puede hacer un objeto; el encapsulamiento protege *cómo* lo hace.

> Ver en detalle: [Encapsulamiento](../conceptos/encapsulamiento.md)

## Modularidad

Todo diseño orientado a objetos enfrenta una tensión inherente: el deseo de encapsular abstracciones versus la necesidad de que ciertas abstracciones sean visibles para otros módulos. La modularidad resuelve esa tensión al descomponer el sistema en un conjunto de módulos **cohesivos** y **débilmente acoplados**.

En Python, cada archivo `.py` es naturalmente un módulo. Dado que abstracción, encapsulación y modularidad son principios sinérgicos, la modularidad opera como el contenedor que los organiza y delimita.

A continuación, el ejemplo muestra tres clases que en un sistema real vivirían en archivos separados (`productos.py`, `inventario.py`, `reporte.py`). Cada módulo tiene una única responsabilidad y sus dependencias son mínimas:

```python
# --- módulo: productos.py ---
class Producto:
    """Encapsula los datos y reglas de negocio de un producto."""

    def __init__(self, nombre: str, precio: float) -> None:
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.nombre = nombre
        self._precio = precio

    @property
    def precio(self) -> float:
        return self._precio

    def __repr__(self) -> str:
        return f"Producto({self.nombre!r}, ${self._precio:.2f})"


# --- módulo: inventario.py ---
class Inventario:
    """Gestiona una colección de productos. Solo depende de Producto."""

    def __init__(self) -> None:
        self._items: list[Producto] = []

    def agregar(self, producto: Producto) -> None:
        self._items.append(producto)

    def buscar(self, nombre: str) -> Producto | None:
        return next((p for p in self._items if p.nombre == nombre), None)

    def total_stock(self) -> int:
        return len(self._items)


# --- módulo: reporte.py ---
class ReporteInventario:
    """Genera reportes. Cohesivo: solo sabe de reportes, nada más."""

    def generar(self, inventario: Inventario) -> str:
        lineas = [
            "=== Reporte de Inventario ===",
            f"Total de productos: {inventario.total_stock()}",
        ]
        return "\n".join(lineas)


# Uso
inv = Inventario()
inv.agregar(Producto("Laptop", 1500))
inv.agregar(Producto("Monitor", 400))

reporte = ReporteInventario()
print(reporte.generar(inv))
```

### Cohesión y acoplamiento

Dos métricas guían el diseño modular:

- **Cohesión** (alta es buena): un módulo es cohesivo cuando todas sus partes trabajan juntas hacia un único propósito. `ReporteInventario` solo genera reportes — no agrega productos, no valida precios. Eso es alta cohesión.
- **Acoplamiento** (bajo es bueno): un módulo tiene bajo acoplamiento cuando depende de pocos módulos externos y solo de sus interfaces públicas. Si `ReporteInventario` solo necesita saber que `Inventario` tiene `total_stock()`, no importa cómo lo implementa internamente.

> En la práctica, cuando un cambio en una parte del sistema irradia modificaciones hacia muchos otros archivos, es una señal clara de alto acoplamiento. La solución casi siempre implica identificar qué responsabilidades están mal asignadas y redistribuirlas en módulos más cohesivos.

## Jerarquía

Cualquier sistema real involucra decenas de abstracciones que necesitan relacionarse entre sí. La jerarquía organiza esas relaciones de manera que el sistema siga siendo comprensible. Las dos formas fundamentales son:

- **Jerarquía "es-un"** (herencia): una subclase *es un* tipo específico de su clase padre. `Auto` es un `Vehiculo`.
- **Jerarquía "tiene-un"** (composición): un objeto *contiene* o *usa* a otro. `Auto` tiene un `Motor`.

Elegir entre estas dos es una de las decisiones de diseño más frecuentes y más importantes. La regla práctica: si podés decir con naturalidad que A *es un* B en todos los contextos, usá herencia. Si la relación es que A *tiene un* B o A *usa un* B, usá composición. En la práctica, el abuso de herencia genera jerarquías rígidas y difíciles de cambiar — la composición suele ser la opción más flexible.

> Ver en detalle: [Herencia](../conceptos/herencia.md) · [Composición vs. Herencia](../diseno/composicion_vs_herencia.md)

---
