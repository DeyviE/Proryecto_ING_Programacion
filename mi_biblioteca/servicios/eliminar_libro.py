from database import ConexionDB

class EliminarLibro:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, libro_id):
        try:
            self.cursor.execute("""
                DELETE FROM ingenieria_de_programacion.DOO_libros
                WHERE id = %s;
            """, (libro_id,))
            self.db.conn.commit()
            print("Libro eliminado correctamente.")
        except Exception as e:
            print("Error al eliminar libro:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()