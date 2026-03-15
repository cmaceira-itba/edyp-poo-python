"""
Capítulo: Excepciones
----------------------
Las excepciones son objetos que forman una jerarquía de herencia.
Design by Contract: cada método tiene precondiciones y postcondiciones;
las excepciones comunican cuándo el contrato fue violado.

Temas:
  - Uso de excepciones built-in
  - try / except / else / finally
  - Excepciones personalizadas con atributos propios
  - Jerarquía de excepciones de dominio
"""


# ── Jerarquía de excepciones del dominio ──────────────────────────────────────

class TiendaError(Exception):
    """Excepción base para todos los errores del módulo de tienda."""
    pass


class ProductoNoEncontradoError(TiendaError):
    """Se lanza cuando se busca un producto inexistente."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        super().__init__(f"Producto no encontrado: '{nombre}'")


class StockInsuficienteError(TiendaError):
    """Se lanza cuando no hay suficiente stock para una venta."""

    def __init__(self, producto: str, disponible: int, solicitado: int) -> None:
        self.producto = producto
        self.disponible = disponible
        self.solicitado = solicitado
        super().__init__(
            f"Stock insuficiente para '{producto}': "
            f"disponible={disponible}, solicitado={solicitado}"
        )


class PrecioInvalidoError(TiendaError):
    """Se lanza cuando se intenta asignar un precio inválido."""

    def __init__(self, precio: float) -> None:
        self.precio = precio
        super().__init__(f"El precio debe ser positivo, recibí: {precio}")


# ── Clases del dominio ────────────────────────────────────────────────────────

class Producto:
    """Producto con validaciones en cada operación.

    Attributes:
        nombre: Nombre del producto.
    """

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        if precio <= 0:
            raise PrecioInvalidoError(precio)
        if stock < 0:
            raise ValueError(f"El stock inicial no puede ser negativo: {stock}")
        self.nombre = nombre
        self._precio = precio
        self._stock = stock

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def precio(self) -> float:
        return self._precio

    def vender(self, cantidad: int) -> float:
        """Descuenta stock y retorna el total.

        Raises:
            ValueError: si la cantidad no es positiva.
            StockInsuficienteError: si no hay stock suficiente.
        """
        if cantidad <= 0:
            raise ValueError(f"La cantidad debe ser positiva: {cantidad}")
        if cantidad > self._stock:
            raise StockInsuficienteError(self.nombre, self._stock, cantidad)
        self._stock -= cantidad
        return cantidad * self._precio

    def __repr__(self) -> str:
        return f"Producto({self.nombre!r}, ${self._precio:.2f}, stock={self._stock})"


class Carrito:
    """Carrito de compras que trabaja con un catálogo de productos."""

    def __init__(self, catalogo: dict[str, Producto]) -> None:
        self._catalogo = catalogo
        self._items: dict[str, int] = {}   # nombre → cantidad

    def agregar(self, nombre: str, cantidad: int) -> None:
        """Agrega un producto al carrito.

        Raises:
            ProductoNoEncontradoError: si el producto no está en el catálogo.
            StockInsuficienteError: si no hay stock suficiente.
            ValueError: si la cantidad no es positiva.
        """
        if nombre not in self._catalogo:
            raise ProductoNoEncontradoError(nombre)
        producto = self._catalogo[nombre]
        if cantidad > producto.stock:
            raise StockInsuficienteError(nombre, producto.stock, cantidad)
        if cantidad <= 0:
            raise ValueError(f"Cantidad inválida: {cantidad}")
        self._items[nombre] = self._items.get(nombre, 0) + cantidad

    def total(self) -> float:
        return sum(
            self._catalogo[nombre].precio * cantidad
            for nombre, cantidad in self._items.items()
        )

    def checkout(self) -> float:
        """Procesa la compra: descuenta stock y retorna el total.

        Raises:
            StockInsuficienteError: si algún producto se quedó sin stock
              entre el agregar y el checkout.
        """
        total = 0.0
        for nombre, cantidad in self._items.items():
            total += self._catalogo[nombre].vender(cantidad)
        self._items.clear()
        return total


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Excepciones built-in en constructor ===")
    try:
        Producto("Roto", -10.0, 5)
    except PrecioInvalidoError as e:
        print(f"  PrecioInvalidoError: {e}")
    try:
        Producto("Roto", 10.0, -1)
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n=== try / except / else / finally ===")
    laptop = Producto("Laptop", 1500.0, 3)
    try:
        total = laptop.vender(2)
    except StockInsuficienteError as e:
        print(f"  No se pudo vender: {e}")
    else:
        print(f"  Venta exitosa: ${total:.2f}")   # ✅ se ejecuta
    finally:
        print(f"  Estado actual: {laptop}")        # siempre

    print("\n=== Captura selectiva ===")
    laptop2 = Producto("Monitor", 400.0, 1)
    try:
        laptop2.vender(5)
    except StockInsuficienteError as e:
        print(f"  StockInsuficienteError: {e}")
        print(f"  → Podemos ofrecerte {e.disponible} unidades en su lugar.")
    except TiendaError as e:
        print(f"  Error de tienda (genérico): {e}")

    print("\n=== Carrito de compras ===")
    catalogo = {
        "Laptop": Producto("Laptop", 1500.0, 5),
        "Mouse":  Producto("Mouse", 35.0, 20),
        "Teclado": Producto("Teclado", 80.0, 10),
    }
    carrito = Carrito(catalogo)

    operaciones = [
        ("Laptop", 2),
        ("Mouse", 3),
        ("Tablet", 1),    # no existe → ProductoNoEncontradoError
        ("Laptop", 10),   # sin stock suficiente → StockInsuficienteError
    ]

    for nombre, cantidad in operaciones:
        try:
            carrito.agregar(nombre, cantidad)
            print(f"  ✅ Agregado: {nombre} x{cantidad}")
        except ProductoNoEncontradoError as e:
            print(f"  ❌ Producto no encontrado: {e}")
        except StockInsuficienteError as e:
            print(f"  ❌ Sin stock: {e}  → disponible: {e.disponible}")

    print(f"\n  Total en carrito: ${carrito.total():.2f}")
    total_pagado = carrito.checkout()
    print(f"  Total cobrado:    ${total_pagado:.2f}")
    print(f"  Laptop restante:  {catalogo['Laptop']}")

    print("\n=== Jerarquía: capturar la base captura todo ===")
    productos_a_vender = [
        ("Monitor", 1),   # no está en catálogo
        ("Mouse", 50),    # sin stock
    ]
    for nombre, cant in productos_a_vender:
        try:
            carrito.agregar(nombre, cant)
        except TiendaError as e:
            # Captura tanto ProductoNoEncontradoError como StockInsuficienteError
            print(f"  TiendaError ({type(e).__name__}): {e}")
