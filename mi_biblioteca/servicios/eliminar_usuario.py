from database import ConexionDB

class EliminarUsuario:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, usuario_id):
        try:
            self.cursor.execute("""
                DELETE FROM ingenieria_de_programacion.DOO_usuarios
                WHERE id = %s;
            """, (usuario_id,))
            self.db.conn.commit()
            print("Usuario eliminado correctamente.")
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
