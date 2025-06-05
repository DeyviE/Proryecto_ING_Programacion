from database import ConexionDB
from datetime import date, timedelta
from modelos.prestamo import Prestamo
from modelos.libros import Libro

class PrestarLibro:
    def __init__(self, gestion):
        self.db = ConexionDB()
        self.cursor = self.db.cursor
        self.gestion = gestion

    def ejecutar(self, libro_id, usuario_id):
        try:
            # Verificar disponibilidad
            self.cursor.execute("SELECT disponible FROM ingenieria_de_programacion.DOO_libros WHERE id = %s;", (libro_id,))
            result = self.cursor.fetchone()

            if not result:
                print("Libro no encontrado.")
                return

            if not result[0]:
                print("Libro no disponible.")
                return

            # Insertar préstamo en BD
            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_prestamos (libro_id, usuario_id, fecha_prestamo)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (libro_id, usuario_id, date.today()))
            prestamo_id = self.cursor.fetchone()[0]

            # Obtener datos del libro
            self.cursor.execute("""
                SELECT id, titulo, autor, isbn, disponible
                FROM ingenieria_de_programacion.DOO_libros
                WHERE id = %s;
            """, (libro_id,))
            libro_data = self.cursor.fetchone()
            libro_obj = Libro(*libro_data)

            # Obtener nombre del usuario
            usuario_nombre = self.obtener_nombre_usuario(usuario_id)

            # Crear préstamo (7 días)
            prestamo_obj = Prestamo(
                usuario_nombre,
                libro_obj,
                date.today(),
                date.today() + timedelta(days=7)
            )

            # Registrar en gestión
            self.gestion.registrar_prestamo(prestamo_obj)

            # Marcar como no disponible
            self.cursor.execute("UPDATE ingenieria_de_programacion.DOO_libros SET disponible = FALSE WHERE id = %s;", (libro_id,))

            self.db.conn.commit()
            print(f"Préstamo realizado. ID de préstamo: {prestamo_id}")

        except Exception as e:
            print("Error al prestar libro:", e)
            self.db.conn.rollback()

        finally:
            self.cursor.close()
            self.db.conn.close()

    def obtener_nombre_usuario(self, usuario_id):
        self.cursor.execute("SELECT nombre FROM ingenieria_de_programacion.DOO_usuarios WHERE id = %s;", (usuario_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Desconocido"
