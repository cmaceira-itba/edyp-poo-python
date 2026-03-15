"""
Capítulo: Principios SOLID
----------------------------
Demostración de los cinco principios SOLID con ejemplos mínimos y ejecutables.
Cada sección muestra la versión que viola el principio y la versión corregida.
"""

from abc import ABC, abstractmethod


# ── S: Single Responsibility Principle ───────────────────────────────────────

class Factura:
    """Solo conoce la lógica de negocio de una factura (SRP)."""

    def __init__(self, items: list[tuple[str, float, int]]) -> None:
        # items: lista de (descripcion, precio_unitario, cantidad)
        self._items = items

    def calcular_total(self) -> float:
        return sum(precio * cantidad for _, precio, cantidad in self._items)

    def __repr__(self) -> str:
        return f"Factura(total=${self.calcular_total():.2f})"


class FacturaImpresora:
    """Solo sabe cómo presentar una factura por pantalla."""

    def imprimir(self, factura: Factura) -> None:
        print(f"  [Impresora] {factura} → total=${factura.calcular_total():.2f}")


class FacturaRepositorio:
    """Solo sabe cómo persistir facturas (en memoria para el ejemplo)."""

    def __init__(self) -> None:
        self._guardadas: list[Factura] = []

    def guardar(self, factura: Factura) -> None:
        self._guardadas.append(factura)
        print(f"  [Repositorio] Factura guardada. Total almacenadas: {len(self._guardadas)}")


# ── O: Open/Closed Principle ──────────────────────────────────────────────────

class ExportadorReporte(ABC):
    """Abstracción base: abierta a extensión, cerrada a modificación."""

    @abstractmethod
    def exportar(self, datos: list[str]) -> None: ...


class ExportadorPDF(ExportadorReporte):
    def exportar(self, datos: list[str]) -> None:
        print(f"  [PDF] Exportando {len(datos)} filas → reporte.pdf")


class ExportadorCSV(ExportadorReporte):
    def exportar(self, datos: list[str]) -> None:
        print(f"  [CSV] Exportando {len(datos)} filas → reporte.csv")


class ExportadorJSON(ExportadorReporte):
    """Formato nuevo: se agrega sin tocar el código existente."""

    def exportar(self, datos: list[str]) -> None:
        print(f"  [JSON] Exportando {len(datos)} filas → reporte.json")


# ── L: Liskov Substitution Principle ─────────────────────────────────────────

class Animal:
    """Clase base con comportamiento garantizado para todas las subclases."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def respirar(self) -> str:
        return f"{self.nombre} respira"


class AnimalVolador(Animal):
    """Extensión para animales que pueden volar."""

    def volar(self) -> str:
        return f"{self.nombre} vuela"


class Pato(AnimalVolador):
    def volar(self) -> str:
        return f"{self.nombre} vuela con sus alas"

    def graznar(self) -> str:
        return f"{self.nombre}: ¡Cuac!"


class PatoDeHule(Animal):
    """No hereda de AnimalVolador porque no puede volar."""

    def chillar(self) -> str:
        return f"{self.nombre}: ¡Squeak!"


def hacer_respirar(animales: list[Animal]) -> None:
    """Funciona con cualquier subclase de Animal (LSP)."""
    for animal in animales:
        print(f"  {animal.respirar()}")


# ── I: Interface Segregation Principle ───────────────────────────────────────

class Trabajable(ABC):
    @abstractmethod
    def trabajar(self) -> None: ...


class Comedor(ABC):
    @abstractmethod
    def comer(self) -> None: ...


class Dormidor(ABC):
    @abstractmethod
    def dormir(self) -> None: ...


class Humano(Trabajable, Comedor, Dormidor):
    """Implementa todo porque un humano hace las tres cosas."""

    def trabajar(self) -> None:
        print("  Humano trabajando")

    def comer(self) -> None:
        print("  Humano comiendo")

    def dormir(self) -> None:
        print("  Humano durmiendo")


class Robot(Trabajable):
    """Solo implementa lo que tiene sentido para él."""

    def trabajar(self) -> None:
        print("  Robot trabajando (sin comer ni dormir)")


# ── D: Dependency Inversion Principle ────────────────────────────────────────

class MedioDeEnvio(ABC):
    """Abstracción de la que dependen tanto el emisor como los destinatarios."""

    @abstractmethod
    def enviar(self, mensaje: str) -> None: ...


class EnvioEmail(MedioDeEnvio):
    def enviar(self, mensaje: str) -> None:
        print(f"  [Email] {mensaje}")


class EnvioSMS(MedioDeEnvio):
    def enviar(self, mensaje: str) -> None:
        print(f"  [SMS] {mensaje}")


class Notificador:
    """Módulo de alto nivel: depende de la abstracción, no de una implementación."""

    def __init__(self, medio: MedioDeEnvio) -> None:
        self._medio = medio

    def notificar(self, mensaje: str) -> None:
        self._medio.enviar(mensaje)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== S — Single Responsibility ===")
    factura = Factura([("Laptop", 1500.0, 1), ("Mouse", 25.0, 2)])
    FacturaImpresora().imprimir(factura)
    FacturaRepositorio().guardar(factura)

    print("\n=== O — Open/Closed ===")
    datos = ["fila1", "fila2", "fila3"]
    for exportador in [ExportadorPDF(), ExportadorCSV(), ExportadorJSON()]:
        exportador.exportar(datos)

    print("\n=== L — Liskov Substitution ===")
    animales: list[Animal] = [Pato("Donald"), PatoDeHule("Rubber"), Animal("Genérico")]
    hacer_respirar(animales)
    # Solo los que pueden volar
    voladores: list[AnimalVolador] = [Pato("Daffy")]
    for v in voladores:
        print(f"  {v.volar()}")

    print("\n=== I — Interface Segregation ===")
    Humano().trabajar()
    Humano().comer()
    Robot().trabajar()

    print("\n=== D — Dependency Inversion ===")
    for medio in [EnvioEmail(), EnvioSMS()]:
        Notificador(medio).notificar("Pedido confirmado #1234")
