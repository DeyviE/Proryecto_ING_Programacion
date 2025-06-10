from database import ConexionDB

class AgregarLibro:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, titulo, autor, isbn):
        try:
            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_libros (titulo, autor, isbn, disponible)
                VALUES (%s, %s, %s, TRUE)
                RETURNING id;
            """, (titulo, autor, isbn))
            nuevo_id = self.cursor.fetchone()[0]
            self.db.conn.commit()
            print(f"Libro agregado correctamente. ID: {nuevo_id}")
        except Exception as e:
            print("Error al agregar libro:", e)
            self.db.conn.rollback()
        finally:
            self.cursor.close()
            self.db.conn.close()
