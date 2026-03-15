"""
Capítulo: Abstracción (Elementos del Modelo de Objetos)
---------------------------------------------------------
Las clases abstractas definen *qué* puede hacer un objeto sin decir *cómo*.
Todas las subclases concretas deben cumplir ese contrato.
"""

import math
from abc import ABC, abstractmethod


# ── Clase abstracta base ──────────────────────────────────────────────────────

class Figura(ABC):
    """Abstracción de una figura geométrica plana.

    Define el contrato: toda figura debe poder calcular su área y perímetro.
    El método `describir` es concreto porque la lógica es igual para todas.
    """

    @abstractmethod
    def area(self) -> float:
        """Retorna el área de la figura en unidades cuadradas."""
        ...

    @abstractmethod
    def perimetro(self) -> float:
        """Retorna el perímetro de la figura."""
        ...

    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre de la figura."""
        ...

    def describir(self) -> str:
        """Descripción legible de la figura (método concreto compartido)."""
        return (
            f"{self.nombre()}: "
            f"área={self.area():.4f}, "
            f"perímetro={self.perimetro():.4f}"
        )

    def es_mas_grande_que(self, otra: "Figura") -> bool:
        """Compara áreas sin importar el tipo concreto de figura."""
        return self.area() > otra.area()


# ── Implementaciones concretas ────────────────────────────────────────────────

class Circulo(Figura):
    """Círculo definido por su radio."""

    def __init__(self, radio: float) -> None:
        if radio <= 0:
            raise ValueError(f"El radio debe ser positivo: {radio}")
        self._radio = radio

    def area(self) -> float:
        return math.pi * self._radio ** 2

    def perimetro(self) -> float:
        return 2 * math.pi * self._radio

    def nombre(self) -> str:
        return f"Círculo(r={self._radio})"


class Rectangulo(Figura):
    """Rectángulo definido por ancho y alto."""

    def __init__(self, ancho: float, alto: float) -> None:
        if ancho <= 0 or alto <= 0:
            raise ValueError(f"Dimensiones deben ser positivas: {ancho=}, {alto=}")
        self._ancho = ancho
        self._alto = alto

    def area(self) -> float:
        return self._ancho * self._alto

    def perimetro(self) -> float:
        return 2 * (self._ancho + self._alto)

    def nombre(self) -> str:
        return f"Rectángulo({self._ancho}x{self._alto})"


class TrianguloEquilatero(Figura):
    """Triángulo equilátero definido por el lado."""

    def __init__(self, lado: float) -> None:
        if lado <= 0:
            raise ValueError(f"El lado debe ser positivo: {lado}")
        self._lado = lado

    def area(self) -> float:
        return (math.sqrt(3) / 4) * self._lado ** 2

    def perimetro(self) -> float:
        return 3 * self._lado

    def nombre(self) -> str:
        return f"TriánguloEquilátero(lado={self._lado})"


# ── Función que trabaja con la abstracción ────────────────────────────────────

def figura_con_mayor_area(figuras: list[Figura]) -> Figura:
    """Retorna la figura con mayor área de la lista.

    Funciona con cualquier subclase de Figura gracias al polimorfismo.
    """
    return max(figuras, key=lambda f: f.area())


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Polimorfismo con Figura ===")
    figuras: list[Figura] = [
        Circulo(5),
        Rectangulo(4, 6),
        TrianguloEquilatero(8),
        Rectangulo(10, 2),
        Circulo(3),
    ]

    for figura in figuras:
        print(f"  {figura.describir()}")

    print("\n=== Figura con mayor área ===")
    ganadora = figura_con_mayor_area(figuras)
    print(f"  {ganadora.nombre()} → área={ganadora.area():.4f}")

    print("\n=== Comparación de figuras ===")
    c = Circulo(5)
    r = Rectangulo(4, 6)
    print(f"  ¿{c.nombre()} es más grande que {r.nombre()}? {c.es_mas_grande_que(r)}")

    print("\n=== Error: instanciar clase abstracta ===")
    try:
        _ = Figura()  # type: ignore
    except TypeError as e:
        print(f"  TypeError: {e}")

    print("\n=== Error: dimensiones inválidas ===")
    try:
        Circulo(-1)
    except ValueError as e:
        print(f"  ValueError: {e}")
