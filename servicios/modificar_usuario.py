from database import ConexionDB

class ModificarUsuario:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, usuario_id, nuevo_nombre, nuevo_correo):
        try:
            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_usuarios
                SET nombre = %s, correo = %s
                WHERE id = %s;
            """, (nuevo_nombre, nuevo_correo, usuario_id))
            self.db.conn.commit()
            print("Usuario actualizado correctamente.")
        except Exception as e:
            print("Error al modificar usuario:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
