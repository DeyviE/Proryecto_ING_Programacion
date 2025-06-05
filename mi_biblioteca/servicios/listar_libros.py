from database import ConexionDB
from modelos.libro import Libro

class ListarLibros:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self):
        try:
            self.cursor.execute("""
                SELECT id, titulo, autor, isbn, disponible
                FROM ingenieria_de_programacion.DOO_libros
                ORDER BY id;
            """)
            filas = self.cursor.fetchall()
            libros = [Libro(*fila) for fila in filas]

            if not libros:
                print("No hay libros registrados.")
                return

            print("=== Lista de libros ===")
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                print(f"{libro.id}: «{libro.titulo}» de {libro.autor} (ISBN: {libro.isbn}) – {estado}")
        except Exception as e:
            print("Error al listar libros:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
