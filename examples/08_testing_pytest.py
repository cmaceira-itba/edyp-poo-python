"""
Capítulo: Testing de Clases con pytest
----------------------------------------
Ejecutar con:  pytest examples/08_testing_pytest.py -v

Este archivo es autónomo: define las clases bajo test y los tests en el mismo
lugar para que sea fácil de estudiar. En un proyecto real vivirían en
src/ y tests/ por separado.

Patrones cubiertos:
  - Tests básicos con assert
  - Verificación de excepciones con pytest.raises
  - Fixtures para evitar duplicar el setup
  - Mocking con MagicMock(spec=...)
  - pytest.approx para comparar floats
"""

import pytest
from unittest.mock import MagicMock


# ═══════════════════════════════════════════════════════════════════════════════
# Clases de dominio (normalmente en src/)
# ═══════════════════════════════════════════════════════════════════════════════

class CuentaBancaria:
    """Cuenta bancaria con saldo protegido."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        if not titular or not titular.strip():
            raise TypeError("El titular debe ser un string no vacío")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        self._titular = titular
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def titular(self) -> str:
        return self._titular

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto

    def __repr__(self) -> str:
        return f"CuentaBancaria({self._titular!r}, saldo=${self._saldo:.2f})"


class GatewayPago:
    """Servicio externo de pago. En tests se mockea para no llamar la API real."""

    def procesar(self, monto: float, tarjeta: str) -> bool:
        raise NotImplementedError("Esto conectaría con la API real")


class ProcesadorPedido:
    """Procesa pedidos aplicando comisión y delegando el pago al gateway.

    Attributes:
        gateway: Servicio de pago inyectado por el constructor.
        comision: Porcentaje de comisión sobre el total (0.0 a 1.0).
    """

    def __init__(self, gateway: GatewayPago, comision: float = 0.05) -> None:
        if not 0 <= comision <= 1:
            raise ValueError(f"La comisión debe estar entre 0 y 1: {comision}")
        self._gateway = gateway
        self._comision = comision

    def procesar_pedido(self, monto: float, tarjeta: str) -> dict:
        """Procesa el pago de un pedido.

        Returns:
            dict con 'aprobado' (bool) y 'total_cobrado' (float).

        Raises:
            ValueError: si el monto no es positivo.
        """
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        total = monto * (1 + self._comision)
        aprobado = self._gateway.procesar(total, tarjeta)
        return {"aprobado": aprobado, "total_cobrado": total if aprobado else 0.0}


# ═══════════════════════════════════════════════════════════════════════════════
# Tests (normalmente en tests/)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cuenta_vacia() -> CuentaBancaria:
    """Cuenta sin saldo inicial."""
    return CuentaBancaria("Test User")


@pytest.fixture
def cuenta_con_saldo() -> CuentaBancaria:
    """Cuenta con $1000 lista para operar."""
    return CuentaBancaria("Test User", 1000.0)


@pytest.fixture
def gateway_mock() -> MagicMock:
    """Mock del gateway de pago con spec para evitar métodos fantasma."""
    return MagicMock(spec=GatewayPago)


# ── Tests de CuentaBancaria ───────────────────────────────────────────────────

class TestCuentaBancaria:
    """Tests unitarios para CuentaBancaria."""

    def test_saldo_inicial_por_defecto_es_cero(self, cuenta_vacia: CuentaBancaria) -> None:
        assert cuenta_vacia.saldo == 0.0

    def test_saldo_inicial_se_asigna(self) -> None:
        cuenta = CuentaBancaria("Ana", 500.0)
        assert cuenta.saldo == 500.0

    def test_titular_se_guarda(self) -> None:
        cuenta = CuentaBancaria("Carlos López", 0.0)
        assert cuenta.titular == "Carlos López"

    def test_saldo_inicial_negativo_lanza_value_error(self) -> None:
        with pytest.raises(ValueError):
            CuentaBancaria("Ana", -1.0)

    def test_titular_vacio_lanza_type_error(self) -> None:
        with pytest.raises(TypeError):
            CuentaBancaria("")

    def test_titular_solo_espacios_lanza_type_error(self) -> None:
        with pytest.raises(TypeError):
            CuentaBancaria("   ")

    def test_depositar_incrementa_saldo(self, cuenta_con_saldo: CuentaBancaria) -> None:
        cuenta_con_saldo.depositar(500.0)
        assert cuenta_con_saldo.saldo == 1500.0

    def test_depositar_multiples_veces_acumula(self, cuenta_vacia: CuentaBancaria) -> None:
        cuenta_vacia.depositar(100.0)
        cuenta_vacia.depositar(200.0)
        cuenta_vacia.depositar(300.0)
        assert cuenta_vacia.saldo == 600.0

    def test_depositar_monto_negativo_lanza_error(self, cuenta_con_saldo: CuentaBancaria) -> None:
        with pytest.raises(ValueError, match="debe ser positivo"):
            cuenta_con_saldo.depositar(-50.0)

    def test_depositar_cero_lanza_error(self, cuenta_con_saldo: CuentaBancaria) -> None:
        with pytest.raises(ValueError):
            cuenta_con_saldo.depositar(0.0)

    def test_retirar_reduce_saldo(self, cuenta_con_saldo: CuentaBancaria) -> None:
        cuenta_con_saldo.retirar(300.0)
        assert cuenta_con_saldo.saldo == 700.0

    def test_retirar_exactamente_el_saldo(self, cuenta_con_saldo: CuentaBancaria) -> None:
        """Caso borde: retirar exactamente lo disponible debe dejar saldo 0."""
        cuenta_con_saldo.retirar(1000.0)
        assert cuenta_con_saldo.saldo == 0.0

    def test_retirar_mas_del_saldo_lanza_error(self, cuenta_con_saldo: CuentaBancaria) -> None:
        with pytest.raises(ValueError, match="Saldo insuficiente"):
            cuenta_con_saldo.retirar(9999.0)

    def test_retirar_monto_negativo_lanza_error(self, cuenta_con_saldo: CuentaBancaria) -> None:
        with pytest.raises(ValueError):
            cuenta_con_saldo.retirar(-100.0)

    def test_operaciones_secuenciales(self, cuenta_con_saldo: CuentaBancaria) -> None:
        """Verifica que depósitos y retiros sucesivos son consistentes."""
        cuenta_con_saldo.depositar(200.0)   # 1200
        cuenta_con_saldo.retirar(500.0)     # 700
        cuenta_con_saldo.depositar(100.0)   # 800
        assert cuenta_con_saldo.saldo == 800.0


# ── Tests de ProcesadorPedido (con mocking) ───────────────────────────────────

class TestProcesadorPedido:
    """Tests de ProcesadorPedido. GatewayPago siempre es mockeado."""

    def test_pedido_aprobado_retorna_total_con_comision(
        self, gateway_mock: MagicMock
    ) -> None:
        gateway_mock.procesar.return_value = True
        procesador = ProcesadorPedido(gateway_mock, comision=0.10)

        resultado = procesador.procesar_pedido(100.0, "4111-1111-1111-1111")

        assert resultado["aprobado"] is True
        assert resultado["total_cobrado"] == pytest.approx(110.0)

    def test_pedido_rechazado_retorna_cero(self, gateway_mock: MagicMock) -> None:
        gateway_mock.procesar.return_value = False
        procesador = ProcesadorPedido(gateway_mock)

        resultado = procesador.procesar_pedido(200.0, "tarjeta-invalida")

        assert resultado["aprobado"] is False
        assert resultado["total_cobrado"] == 0.0

    def test_monto_negativo_no_llama_al_gateway(self, gateway_mock: MagicMock) -> None:
        procesador = ProcesadorPedido(gateway_mock)

        with pytest.raises(ValueError):
            procesador.procesar_pedido(-50.0, "tarjeta")

        # El gateway NO debe llamarse si el monto es inválido
        gateway_mock.procesar.assert_not_called()

    def test_comision_cero_no_altera_el_monto(self, gateway_mock: MagicMock) -> None:
        gateway_mock.procesar.return_value = True
        procesador = ProcesadorPedido(gateway_mock, comision=0.0)

        resultado = procesador.procesar_pedido(500.0, "tarjeta")

        assert resultado["total_cobrado"] == pytest.approx(500.0)

    def test_gateway_llamado_con_monto_correcto(self, gateway_mock: MagicMock) -> None:
        gateway_mock.procesar.return_value = True
        procesador = ProcesadorPedido(gateway_mock, comision=0.05)
        tarjeta = "1234-5678-9012-3456"

        procesador.procesar_pedido(200.0, tarjeta)

        gateway_mock.procesar.assert_called_once_with(
            pytest.approx(210.0), tarjeta
        )

    def test_comision_invalida_lanza_error(self, gateway_mock: MagicMock) -> None:
        with pytest.raises(ValueError):
            ProcesadorPedido(gateway_mock, comision=1.5)


# ── Main (para ejecutar manualmente sin pytest) ───────────────────────────────

if __name__ == "__main__":
    print("Este archivo está diseñado para ejecutarse con pytest:")
    print("  pytest examples/08_testing_pytest.py -v")
    print()
    print("Ejecutando una demostración rápida sin pytest...")

    # Demo básica de las clases
    cuenta = CuentaBancaria("Demo User", 500.0)
    cuenta.depositar(200.0)
    cuenta.retirar(100.0)
    print(f"  Cuenta demo: {cuenta}")

    gw = MagicMock(spec=GatewayPago)
    gw.procesar.return_value = True
    proc = ProcesadorPedido(gw, comision=0.10)
    res = proc.procesar_pedido(100.0, "tarjeta-demo")
    print(f"  Pedido demo: {res}")
