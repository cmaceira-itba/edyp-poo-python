"""
Capítulo: Encapsulamiento (Elementos del Modelo de Objetos)
------------------------------------------------------------
El estado interno de un objeto no debe ser accesible directamente.
El objeto es el único responsable de mantener su propia consistencia.

Convenciones Python:
  sin prefijo  → público
  _guion       → protegido (convención, no se accede desde afuera)
  __doble      → name mangling (Python lo renombra a _Clase__attr)
"""


# ── Ejemplo 1: CuentaBancaria ─────────────────────────────────────────────────

class CuentaBancaria:
    """Cuenta bancaria con saldo protegido mediante encapsulamiento.

    El saldo solo puede modificarse a través de depósitos y retiros,
    garantizando que nunca quede en un estado inválido.

    Attributes:
        titular: Nombre del titular de la cuenta (solo lectura).
    """

    _tasa_impuesto: float = 0.0   # atributo de clase, podría cambiar por política

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        if not titular or not titular.strip():
            raise TypeError("El titular debe ser un string no vacío")
        if saldo_inicial < 0:
            raise ValueError(f"El saldo inicial no puede ser negativo: {saldo_inicial}")
        self._titular = titular
        self.__saldo = saldo_inicial          # name mangling: _CuentaBancaria__saldo
        self.__historial: list[str] = []

    @property
    def saldo(self) -> float:
        """El saldo es de solo lectura desde afuera."""
        return self.__saldo

    @property
    def titular(self) -> str:
        return self._titular

    @property
    def historial(self) -> list[str]:
        """Copia del historial (no exponemos la lista interna)."""
        return list(self.__historial)

    def depositar(self, monto: float) -> None:
        """Incrementa el saldo.

        Args:
            monto: Monto a depositar. Debe ser positivo.

        Raises:
            ValueError: si el monto no es positivo.
        """
        if monto <= 0:
            raise ValueError(f"El monto a depositar debe ser positivo: {monto}")
        self.__saldo += monto
        self.__historial.append(f"Depósito: +${monto:.2f} → saldo=${self.__saldo:.2f}")

    def retirar(self, monto: float) -> None:
        """Decrementa el saldo.

        Args:
            monto: Monto a retirar. Debe ser positivo y no mayor al saldo.

        Raises:
            ValueError: si el monto es inválido o el saldo es insuficiente.
        """
        if monto <= 0:
            raise ValueError(f"El monto a retirar debe ser positivo: {monto}")
        if monto > self.__saldo:
            raise ValueError(
                f"Saldo insuficiente: tenés ${self.__saldo:.2f}, "
                f"intentás retirar ${monto:.2f}"
            )
        self.__saldo -= monto
        self.__historial.append(f"Retiro:   -${monto:.2f} → saldo=${self.__saldo:.2f}")

    def transferir_a(self, destino: "CuentaBancaria", monto: float) -> None:
        """Transfiere monto a otra cuenta.

        Args:
            destino: Cuenta destino.
            monto: Monto a transferir.
        """
        self.retirar(monto)
        destino.depositar(monto)
        self.__historial[-1] += f" [→ {destino.titular}]"

    def __repr__(self) -> str:
        return f"CuentaBancaria({self._titular!r}, saldo=${self.__saldo:.2f})"


# ── Ejemplo 2: Temperatura (propiedad con setter validado) ───────────────────

class Termometro:
    """Termómetro con temperatura validada en cada asignación.

    Attributes:
        unidad: 'C' para Celsius, 'F' para Fahrenheit.
    """

    ABSOLUTO_CERO_C = -273.15

    def __init__(self, temperatura_c: float = 0.0) -> None:
        self.temperatura = temperatura_c   # usa el setter desde el inicio

    @property
    def temperatura(self) -> float:
        """Temperatura en Celsius."""
        return self._temperatura

    @temperatura.setter
    def temperatura(self, valor: float) -> None:
        if valor < self.ABSOLUTO_CERO_C:
            raise ValueError(
                f"La temperatura no puede ser menor al cero absoluto "
                f"({self.ABSOLUTO_CERO_C}°C): {valor}"
            )
        self._temperatura = valor

    @property
    def fahrenheit(self) -> float:
        """Convierte la temperatura a Fahrenheit (solo lectura)."""
        return self._temperatura * 9 / 5 + 32

    def __repr__(self) -> str:
        return f"Termometro({self._temperatura:.2f}°C / {self.fahrenheit:.2f}°F)"


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== CuentaBancaria ===")
    cuenta_ana = CuentaBancaria("Ana García", 1000.0)
    cuenta_carlos = CuentaBancaria("Carlos López", 500.0)

    cuenta_ana.depositar(200.0)
    cuenta_ana.retirar(150.0)
    cuenta_ana.transferir_a(cuenta_carlos, 300.0)

    print(f"\n  {cuenta_ana}")
    print(f"  {cuenta_carlos}")

    print("\n  Historial Ana:")
    for entrada in cuenta_ana.historial:
        print(f"    {entrada}")

    print("\n  Intentar acceso directo al saldo (name mangling):")
    try:
        _ = cuenta_ana.__saldo   # type: ignore
    except AttributeError as e:
        print(f"    AttributeError: {e}")
    # El atributo real está en: cuenta_ana._CuentaBancaria__saldo
    print(f"    Acceso via name mangling: {cuenta_ana._CuentaBancaria__saldo:.2f}")  # noqa

    print("\n  Errores de validación:")
    try:
        cuenta_ana.retirar(9999)
    except ValueError as e:
        print(f"    {e}")
    try:
        cuenta_ana.depositar(-50)
    except ValueError as e:
        print(f"    {e}")

    print("\n=== Termómetro ===")
    t = Termometro(100.0)
    print(f"  {t}")
    t.temperatura = -10.0
    print(f"  {t}")
    try:
        t.temperatura = -300.0
    except ValueError as e:
        print(f"  ValueError: {e}")
