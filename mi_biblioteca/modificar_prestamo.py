from database import ConexionDB

class ModificarPrestamo:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, prestamo_id, nuevo_libro_id, nuevo_usuario_id, nueva_fecha_prestamo, nueva_fecha_devolucion=None):
        try:
            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_prestamos
                SET libro_id = %s,
                    usuario_id = %s,
                    fecha_prestamo = %s,
                    fecha_devolucion = %s
                WHERE id = %s;
            """, (nuevo_libro_id, nuevo_usuario_id, nueva_fecha_prestamo, nueva_fecha_devolucion, prestamo_id))
            self.db.conn.commit()
            print("Préstamo actualizado correctamente.")
        except Exception as e:
            print("Error al modificar préstamo:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
