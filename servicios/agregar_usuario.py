from database import ConexionDB

class AgregarUsuario:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self, nombre, correo):
        try:
            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_usuarios (nombre, correo)
                VALUES (%s, %s)
                RETURNING id;
            """, (nombre, correo))
            nuevo_id = self.cursor.fetchone()[0]
            self.db.conn.commit()
            print(f"Usuario agregado correctamente. ID: {nuevo_id}")
        except Exception as e:
            print("Error al agregar usuario:", e)
            self.db.conn.rollback()
        finally:
            self.cursor.close()
            self.db.conn.close()
