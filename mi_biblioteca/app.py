from flask import Flask, render_template, request, redirect, url_for
from servicios.agregar_libro import AgregarLibro
from servicios.listar_libros import ListarLibros
from servicios.agregar_usuario import AgregarUsuario
from servicios.listar_usuarios import ListarUsuarios
from servicios.prestar_libro import PrestarLibro
from servicios.devolver_libro import DevolverLibro
from servicios.listar_libros_prestados import ListarLibrosPrestados
from servicios.actividad_usuario import ActividadUsuario
from servicios.modificar_libro import ModificarLibro
from servicios.modificar_usuario import ModificarUsuario
from servicios.modificar_prestamo import ModificarPrestamo
from modelos.GestionBiblioteca import GestionBiblioteca # If still used, otherwise remove

app = Flask(__name__)
gestion = GestionBiblioteca() # If you're still using this central management class

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libros')
def listar_libros():
    # You might need to refactor ListarLibros to return data instead of printing
    # For now, let's assume it prints and we'll capture output or refactor later.
    # A better approach would be to have a method in ListarLibros that returns a list of book dictionaries/objects.
    
    # --- Refactored ListarLibros to return data ---
    class ListarLibrosWeb(ListarLibros):
        def ejecutar_web(self):
            try:
                self.cursor.execute("""
                    SELECT id, titulo, autor, isbn, disponible
                    FROM ingenieria_de_programacion.DOO_libros
                    ORDER BY id;
                """)
                filas = self.cursor.fetchall()
                # Assuming Libro is a simple data class or tuple, convert to dict for easier template rendering
                libros_data = []
                for fila in filas:
                    libros_data.append({
                        'id': fila[0],
                        'titulo': fila[1],
                        'autor': fila[2],
                        'isbn': fila[3],
                        'disponible': "Disponible" if fila[4] else "Prestado"
                    })
                return libros_data
            except Exception as e:
                print("Error al listar libros:", e)
                return []
            finally:
                self.cursor.close()
                self.db.conn.close()

    libros = ListarLibrosWeb().ejecutar_web()
    return render_template('list_books.html', libros=libros)

@app.route('/libros/agregar', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        isbn = request.form['isbn']
        
        # Instantiate and execute your existing service
        add_book_service = AgregarLibro()
        # You'll need to modify AgregarLibro to return success/failure or redirect based on outcome
        # For now, let's assume it handles its own printing and we just redirect.
        add_book_service.ejecutar(titulo, autor, isbn)
        return redirect(url_for('listar_libros'))
    return render_template('add_book.html')

@app.route('/libros/modificar/<int:libro_id>', methods=['GET', 'POST'])
def modificar_libro(libro_id):
    # To pre-fill the form, you'd ideally fetch the book details first
    # This would require a 'get_book_by_id' method in your services or directly querying here.
    
    # For simplicity, we'll just handle the POST request.
    if request.method == 'POST':
        nuevo_titulo = request.form['nuevo_titulo']
        nuevo_autor = request.form['nuevo_autor']
        nuevo_isbn = request.form['nuevo_isbn']
        
        ModificarLibro().ejecutar(libro_id, nuevo_titulo, nuevo_autor, nuevo_isbn)
        return redirect(url_for('listar_libros'))
    
    # In a real app, you'd fetch the book details and pass them to the template for pre-filling
    return render_template('modificar_libro.html', libro_id=libro_id)

# --- Add routes for other functionalities (usuarios, prestamos, etc.) ---

@app.route('/usuarios')
def listar_usuarios():
    class ListarUsuariosWeb(ListarUsuarios):
        def ejecutar_web(self):
            try:
                self.cursor.execute("""
                    SELECT id, nombre, correo
                    FROM ingenieria_de_programacion.DOO_usuarios
                    ORDER BY id;
                """)
                filas = self.cursor.fetchall()
                usuarios_data = []
                for fila in filas:
                    usuarios_data.append({
                        'id': fila[0],
                        'nombre': fila[1],
                        'correo': fila[2]
                    })
                return usuarios_data
            except Exception as e:
                print("Error al listar usuarios:", e)
                return []
            finally:
                self.cursor.close()
                self.db.conn.close()

    usuarios = ListarUsuariosWeb().ejecutar_web()
    return render_template('list_users.html', usuarios=usuarios)

@app.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        
        AgregarUsuario().ejecutar(nombre, correo)
        return redirect(url_for('listar_usuarios'))
    return render_template('add_user.html')

@app.route('/usuarios/modificar/<int:usuario_id>', methods=['GET', 'POST'])
def modificar_usuario(usuario_id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nuevo_nombre']
        nuevo_correo = request.form['nuevo_correo']
        
        ModificarUsuario().ejecutar(usuario_id, nuevo_nombre, nuevo_correo)
        return redirect(url_for('listar_usuarios'))
    return render_template('modificar_usuario.html', usuario_id=usuario_id)

@app.route('/prestamos')
def listar_prestamos():
    class ListarLibrosPrestadosWeb(ListarLibrosPrestados):
        def ejecutar_web(self):
            try:
                self.cursor.execute("""
                    SELECT
                        p.id AS prestamo_id,
                        l.titulo,
                        u.nombre AS usuario_nombre,
                        p.fecha_prestamo,
                        p.fecha_devolucion
                    FROM ingenieria_de_programacion.DOO_prestamos p
                    JOIN ingenieria_de_programacion.DOO_libros l ON p.libro_id = l.id
                    JOIN ingenieria_de_programacion.DOO_usuarios u ON p.usuario_id = u.id
                    ORDER BY p.fecha_prestamo DESC;
                """)
                filas = self.cursor.fetchall()
                prestamos_data = []
                for fila in filas:
                    prestamos_data.append({
                        'prestamo_id': fila[0],
                        'titulo_libro': fila[1],
                        'nombre_usuario': fila[2],
                        'fecha_prestamo': fila[3],
                        'fecha_devolucion': fila[4] if fila[4] else "Pendiente"
                    })
                return prestamos_data
            except Exception as e:
                print("Error al listar préstamos:", e)
                return []
            finally:
                self.cursor.close()
                self.db.conn.close()
                
    prestamos = ListarLibrosPrestadosWeb().ejecutar_web()
    return render_template('list_loans.html', prestamos=prestamos)

@app.route('/prestamos/prestar', methods=['GET', 'POST'])
def prestar_libro():
    if request.method == 'POST':
        libro_id = int(request.form['libro_id'])
        usuario_id = int(request.form['usuario_id'])
        
        PrestarLibro(gestion).ejecutar(libro_id, usuario_id) # Assuming GestionBiblioteca is needed
        return redirect(url_for('listar_prestamos'))
    
    # You might want to list available books and users in the template
    # For now, it's just input fields.
    return render_template('lend_book.html')

@app.route('/prestamos/devolver', methods=['GET', 'POST'])
def devolver_libro():
    if request.method == 'POST':
        libro_id = int(request.form['libro_id'])
        
        DevolverLibro().ejecutar(libro_id)
        return redirect(url_for('listar_prestamos'))
    return render_template('return_book.html')

@app.route('/prestamos/modificar/<int:prestamo_id>', methods=['GET', 'POST'])
def modificar_prestamo(prestamo_id):
    if request.method == 'POST':
        nuevo_libro_id = int(request.form['nuevo_libro_id'])
        nuevo_usuario_id = int(request.form['nuevo_usuario_id'])
        nueva_fecha_prestamo = request.form['nueva_fecha_prestamo']
        devolver = request.form.get('devolver') # Use .get to handle unchecked checkbox
        nueva_fecha_devolucion = request.form.get('nueva_fecha_devolucion') if devolver else None
        
        ModificarPrestamo().ejecutar(prestamo_id, nuevo_libro_id, nuevo_usuario_id, nueva_fecha_prestamo, nueva_fecha_devolucion)
        return redirect(url_for('listar_prestamos'))
    return render_template('modificar_prestamo.html', prestamo_id=prestamo_id)

@app.route('/usuarios/<int:usuario_id>/actividad')
def mostrar_actividad_usuario(usuario_id):
    class ActividadUsuarioWeb(ActividadUsuario):
        def ejecutar_web(self, usuario_id):
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
                
                actividad_data = []
                for prestamo_id, libro_id, titulo, fecha_prestamo, fecha_devolucion in filas:
                    estado = (
                        f"Devuelto el {fecha_devolucion.strftime('%Y-%m-%d')}"
                        if fecha_devolucion is not None
                        else "No devuelto aún"
                    )
                    actividad_data.append({
                        'prestamo_id': prestamo_id,
                        'libro_id': libro_id,
                        'titulo_libro': titulo,
                        'fecha_prestamo': fecha_prestamo.strftime('%Y-%m-%d'),
                        'estado': estado
                    })
                return actividad_data
            except Exception as e:
                print("Error al mostrar actividad de usuario:", e)
                return []
            finally:
                self.cursor.close()
                self.db.conn.close()

    actividad = ActividadUsuarioWeb().ejecutar_web(usuario_id)
    return render_template('user_activity.html', usuario_id=usuario_id, actividad=actividad)


if __name__ == '__main__':
    app.run(debug=True)