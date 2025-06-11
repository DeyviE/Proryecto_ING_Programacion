from database import ConexionDB
from modelos.libro import Libro
from modelos.usuario import Usuario
from modelos.prestamo import Prestamo
from datetime import date

class GestionBiblioteca:
    def __init__(self):
        self.db = ConexionDB()
        self.cursor = self.db.cursor

    # --- Operaciones de Libro ---
    def agregar_libro(self, titulo, autor, isbn):
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

    def listar_libros(self):
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
                return []
            
            # print("=== Lista de libros ===") # Esto es para la consola
            # for libro in libros:
            #     estado = "Disponible" if libro.disponible else "Prestado"
            #     print(f"{libro.id}: «{libro.titulo}» de {libro.autor} (ISBN: {libro.isbn}) – {estado}")
            return libros # Retorna la lista de objetos Libro
        except Exception as e:
            print("Error al listar libros:", e)
            return []
        finally:
            # En una aplicación web, es mejor manejar el cierre de conexión por cada request
            # o usar un pool de conexiones. Por ahora, lo cerramos aquí.
            pass # No cerramos la conexión aquí si la vamos a usar en el mismo request de Flask


    def modificar_libro(self, libro_id, nuevo_titulo, nuevo_autor, nuevo_isbn):
        try:
            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_libros
                SET titulo = %s, autor = %s, isbn = %s
                WHERE id = %s;
            """, (nuevo_titulo, nuevo_autor, nuevo_isbn, libro_id))
            self.db.conn.commit()
            print("Libro actualizado correctamente.")
            return True
        except Exception as e:
            print("Error al modificar libro:", e)
            self.db.conn.rollback()
            return False
        finally:
            pass # Mantener la conexión abierta o cerrar fuera

    # --- Operaciones de Usuario ---
    def agregar_usuario(self, nombre, correo):
        try:
            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_usuarios (nombre, correo)
                VALUES (%s, %s)
                RETURNING id;
            """, (nombre, correo))
            nuevo_id = self.cursor.fetchone()[0]
            self.db.conn.commit()
            print(f"Usuario agregado correctamente. ID: {nuevo_id}")
            return nuevo_id
        except Exception as e:
            print("Error al agregar usuario:", e)
            self.db.conn.rollback()
            return None
        finally:
            pass

    def listar_usuarios(self):
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
                return []
            # print("=== Lista de usuarios ===") # Para consola
            # for usuario in usuarios:
            #     print(f"{usuario.id}: {usuario.nombre} ({usuario.correo})")
            return usuarios # Retorna la lista de objetos Usuario
        except Exception as e:
            print("Error al listar usuarios:", e)
            return []
        finally:
            pass

    def modificar_usuario(self, usuario_id, nuevo_nombre, nuevo_correo):
        try:
            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_usuarios
                SET nombre = %s, correo = %s
                WHERE id = %s;
            """, (nuevo_nombre, nuevo_correo, usuario_id))
            self.db.conn.commit()
            print("Usuario actualizado correctamente.")
            return True
        except Exception as e:
            print("Error al modificar usuario:", e)
            self.db.conn.rollback()
            return False
        finally:
            pass

    # --- Operaciones de Préstamo ---
    def prestar_libro(self, libro_id, usuario_id):
        try:
            # Verificar disponibilidad del libro
            self.cursor.execute("SELECT disponible FROM ingenieria_de_programacion.DOO_libros WHERE id = %s;", (libro_id,))
            disponible = self.cursor.fetchone()
            if not disponible or not disponible[0]:
                print("El libro no está disponible o no existe.")
                return False

            # Verificar existencia del usuario
            self.cursor.execute("SELECT id FROM ingenieria_de_programacion.DOO_usuarios WHERE id = %s;", (usuario_id,))
            usuario_existe = self.cursor.fetchone()
            if not usuario_existe:
                print("El usuario no existe.")
                return False

            self.cursor.execute("""
                INSERT INTO ingenieria_de_programacion.DOO_prestamos (libro_id, usuario_id, fecha_prestamo, fecha_devolucion)
                VALUES (%s, %s, %s, NULL)
                RETURNING id;
            """, (libro_id, usuario_id, date.today()))
            prestamo_id = self.cursor.fetchone()[0]

            self.cursor.execute("UPDATE ingenieria_de_programacion.DOO_libros SET disponible = FALSE WHERE id = %s;", (libro_id,))

            self.db.conn.commit()
            print(f"Libro prestado correctamente. Préstamo ID: {prestamo_id}")
            return True
        except Exception as e:
            print("Error al prestar libro:", e)
            self.db.conn.rollback()
            return False
        finally:
            pass

    def devolver_libro(self, libro_id):
        try:
            self.cursor.execute("""
                SELECT id FROM ingenieria_de_programacion.DOO_prestamos
                WHERE libro_id = %s AND fecha_devolucion IS NULL
                ORDER BY fecha_prestamo DESC LIMIT 1;
            """, (libro_id,))
            row = self.cursor.fetchone()

            if not row:
                print("No hay préstamo activo para este libro.")
                return False

            prestamo_id = row[0]

            self.cursor.execute("""
                UPDATE ingenieria_de_programacion.DOO_prestamos
                SET fecha_devolucion = %s
                WHERE id = %s;
            """, (date.today(), prestamo_id))

            self.cursor.execute("UPDATE ingenieria_de_programacion.DOO_libros SET disponible = TRUE WHERE id = %s;", (libro_id,))

            self.db.conn.commit()
            print(f"Libro devuelto. Préstamo actualizado (ID {prestamo_id})")
            return True
        except Exception as e:
            print("Error al devolver libro:", e)
            self.db.conn.rollback()
            return False
        finally:
            pass

    def listar_libros_prestados(self):
        try:
            self.cursor.execute("""
                SELECT
                    p.id,
                    l.id,
                    l.titulo,
                    u.id,
                    u.nombre,
                    p.fecha_prestamo,
                    p.fecha_devolucion
                FROM ingenieria_de_programacion.DOO_prestamos p
                JOIN ingenieria_de_programacion.DOO_libros l ON p.libro_id = l.id
                JOIN ingenieria_de_programacion.DOO_usuarios u ON p.usuario_id = u.id
                ORDER BY p.fecha_prestamo DESC;
            """)
            filas = self.cursor.fetchall()
            prestamos = []
            for fila in filas:
                prestamos.append(Prestamo(
                    id=fila[0],
                    libro_id=fila[1],
                    usuario_id=fila[3],
                    fecha_prestamo=fila[5],
                    fecha_devolucion=fila[6],
                    titulo_libro=fila[2],  # Título del libro
                    nombre_usuario=fila[4]  # Nombre del usuario
                ))

            if not prestamos:
                print("No hay libros prestados actualmente.")
                return []
            
            # print("=== Libros Prestados ===") # Para consola
            # for p in prestamos:
            #     estado = f"Devuelto el {p.fecha_devolucion}" if p.fecha_devolucion else "No devuelto aún"
            #     print(f"ID Préstamo: {p.id}, Libro: «{p.titulo_libro}» (ID: {p.libro_id}), "
            #           f"Usuario: {p.nombre_usuario} (ID: {p.usuario_id}), "
            #           f"Prestado: {p.fecha_prestamo}, {estado}")
            return prestamos # Retorna la lista de objetos Prestamo
        except Exception as e:
            print("Error al listar libros prestados:", e)
            return []
        finally:
            pass

    def modificar_prestamo(self, prestamo_id, nuevo_libro_id, nuevo_usuario_id, nueva_fecha_prestamo, nueva_fecha_devolucion=None):
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
            return True
        except Exception as e:
            print("Error al modificar préstamo:", e)
            self.db.conn.rollback()
            return False
        finally:
            pass

    def obtener_actividad_usuario(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT
                    p.id AS prestamo_id,
                    l.id AS libro_id,
                    l.titulo,
                    p.fecha_prestamo,
                    p.fecha_devolucion
                FROM ingenieria_de_programacion.DOO_prestamos p
                JOIN ingenieria_de_programacion.DOO_libros l
                  ON p.libro_id = l.id
                WHERE p.usuario_id = %s
                ORDER BY p.fecha_prestamo;
            """, (usuario_id,))
            filas = self.cursor.fetchall()

            if not filas:
                # print(f"No se encontraron préstamos para el usuario con ID {usuario_id}.") # Para consola
                return []

            actividad = []
            # print(f"=== Actividad de usuario {usuario_id} ===") # Para consola
            for prestamo_id, libro_id, titulo, fecha_prestamo, fecha_devolucion in filas:
                estado = (
                    f"Devuelto el {fecha_devolucion}"
                    if fecha_devolucion is not None
                    else "No devuelto aún"
                )
                actividad.append({
                    "prestamo_id": prestamo_id,
                    "libro_id": libro_id,
                    "titulo": titulo,
                    "fecha_prestamo": fecha_prestamo,
                    "fecha_devolucion": fecha_devolucion,
                    "estado": estado
                })
                # print(f"Préstamo {prestamo_id}: Libro {libro_id} – «{titulo}», " # Para consola
                #       f"Prestado: {fecha_prestamo}, {estado}")
            return actividad # Retorna la lista de diccionarios
        except Exception as e:
            print("Error al mostrar actividad de usuario:", e)
            return []
        finally:
            pass # Mantener la conexión abierta o cerrar fuera

    # Nota: Los métodos de cierre de conexión los he comentado o puesto 'pass'
    # en los finally para evitar problemas de cierre prematuro en un entorno web
    # donde una misma conexión podría usarse para varias operaciones dentro
    # de un único request HTTP. Sin embargo, en un script de consola como main.py,
    # sí es importante cerrar la conexión al final de cada operación.
    # Para Flask, es mejor manejar el cierre de la conexión al final de cada request.