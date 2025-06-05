from database import ConexionDB

class ListarLibrosPrestados:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self):
        try:
            self.cursor.execute("""
                SELECT p.id, l.id, l.titulo, l.autor, u.id, u.nombre, p.fecha_prestamo
                FROM ingenieria_de_programacion.DOO_prestamos p
                JOIN ingenieria_de_programacion.DOO_libros l ON p.libro_id = l.id
                JOIN ingenieria_de_programacion.DOO_usuarios u ON p.usuario_id = u.id
                WHERE p.fecha_devolucion IS NULL
                ORDER BY p.fecha_prestamo;
            """)
            filas = self.cursor.fetchall()

            if not filas:
                print("No hay libros prestados actualmente.")
                return

            print("=== Libros prestados actualmente ===")
            for prestamo_id, libro_id, titulo, autor, usuario_id, nombre, fecha in filas:
                print(f"Préstamo {prestamo_id}: Libro {libro_id} – «{titulo}» de {autor}, "
                      f"Usuario {usuario_id} – {nombre}, Fecha de préstamo: {fecha}")
        except Exception as e:
            print("Error al listar libros prestados:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
