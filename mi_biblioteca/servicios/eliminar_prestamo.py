from database import ConexionDB

class EliminarPrestamo:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, prestamo_id):
        try:
            self.cursor.execute("""
                DELETE FROM ingenieria_de_programacion.DOO_prestamos
                WHERE id = %s;
            """, (prestamo_id,))
            self.db.conn.commit()
            print("Préstamo eliminado correctamente.")
        except Exception as e:
            print("Error al eliminar préstamo:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
