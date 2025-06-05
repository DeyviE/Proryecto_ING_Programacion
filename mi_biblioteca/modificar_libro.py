from database import ConexionDB

class ModificarLibro:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, libro_id, nuevo_titulo, nuevo_autor, nuevo_isbn):
        try:
            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_libros
                SET titulo = %s, autor = %s, isbn = %s
                WHERE id = %s;
            """, (nuevo_titulo, nuevo_autor, nuevo_isbn, libro_id))
            self.db.conn.commit()
            print("Libro actualizado correctamente.")
        except Exception as e:
            print("Error al modificar libro:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()