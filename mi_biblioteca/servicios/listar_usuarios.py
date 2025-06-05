from database import ConexionDB
from modelos.usuario import Usuario

class ListarUsuarios:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    def ejecutar(self):
        try:
            self.cursor.execute("""
                SELECT id, nombre, correo
                FROM ingenieria_de_programacion.DOO_usuarios
                ORDER BY id;
            """)
            filas = self.cursor.fetchall()
            usuarios = [Usuario(*fila) for fila in filas]

            if not usuarios:
                print("No hay usuarios registrados.")
                return

            print("=== Lista de usuarios ===")
            for usuario in usuarios:
                print(f"{usuario.id}: {usuario.nombre} – {usuario.correo}")
        except Exception as e:
            print("Error al listar usuarios:", e)
        finally:
            self.cursor.close()
            self.db.conn.close()
