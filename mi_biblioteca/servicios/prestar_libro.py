from database import ConexionDB
from datetime import date

class PrestarLibro:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, libro_id, usuario_id):
        try:
            self.cursor.execute("SELECT disponible FROM ingenieria_de_programacion.DOO_libros WHERE id = %s;", (libro_id,))
            result = self.cursor.fetchone()

            if not result:
                print("Libro no encontrado.")
                return

            if not result[0]:
                print("Libro no disponible.")
                return

            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_prestamos (libro_id, usuario_id, fecha_prestamo)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (libro_id, usuario_id, date.today()))
            prestamo_id = self.cursor.fetchone()[0]

            self.cursor.execute("UPDATE ingenieria_de_programacion.DOO_libros SET disponible = FALSE WHERE id = %s;", (libro_id,))

            self.db.conn.commit()
            print(f"Préstamo realizado. ID de préstamo: {prestamo_id}")
        except Exception as e:
            print("Error al prestar libro:", e)
            self.db.conn.rollback()
        finally:
            self.cursor.close()
            self.db.conn.close()
