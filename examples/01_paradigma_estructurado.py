"""
Capítulo: El Paradigma Estructurado
------------------------------------
Ejemplos de programación estructurada: funciones, secuencia, selección e iteración.
Contraste entre código limpio y código espagueti.
"""


# ── Ejemplo 1: Función estructurada limpia ───────────────────────────────────

def factorial(n: int) -> int:
    """Calcula el factorial de un entero no negativo.

    Args:
        n: Número entero no negativo.

    Returns:
        El factorial de n.

    Raises:
        ValueError: si n es negativo.
        TypeError: si n no es un entero.
    """
    if not isinstance(n, int):
        raise TypeError(f"Se esperaba un entero, se recibió: {type(n).__name__}")
    if n < 0:
        raise ValueError(f"El factorial no está definido para negativos: {n}")
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado


# ── Ejemplo 2: Código espagueti vs. código limpio ────────────────────────────

# ❌ Espagueti: flags anidados, difícil de leer
def procesar_pedido_espagueti(usuario, items, descuento):
    ok = False
    total = 0
    if usuario:
        if len(items) > 0:
            for item in items:
                if item["stock"] > 0:
                    total += item["precio"]
                    ok = True
                else:
                    ok = False
                    break
            if ok:
                if descuento > 0:
                    total = total - (total * descuento / 100)
    return total if ok else -1


# ✅ Limpio: early returns, responsabilidades claras
def _validar_items(items: list[dict]) -> bool:
    """Verifica que todos los items tengan stock disponible."""
    return all(item["stock"] > 0 for item in items)


def _calcular_total(items: list[dict], descuento: float) -> float:
    """Suma precios y aplica descuento porcentual."""
    total = sum(item["precio"] for item in items)
    if descuento > 0:
        total *= 1 - descuento / 100
    return total


def procesar_pedido(usuario: str, items: list[dict], descuento: float) -> float:
    """Procesa un pedido y retorna el total, o -1 si hay algún error.

    Args:
        usuario: Nombre del usuario que realiza el pedido.
        items: Lista de dicts con claves 'stock' y 'precio'.
        descuento: Porcentaje de descuento (0-100).

    Returns:
        Total del pedido, o -1 si el pedido no es válido.
    """
    if not usuario:
        return -1
    if not items:
        return -1
    if not _validar_items(items):
        return -1
    return _calcular_total(items, descuento)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Factorial ===")
    for n in [0, 1, 5, 10]:
        print(f"  factorial({n}) = {factorial(n)}")

    print("\n=== Factorial con error ===")
    try:
        factorial(-3)
    except ValueError as e:
        print(f"  ValueError: {e}")
    try:
        factorial(3.5)
    except TypeError as e:
        print(f"  TypeError: {e}")

    print("\n=== Procesamiento de pedidos ===")
    items_ok = [{"stock": 2, "precio": 100}, {"stock": 5, "precio": 200}]
    items_sin_stock = [{"stock": 0, "precio": 100}, {"stock": 5, "precio": 200}]

    print(f"  Pedido válido (10% desc): ${procesar_pedido('Ana', items_ok, 10):.2f}")
    print(f"  Pedido sin stock:         {procesar_pedido('Ana', items_sin_stock, 0)}")
    print(f"  Pedido sin usuario:       {procesar_pedido('', items_ok, 0)}")
    print(f"  Pedido sin items:         {procesar_pedido('Ana', [], 0)}")
