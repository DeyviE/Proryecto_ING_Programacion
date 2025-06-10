from database import ConexionDB
from modelos.libro import Libro
from modelos.prestamo import Prestamo

class ActividadUsuario:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT
                    p.id AS prestamo_id,
                    l.id AS libro_id,
                    l.titulo,
                    p.fecha_prestamo,
                    p.fecha_devolucion
                FROM ingenieria_de_programacion.DOO_prestamos p
                JOIN ingenieria_de_programacion.DOO_libros l
                  ON p.libro_id = l.id
                WHERE p.usuario_id = %s
                ORDER BY p.fecha_prestamo;
            """, (usuario_id,))
            filas = self.cursor.fetchall()

            if not filas:
                print(f"No se encontraron préstamos para el usuario con ID {usuario_id}.")
                return

            print(f"=== Actividad de usuario {usuario_id} ===")
            for prestamo_id, libro_id, titulo, fecha_prestamo, fecha_devolucion in filas:
                estado = (
                    f"Devuelto el {fecha_devolucion}"
                    if fecha_devolucion is not None
                    else "No devuelto aún"
                )
                print(f"Préstamo {prestamo_id}: Libro {libro_id} – «{titulo}», "
                      f"Prestado: {fecha_prestamo}, {estado}")
        except Exception as e:
            print("Error al mostrar actividad de usuario:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
