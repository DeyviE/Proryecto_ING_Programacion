# gestion.py
from datetime import datetime, timedelta
from mi_biblioteca.prestamo import Prestamo

class GestionBiblioteca:
    def __init__(self):
        self.prestamos = []  # Lista de objetos Prestamo

    def registrar_prestamo(self, prestamo: Prestamo):
        """Registra un nuevo préstamo en el sistema."""
        self.prestamos.append(prestamo)

    def estado_libro(self, libro_obj):
        """Devuelve si el libro está prestado o disponible y, si aplica, la fecha de devolución."""
        for prestamo in self.prestamos:
            if prestamo.libro == libro_obj and prestamo.fecha_devolucion >= datetime.now():
                return f"📕 Prestado. Disponible el {prestamo.fecha_devolucion.strftime('%Y-%m-%d')}"
        return "📗 Disponible"

    def historial_libro(self, libro_obj, desde=None):
        """
        Devuelve el historial de préstamos de un libro desde una fecha específica.
        Si no se indica fecha, por defecto se considera 1 año atrás.
        """
        if desde is None:
            desde = datetime.now() - timedelta(days=365)

        historial = [
            p for p in self.prestamos
            if p.libro == libro_obj and p.fecha_prestamo >= desde
        ]

        if not historial:
            return "No hay préstamos registrados en el último año."

        resultado = [f"📚 Historial de préstamos para '{libro_obj.titulo}':"]
        for p in historial:
            resultado.append(f" - Prestado por {p.usuario} del {p.fecha_prestamo.strftime('%Y-%m-%d')} al {p.fecha_devolucion.strftime('%Y-%m-%d')}")

        return "\n".join(resultado)
