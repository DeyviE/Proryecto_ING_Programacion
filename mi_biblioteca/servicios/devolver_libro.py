from database import ConexionDB
from datetime import date

class DevolverLibro:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, libro_id):
        try:
            self.cursor.execute("""
                SELECT id FROM ingenieria_de_programacion.DOO_prestamos
                WHERE libro_id = %s AND fecha_devolucion IS NULL
                ORDER BY fecha_prestamo DESC LIMIT 1;
            """, (libro_id,))
            row = self.cursor.fetchone()

            if not row:
                print("No hay préstamo activo para este libro.")
                return

            prestamo_id = row[0]

            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_prestamos
                SET fecha_devolucion = %s
                WHERE id = %s;
            """, (date.today(), prestamo_id))

            self.cursor.execute("UPDATE ingenieria_de_programacion.DOO_libros SET disponible = TRUE WHERE id = %s;", (libro_id,))

            self.db.conn.commit()
            print(f"Libro devuelto. Préstamo actualizado (ID {prestamo_id})")
        except Exception as e:
            print("Error al devolver libro:", e)
            self.db.conn.rollback()
        finally:
            self.cursor.close()
            self.db.conn.close()
