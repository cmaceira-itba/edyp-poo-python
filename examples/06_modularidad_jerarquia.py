"""
Capítulos: Modularidad y Jerarquía (Elementos del Modelo de Objetos)
----------------------------------------------------------------------
Modularidad: clases cohesivas con dependencias mínimas (en un sistema real
viven en archivos separados).

Jerarquía: dos tipos fundamentales:
  - "es-un"   → herencia
  - "tiene-un" → composición (preferida cuando sea posible)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# MODULARIDAD
# (En un proyecto real: productos.py / inventario.py / reporte.py)
# ═══════════════════════════════════════════════════════════════════════════════

# ── módulo: productos.py ──────────────────────────────────────────────────────

class Producto:
    """Encapsula datos y reglas de negocio de un producto.

    Attributes:
        nombre: Nombre del producto.
        precio: Precio unitario (solo lectura).
    """

    def __init__(self, nombre: str, precio: float, stock: int = 0) -> None:
        if precio < 0:
            raise ValueError(f"El precio no puede ser negativo: {precio}")
        if stock < 0:
            raise ValueError(f"El stock no puede ser negativo: {stock}")
        self.nombre = nombre
        self._precio = precio
        self._stock = stock

    @property
    def precio(self) -> float:
        return self._precio

    @property
    def stock(self) -> int:
        return self._stock

    def reponer(self, cantidad: int) -> None:
        """Aumenta el stock."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser positiva")
        self._stock += cantidad

    def vender(self, cantidad: int) -> float:
        """Descuenta stock y retorna el total de la venta."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self._stock:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}': "
                f"disponible={self._stock}, solicitado={cantidad}"
            )
        self._stock -= cantidad
        return cantidad * self._precio

    def __repr__(self) -> str:
        return f"Producto({self.nombre!r}, ${self._precio:.2f}, stock={self._stock})"


# ── módulo: inventario.py ─────────────────────────────────────────────────────

class Inventario:
    """Gestiona una colección de productos. Solo depende de Producto."""

    def __init__(self) -> None:
        self._items: dict[str, Producto] = {}

    def agregar(self, producto: Producto) -> None:
        """Agrega o reemplaza un producto en el inventario."""
        self._items[producto.nombre] = producto

    def buscar(self, nombre: str) -> Producto | None:
        """Retorna el producto o None si no existe."""
        return self._items.get(nombre)

    def listar(self) -> list[Producto]:
        return list(self._items.values())

    def total_productos(self) -> int:
        return len(self._items)

    def valor_total_stock(self) -> float:
        return sum(p.precio * p.stock for p in self._items.values())


# ── módulo: reporte.py ────────────────────────────────────────────────────────

class ReporteInventario:
    """Genera reportes. Cohesivo: solo sabe de reportes."""

    def generar(self, inventario: Inventario) -> str:
        lineas = [
            "=" * 40,
            "   REPORTE DE INVENTARIO",
            "=" * 40,
            f"  Productos:       {inventario.total_productos()}",
            f"  Valor total:     ${inventario.valor_total_stock():.2f}",
            "-" * 40,
        ]
        for producto in inventario.listar():
            lineas.append(
                f"  {producto.nombre:<15} "
                f"${producto.precio:>8.2f}  "
                f"stock: {producto.stock}"
            )
        lineas.append("=" * 40)
        return "\n".join(lineas)


# ═══════════════════════════════════════════════════════════════════════════════
# JERARQUÍA
# ═══════════════════════════════════════════════════════════════════════════════

# ── Jerarquía "es-un" (herencia) ──────────────────────────────────────────────

class Vehiculo:
    """Abstracción base para todo vehículo."""

    def __init__(self, marca: str, modelo: str, año: int) -> None:
        self.marca = marca
        self.modelo = modelo
        self.año = año

    def describir(self) -> str:
        return f"{self.marca} {self.modelo} ({self.año})"


class Moto(Vehiculo):
    """Una Moto ES UN Vehículo. ✅ herencia correcta."""

    def __init__(self, marca: str, modelo: str, año: int, cilindrada: int) -> None:
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada

    def describir(self) -> str:
        return f"Moto: {super().describir()} — {self.cilindrada}cc"


class Camion(Vehiculo):
    """Un Camión ES UN Vehículo."""

    def __init__(self, marca: str, modelo: str, año: int, toneladas: float) -> None:
        super().__init__(marca, modelo, año)
        self.toneladas = toneladas

    def describir(self) -> str:
        return f"Camión: {super().describir()} — {self.toneladas}t"


# ── Jerarquía "tiene-un" (composición) ───────────────────────────────────────

class Motor:
    """Componente reutilizable e independiente."""

    def __init__(self, cilindros: int, hp: int) -> None:
        self.cilindros = cilindros
        self.hp = hp

    def encender(self) -> str:
        return f"Motor {self.cilindros}cil/{self.hp}hp encendido"

    def __repr__(self) -> str:
        return f"Motor({self.cilindros}cil, {self.hp}hp)"


class SistemaGPS:
    """Otro componente reutilizable."""

    def __init__(self, proveedor: str) -> None:
        self.proveedor = proveedor

    def ubicacion(self) -> str:
        return f"[{self.proveedor}] GPS activo"


class Auto:
    """Un Auto TIENE UN Motor y puede tener un GPS.
    No hereda de Motor — no es un Motor.
    """

    def __init__(self, marca: str, cilindros: int, hp: int) -> None:
        self.marca = marca
        self._motor = Motor(cilindros, hp)   # composición
        self._gps: SistemaGPS | None = None

    def instalar_gps(self, gps: SistemaGPS) -> None:
        self._gps = gps

    def arrancar(self) -> str:
        return f"{self.marca}: {self._motor.encender()}"

    def navegar(self) -> str:
        if self._gps is None:
            return f"{self.marca}: sin GPS instalado"
        return f"{self.marca}: {self._gps.ubicacion()}"

    def __repr__(self) -> str:
        return f"Auto({self.marca!r}, {self._motor})"


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Modularidad: Inventario ===")
    inv = Inventario()
    inv.agregar(Producto("Laptop", 1500.0, 10))
    inv.agregar(Producto("Monitor", 400.0, 25))
    inv.agregar(Producto("Teclado", 80.0, 50))
    inv.agregar(Producto("Mouse", 35.0, 60))
    print(ReporteInventario().generar(inv))

    print("\n  Venta de 3 laptops:")
    laptop = inv.buscar("Laptop")
    if laptop:
        total = laptop.vender(3)
        print(f"  Total cobrado: ${total:.2f}")
    print(ReporteInventario().generar(inv))

    print("\n=== Jerarquía 'es-un' (herencia) ===")
    vehiculos: list[Vehiculo] = [
        Moto("Honda", "CBR600", 2022, 600),
        Camion("Scania", "R500", 2020, 25.0),
        Vehiculo("Genérico", "X", 2023),
    ]
    for v in vehiculos:
        print(f"  {v.describir()}")

    print("\n=== Jerarquía 'tiene-un' (composición) ===")
    auto = Auto("Toyota", 4, 150)
    print(f"  {auto.arrancar()}")
    print(f"  {auto.navegar()}")

    auto.instalar_gps(SistemaGPS("Waze"))
    print(f"  {auto.navegar()}")
    print(f"  {auto}")
