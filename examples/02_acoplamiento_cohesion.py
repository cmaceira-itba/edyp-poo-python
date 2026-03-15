"""
Capítulo: Acoplamiento y Cohesión
-----------------------------------
Alto vs. bajo acoplamiento: cómo las dependencias hardcodeadas dificultan
los cambios. Alta vs. baja cohesión: clases con responsabilidad bien definida.
"""


# ── ACOPLAMIENTO ─────────────────────────────────────────────────────────────

# ❌ Alto acoplamiento: OrderProcessor crea su propia dependencia
class FileLogger:
    """Guarda mensajes en un archivo de texto."""

    def __init__(self) -> None:
        self.ruta = "./pedidos.log"

    def registrar(self, mensaje: str) -> None:
        # En un ejemplo real escribiría al disco; acá imprimimos para simular.
        print(f"[FileLogger → {self.ruta}] {mensaje}")


class OrderProcessorAcoplado:
    """Procesa pedidos. Versión con alto acoplamiento."""

    def __init__(self) -> None:
        self._logger = FileLogger()   # ❌ dependencia hardcodeada

    def procesar(self, detalle: str) -> None:
        self._logger.registrar(f"Pedido procesado: {detalle}")


# ✅ Bajo acoplamiento: el logger se inyecta desde afuera
class ConsoleLogger:
    """Alternativa de logger que imprime por consola."""

    def registrar(self, mensaje: str) -> None:
        print(f"[ConsoleLogger] {mensaje}")


class NullLogger:
    """Logger que no hace nada (útil en tests)."""

    def registrar(self, mensaje: str) -> None:
        pass


class OrderProcessor:
    """Procesa pedidos. Versión con bajo acoplamiento (inyección de dependencia)."""

    def __init__(self, logger) -> None:
        self._logger = logger   # ✅ recibe cualquier objeto que tenga .registrar()

    def procesar(self, detalle: str) -> None:
        self._logger.registrar(f"Pedido procesado: {detalle}")


# ── COHESIÓN ──────────────────────────────────────────────────────────────────

# ❌ Baja cohesión: una clase hace de todo
class UserManagerMalDiseñado:
    """Hace demasiado: mezcla persistencia, email y reportes."""

    def crear_usuario(self, nombre: str) -> dict:
        return {"nombre": nombre, "activo": True}

    def enviar_bienvenida(self, usuario: dict) -> None:
        # ¿Por qué gestión de usuarios envía emails?
        print(f"[Email] Bienvenido, {usuario['nombre']}!")

    def generar_reporte(self, usuarios: list[dict]) -> str:
        # ¿Y también genera reportes?
        return f"Total usuarios: {len(usuarios)}"


# ✅ Alta cohesión: cada clase tiene una única responsabilidad
class UserRepository:
    """Solo se encarga de crear y buscar usuarios en memoria."""

    def __init__(self) -> None:
        self._usuarios: list[dict] = []

    def crear(self, nombre: str) -> dict:
        usuario = {"id": len(self._usuarios) + 1, "nombre": nombre, "activo": True}
        self._usuarios.append(usuario)
        return usuario

    def listar(self) -> list[dict]:
        return list(self._usuarios)

    def buscar_por_nombre(self, nombre: str) -> dict | None:
        return next((u for u in self._usuarios if u["nombre"] == nombre), None)


class WelcomeEmailService:
    """Solo se encarga de enviar emails de bienvenida."""

    def enviar(self, usuario: dict) -> None:
        print(f"[EmailService] Bienvenido al sistema, {usuario['nombre']}!")


class UserReportGenerator:
    """Solo se encarga de generar reportes de usuarios."""

    def generar(self, usuarios: list[dict]) -> str:
        activos = sum(1 for u in usuarios if u["activo"])
        return f"Total: {len(usuarios)} | Activos: {activos}"


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Acoplamiento ===")
    print("\n-- Alto acoplamiento (FileLogger hardcodeado) --")
    procesador_acoplado = OrderProcessorAcoplado()
    procesador_acoplado.procesar("Laptop x1")

    print("\n-- Bajo acoplamiento (logger inyectado) --")
    procesador_consola = OrderProcessor(ConsoleLogger())
    procesador_consola.procesar("Monitor x2")

    procesador_silencioso = OrderProcessor(NullLogger())
    procesador_silencioso.procesar("Teclado x1")   # no imprime nada → ideal para tests
    print("  (NullLogger: nada impreso, pero el pedido se procesó)")

    print("\n=== Cohesión ===")
    repo = UserRepository()
    email_service = WelcomeEmailService()
    report_gen = UserReportGenerator()

    u1 = repo.crear("Ana García")
    u2 = repo.crear("Carlos López")
    email_service.enviar(u1)
    email_service.enviar(u2)

    print(f"\nReporte: {report_gen.generar(repo.listar())}")
    print(f"Buscar 'Ana': {repo.buscar_por_nombre('Ana García')}")
    print(f"Buscar 'Pedro': {repo.buscar_por_nombre('Pedro')}")
